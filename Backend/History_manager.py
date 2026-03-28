import sqlite3
import uuid
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            SessionId TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_session():
    SessionId=str(uuid.uuid4())
    return SessionId

def save_message(SessionId: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (SessionId, role, content)
        VALUES (?, ?, ?)
    ''', (SessionId, role, content))
    conn.commit()
    conn.close()    

def get_history(SessionId: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, content FROM messages
        WHERE SessionId = ?
        ORDER BY timestamp ASC
    ''', (SessionId,))
    rows = cursor.fetchall()
    conn.close()
    history=[{'role': row[0], 'content': row[1]} for row in rows]
    return history

def clear_history(SessionId: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM messages
        WHERE SessionId = ?
    ''', (SessionId,))
    conn.commit()
    conn.close()

init_db()