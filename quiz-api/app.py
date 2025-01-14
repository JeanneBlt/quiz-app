from flask import Flask, request
from flask_cors import CORS
import hashlib
import json
import sqlite3
import os
from jwt_utils import decode_token, build_token
from questions import Question, add_question_to_db
from database import init_db, execute_query, fetch_all

app = Flask(__name__)
CORS(app)

# Initialisation de la base de données au démarrage
init_db()

@app.route('/')
def hello_world():
    return "Hello, world!"

@app.route('/login', methods=['POST'])
def login():

        # Récupération des données JSON
        data = request.json
        if not data:
            return 'Unauthorized', 401
        
        password = data.get('password')

        # Validation des paramètres
        if  not password:
            return 'Unauthorized', 401

        # Vérification des identifiants
        try_psw = password.encode('UTF-8')
        hash = hashlib.md5(try_psw).digest()

        if hash == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
            token = build_token()

            "Good Password "
            return { "message": "Login successful","token": token},200
        else:
            return {"message" :'Unauthorized' }, 401

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/test-db', methods=['GET'])
def test_db():
    from database import fetch_all
    try:
        rows = fetch_all("SELECT * FROM quiz")
        return {"message": "Database test successful", "data": rows}, 200
    except Exception as e:
        return {"message": f"Database test failed: {e}"}, 500

@app.route('/questions', methods=['POST'])
def post_question():
    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402
    
    data = request.get_json()
    if not data:
        return {"message": "Invalid request: Missing JSON body"}, 403

    title = data.get('title')
    texte = data.get('text')
    image = data.get('image')
    position = data.get('position')
    possible_answer = data.get('possibleAnswers')

    print(f"Title: {title}")
    print(f"Texte: {texte}")
    print(f"Image: {image}")
    print(f"Position: {position}")
    print(f"Possible Answer: {possible_answer}")


    # if not all([title, texte, image, position, possible_answer]):
    #     return {"message": "Invalid request: Missing required fields"}, 401

    question = Question(title, texte, image, position, possible_answer)
    return add_question_to_db(question)

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    try:
        # Supprime toutes les questions de la base de données
        execute_query("DELETE FROM quiz")
        return {"message": "All questions deleted successfully"}, 204
    except Exception as e:
        return {"message": f"Error deleting questions: {str(e)}"}, 500

    
@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get('position')
    if not position:
        return {"message": "Position parameter is required"}, 400
    
    try:
        # Récupérer la question en fonction de la position
        from database import fetch_all
        query = "SELECT * FROM quiz WHERE position = ?"
        result = fetch_all(query, (position,))
        
        if not result:
            return {"message": f"No question found at position {position}"}, 404

        # Construire une réponse JSON formatée
        question = result[0]
        response = {
            "id": question[0],
            "text": question[1],
            "title": question[2],
            "image": question[3],
            "position": question[4],
            "possibleAnswers": json.loads(question[5])  # Convertir depuis JSON
        }
        return response, 200
    except Exception as e:
        return {"message": f"Error retrieving question: {str(e)}"}, 500
    
@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """Met à jour une question et ajuste les positions si nécessaire."""
    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402

    data = request.get_json()
    if not data:
        return {"message": "Invalid request: Missing JSON body"}, 403

    title = data.get('title')
    texte = data.get('text')
    image = data.get('image')
    new_position = data.get('position')
    possible_answer = json.dumps(data.get('possibleAnswers'))

    if not all([title, texte, image, new_position, possible_answer]):
        return {"message": "Invalid request: Missing required fields"}, 400

    try:
        # Obtenir la position actuelle de la question
        current_query = "SELECT position FROM quiz WHERE id = ?"
        current_position = fetch_all(current_query, (question_id,))
        
        if not current_position:
            return {"message": "Question not found"}, 404

        current_position = current_position[0][0]

        # Si la position change
        if current_position != new_position:
            if current_position < new_position:
                # Décaler les questions entre current_position + 1 et new_position vers le haut
                shift_query = """
                    UPDATE quiz
                    SET position = position - 1
                    WHERE position > ? AND position <= ?
                """
                execute_query(shift_query, (current_position, new_position))
            else:
                # Décaler les questions entre new_position et current_position - 1 vers le bas
                shift_query = """
                    UPDATE quiz
                    SET position = position + 1
                    WHERE position >= ? AND position < ?
                """
                execute_query(shift_query, (new_position, current_position))

        # Mettre à jour la question avec la nouvelle position
        update_query = """
            UPDATE quiz
            SET title = ?, texte = ?, image = ?, position = ?, "possible answer" = ?
            WHERE id = ?
        """
        execute_query(update_query, (title, texte, image, new_position, possible_answer, question_id))

        return '', 204
    except sqlite3.Error as e:
        return {"message": f"Error updating question: {str(e)}"}, 500

if __name__ == "__main__":
    app.run()

