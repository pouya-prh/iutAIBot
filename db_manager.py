import sqlite3
from datetime import datetime

class DbManager:
    
    def insert_user(telegram_id, username, first_name, last_name):
        conn = sqlite3.connect("sqlite3.db")
        c = conn.cursor()

        joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("""
            INSERT OR IGNORE INTO Users (telegram_id, username, first_name, last_name, joined_at, last_activate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (telegram_id, username, first_name, last_name, joined_at, joined_at))
        
        conn.commit()
        conn.close()
