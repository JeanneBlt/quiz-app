import sqlite3
import os

DB_PATH = os.path.abspath("quiz.db")  # Chemin vers la base de données SQLite
print(f"Database path: {os.path.abspath('quiz.db')}")

def init_db():
    """Initialise la base de données en créant les tables nécessaires si elles n'existent pas."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texte TEXT,
                title TEXT,
                image TEXT,
                position INTEGER,  -- Position doit être unique
                "possible answer" TEXT
            );
        """)
        conn.commit()

def execute_query(query, params=()):
    """Exécute une requête SQL avec des paramètres."""
    try:
        with sqlite3.connect(DB_PATH, timeout=30) as conn:  # Timeout pour éviter "database is locked"
            cursor = conn.cursor()
            print(f"Executing query: {query} with params: {params}")  # Log pour déboguer
            cursor.execute(query, params)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

def fetch_all(query, params=()):
    """Récupère tous les résultats d'une requête SQL."""
    with sqlite3.connect(DB_PATH, timeout=30) as conn:  # Timeout pour éviter "database is locked"
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
