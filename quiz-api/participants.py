import json
from database import execute_query, fetch_all
from questions import get_quiz_length

class Participant:  
    def __init__(self , playerName: str , answers: list):
        """
        Initialise un participant avec un nom et une liste de réponses.

        :param playerName: Nom du joueur (str)
        :param answers: Liste de réponses du joueur (list)
        """
        self.playerName = playerName
        self.answers = answers


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
            INSERT INTO participants (playerName, answers , score)
            VALUES (?, ?, ?)
        """
        # Convertir la liste de réponses en JSON
        answers_json = json.dumps(participant.answers)
        score = calcul_score(answers_json)
        params = (participant.playerName, answers_json, score)
        execute_query(query, params)

        

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
def del_all_participants():
    try: 
        querry = "DELETE FROM participants"
        execute_query(querry)
        return {"message": "base participants suprimé"}, 204
    except Exception as e:
        return {"message": f"Error delete: {str(e)}"}, 400


def get_all_scores():
    try:
        querry = "select playerName ,score from participants"
        result = fetch_all(querry)
        return  result , 200
    except Exception as e:
        return {"message": f"Error score: {str(e)}"}, 400
