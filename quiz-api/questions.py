import json
from database import execute_query, fetch_all

class Question:
    def __init__(self, title: str, texte: str, image: str, position: int, possible_answer: str):
        self.title = title
        self.texte = texte
        self.image = image
        self.position = position
        self.possible_answer = possible_answer

def add_question_to_db(question: Question):
    """Ajoute une question à la base de données."""
    query = """
        INSERT INTO quiz (title, texte, image, position, "possible answer")
        VALUES (?, ?, ?, ?, ?)
    """
    # Convertir la liste en JSON
    possible_answer_json = json.dumps(question.possible_answer)
    params = (question.title, question.texte, question.image, question.position, possible_answer_json)
    
    try:
        execute_query(query, params)
        return {"message": "Question added successfully"}, 200
    except Exception as e:
        return {"message": f"Error adding question: {str(e)}"}, 400
