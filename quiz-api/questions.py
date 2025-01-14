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


    def to_dict(self):
        return {
            "title": self.title,
            "text": self.texte,
            "image": self.image,
            "position": self.position,
            "possibleAnswers": json.loads(self.possible_answer),
        }


def add_question_to_db(question: Question):
    """Ajoute une question à la base de données en décalant les positions si nécessaire."""
    try:
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

        

def get_question_by_position(position: int):
    """Récupère une question par sa position."""
    query = "SELECT * FROM quiz WHERE position = ?"
    result = fetch_all(query, (position,))
    
    if not result:
        return None

    question_data = result[0]
    return {
        "id": question_data[0],
        "text": question_data[1],
        "title": question_data[2],
        "image": question_data[3],
        "position": question_data[4],
        "possibleAnswers": json.loads(question_data[5]),
    }


def update_question_in_db(question_id, title, texte, image, new_position, possible_answers):
    """Met à jour une question et ajuste les positions si nécessaire."""
    current_query = "SELECT position FROM quiz WHERE id = ?"
    current_position = fetch_all(current_query, (question_id,))
    
    if not current_position:
        return {"message": "Question not found"}, 404

    current_position = current_position[0][0]

    if current_position != new_position:
        if current_position < new_position:
            shift_query = """
                UPDATE quiz
                SET position = position - 1
                WHERE position > ? AND position <= ?
            """
            execute_query(shift_query, (current_position, new_position))
        else:
            shift_query = """
                UPDATE quiz
                SET position = position + 1
                WHERE position >= ? AND position < ?
            """
            execute_query(shift_query, (new_position, current_position))

    update_query = """
        UPDATE quiz
        SET title = ?, texte = ?, image = ?, position = ?, "possible answer" = ?
        WHERE id = ?
    """
    execute_query(update_query, (title, texte, image, new_position, json.dumps(possible_answers), question_id))
    return '', 204


def delete_all_questions():
    """Supprime toutes les questions de la base de données."""
    try:
        execute_query("DELETE FROM quiz")
        return {"message": "All questions deleted successfully"}, 204
    except Exception as e:
        return {"message": f"Error deleting questions: {str(e)}"}, 500
