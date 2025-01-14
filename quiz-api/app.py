import hashlib
from flask import Flask, request
from flask_cors import CORS
from jwt_utils import decode_token, build_token
from questions import Question, add_question_to_db, get_question_by_position, update_question_in_db, delete_all_questions
from database import init_db, execute_query, fetch_all

app = Flask(__name__)
CORS(app)

# Initialisation de la base de données au démarrage
init_db()

@app.route('/')
def hello_world():
    return "Hello, world!"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('password'):
        return 'Unauthorized', 401

    password = data.get('password').encode('UTF-8')
    hash = hashlib.md5(password).digest()

    if hash == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
        token = build_token()
        return {"message": "Login successful", "token": token}, 200
    else:
        return {"message": "Unauthorized"}, 401

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
    return delete_all_questions()


if __name__ == "__main__":
    app.run()
