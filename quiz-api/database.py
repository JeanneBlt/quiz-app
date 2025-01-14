import sqlite3
import os

DB_PATH = os.path.abspath("quiz.db")  # Chemin vers votre base de données SQLite
print(f"Database path: {os.path.abspath('quiz.db')}")

def init_db():
    """Initialise la base de données en créant les tables nécessaires si elles n'existent pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT,
            title TEXT,
            image TEXT,
            position INTEGER,
            "possible answer" TEXT
        );
    """)
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    """Exécute une requête SQL avec des paramètres."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print(f"Executing query: {query} with params: {params}")  # Log pour déboguer
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

def fetch_all(query, params=()):
    """Récupère tous les résultats d'une requête SQL."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
    
