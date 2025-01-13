from flask import Flask , request
from flask_cors import CORS
import hashlib
from jwt_utils import decode_token,build_token

app = Flask(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'guys'
	return f"Hello, {x}"

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

if __name__ == "__main__":
    app.run()

