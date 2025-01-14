import json
from database import execute_query, fetch_all

class Question:
    def __init__(self, title: str, texte: str, image: str, position: int, possible_answer: str):
        self.title = title
        self.texte = texte
        self.image = image
        self.position = position
        self.possible_answer = possible_answer


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

        

