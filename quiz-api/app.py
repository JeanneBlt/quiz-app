import hashlib
import json
from flask import Flask, request
from flask_cors import CORS
from jwt_utils import decode_token, build_token
from questions import Question, add_question_to_db, get_question_by_position, update_question_in_db, delete_all_questions , get_quiz_length
from participants import add_participant_to_db ,Participant ,get_all_scores , del_all_participants
from database import init_db, execute_query, fetch_all

app = Flask(__name__)
CORS(app)

# Initialisation de la base de données au démarrage
@app.route('/rebuild-db', methods=['POST'])
def rebuild():
    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    try:
        decode_token(token)
    
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402
    init_db()
    return "Ok" , 200

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
    try:
        size = get_quiz_length()  # Récupérer la taille du quiz
        scores, response_status = get_all_scores()  # Récupérer les scores des participants
        if response_status != 200:
            return scores, response_status
        
        # Retourner la réponse avec les champs dans le bon ordre
        return {"size": size, "scores": scores}, 200
    except Exception as e:
        return {"message": f"Error fetching quiz info: {str(e)}"}, 500

@app.route('/questions', methods=['POST'])
def post_question():
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return {"message": "Unauthorized: Missing token"}, 401

    token = token.split(" ")[1]
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402

    data = request.get_json()
    if not data:
        return {"message": "Invalid request: Missing JSON body"}, 403
    
    question = Question(data['title'], data['text'], data['image'], data['position'], data['possibleAnswers'])
    return add_question_to_db(question)


@app.route('/questions', methods=['GET'])
def get_question():
    position = request.args.get('position')
    if not position:
        return {"message": "Position parameter is required"}, 400

    question = get_question_by_position(int(position))
    if not question:
        return {"message": f"No question found at position {position}"}, 404

    return question, 200


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return {"message": "Unauthorized: Missing token"}, 401

    token = token.split(" ")[1]
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402

    data = request.get_json()
    if not data:
        return {"message": "Invalid request: Missing JSON body"}, 403

    return update_question_in_db(
        question_id,
        data['title'],
        data['text'],
        data['image'],
        data['position'],
        data['possibleAnswers']
    )

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return {"message": "Unauthorized: Missing token"}, 401

    token = token.split(" ")[1]
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402

    try:
        # Récupérer la position de la question à supprimer
        position_query = "SELECT position FROM quiz WHERE id = ?"
        result = fetch_all(position_query, (question_id,))
        if not result:
            return {"message": "Question not found"}, 404

        position_to_remove = result[0][0]

        # Supprimer la question
        delete_query = "DELETE FROM quiz WHERE id = ?"
        execute_query(delete_query, (question_id,))

        # Décaler les positions des questions au-dessus
        shift_query = """
            UPDATE quiz
            SET position = position - 1
            WHERE position > ?
        """
        execute_query(shift_query, (position_to_remove,))

        return '', 204
    except Exception as e:
        return {"message": f"Error deleting question: {str(e)}"}, 500

@app.route('/questions/all', methods=['DELETE'])
def delete_all():

    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402
    return delete_all_questions()
    
@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    try:
        query = "SELECT * FROM quiz WHERE id = ?"
        result = fetch_all(query, (question_id,))
        if not result:
            return {"message": "Question not found"}, 404

        question_data = result[0]
        question = {
            "id": question_data[0],
            "text": question_data[1],
            "title": question_data[2],
            "image": question_data[3],
            "position": question_data[4],
            "possibleAnswers": json.loads(question_data[5]),
        }

        return question, 200
    except Exception as e:
        return {"message": f"Error retrieving question: {str(e)}"}, 500

@app.route('/participations', methods=['POST'])
def add_participant():
    """
    Endpoint pour ajouter un participant à la table participants.
    Reçoit les données du participant au format JSON.
    """
    try:
        # Récupérer les données du participant depuis la requête
        data = request.get_json()

        # Vérifier que les champs nécessaires sont présents
        if 'playerName' not in data or 'answers' not in data:
            return ({"message": "Missing 'playerName' or 'answers' in the request body"}), 400

        # Créer une instance de Participant
        participant = Participant(
            playerName=data["playerName"],
            answers=data['answers']
        )

        # Ajouter le participant à la base de données
        response, status_code = add_participant_to_db(participant)
        return (response), status_code

    except Exception as e:
        return {"message": f"Error processing request: {str(e)}"}, 500




@app.route('/participations/all', methods=['DELETE'])
def supression_participants():
    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402
    response, status_cod = del_all_participants()
    return (response), status_cod


if __name__ == "__main__":
    app.run()
