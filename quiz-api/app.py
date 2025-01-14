from flask import Flask, request
from flask_cors import CORS
import hashlib
from jwt_utils import decode_token, build_token
from questions import Question, add_question_to_db , del_all_question , get_quiz_length
from participants import add_participant_to_db ,Participant ,get_all_scores , del_all_participants
from database import init_db

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
     
        size = get_quiz_length()
      
        scores, response = get_all_scores()
        
    except Exception as e:
        return e, 402
    return {"size": size , "scores" : scores},200

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



@app.route('/questions/all', methods=['DELETE'])
def supression_questions():
    token = request.headers.get('Authorization')
    if not token:
        return {"message": "Unauthorized: Missing token"}, 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    try:
        decode_token(token)
    except Exception as e:
        return {"message": f"Unauthorized: {str(e)}"}, 402
    response, status_cod = del_all_question()
    return (response), status_cod


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

