import sqlite3
from datetime import datetime

class DbManager:
    
    def insert_user(telegram_id, username, first_name, last_name):
        conn = sqlite3.connect("sqlite3.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM Users WHERE telegram_ID = ?", (telegram_id,))
        if c.fetchone() is None:
            joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
                INSERT INTO Users (telegram_ID, username, first_name, last_name, joined_at, last_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (telegram_id, username, first_name, last_name, joined_at, joined_at))
            conn.commit()
            conn.close()
        else:
            last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("UPDATE Users SET last_active = ? WHERE telegram_ID = ?",(last_active, telegram_id))
            conn.commit()
            conn.close()
        
    def submit_suggestion(telegram_id, username, suggestion):
        conn = sqlite3.connect("sqlite3.db")
        c = conn.cursor()
        c.execute("INSERT INTO Suggestions (telegram_ID, username, suggestion) VALUES (?, ?, ?)",
                (telegram_id, username, suggestion))

        conn.commit()
        conn.close()