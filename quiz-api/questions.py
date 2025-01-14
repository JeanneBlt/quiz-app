import json
from database import execute_query, fetch_all

class Question:
    def __init__(self, title: str, texte: str, image: str, position: int, possible_answer: str):
        self.title = title
        self.texte = texte
        self.image = image
        self.position = position
        self.possible_answer = possible_answer

class Participant:  
    def __init__(self , playerName: str , answers: list):
        """
        Initialise un participant avec un nom et une liste de réponses.

        :param playerName: Nom du joueur (str)
        :param answers: Liste de réponses du joueur (list)
        """
        self.playerName = playerName
        self.answers = answers

def del_all_question():
    try: 
        querry = "DELETE FROM quiz"
        execute_query(querry)
        return {"message": "base quiz suprimé"}, 204
    except Exception as e:
        return {"message": f"Error delete: {str(e)}"}, 400


def add_question_to_db(question: Question):
    """Ajoute une question à la base de données en décalant les positions si nécessaire."""
    try:
        # Décaler les positions des questions existantes sans utiliser ORDER BY
        shift_query = """
            UPDATE quiz
            SET position = position + 1
            WHERE position >= ?
        """
        execute_query(shift_query, (question.position,))
        
        # Insérer la nouvelle question
        query = """
            INSERT INTO quiz (title, texte, image, position, "possible answer")
            VALUES (?, ?, ?, ?, ?)
        """
        # Convertir la liste en JSON
        possible_answer_json = json.dumps(question.possible_answer)
        params = (question.title, question.texte, question.image, question.position, possible_answer_json)
        execute_query(query, params)

        return {"message": "Question added successfully"}, 200
    except Exception as e:
        return {"message": f"Error adding question: {str(e)}"}, 400

def get_quiz_length():
    """
    Récupère le nombre total de questions dans la table quiz.
    :return: Nombre de questions (int).
    """
    try:
        query = "SELECT COUNT(*) FROM quiz"
        result = fetch_all(query)
        return result[0][0] if result else 0
    except Exception as e:
        raise Exception(f"Error fetching quiz length: {str(e)}")

def add_participant_to_db(participant: Participant):
    """Ajoute un participant à la table participants."""
    try:
 
        quiz_length = get_quiz_length()

        if len(participant.answers) != quiz_length:
            return {
                "message": f"Answers length must match the number of questions in the quiz ({quiz_length})."
            }, 400

        # Insérer le participant dans la table
        query = """
            INSERT INTO participants (playerName, answers)
            VALUES (?, ?)
        """
        # Convertir la liste de réponses en JSON
        answers_json = json.dumps(participant.answers)
        params = (participant.playerName, answers_json)
        execute_query(query, params)

        score = calcul_score(answers_json)

        return ({"message": "Participant added successfully", "playerName" : participant.playerName ,"score" : score}), 200
    except Exception as e:
        return {"message": f"Error adding participant: {str(e)}"}, 400

def calcul_score(answers):
    answers = json.loads(answers)
    print(answers)
    try:
        querry = 'SELECT position,"possible answer" FROM quiz'
        result = fetch_all(querry)
    except Exception as e:
        return {"message": f"Query error: {str(e)}"},400
    quiz_dict = {row[0]: json.loads(row[1]) for row in result} 
    
    score = 0
    for i, response in enumerate(answers):
        print("______")
        print(i)
        reponse_correct = next((j for j, item in enumerate(quiz_dict[i+1]) if item["isCorrect"] is True), None) +1
        print(response)
        print(reponse_correct)
        
        if reponse_correct == response:
            score= score + 1
        
    return score

        

