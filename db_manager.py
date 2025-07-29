import sqlite3
from datetime import datetime
from events import Events 

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
        
    def return_events():
        conn = sqlite3.connect("sqlite3.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = "SELECT * FROM Events WHERE status = 1"
        c.execute(query)
        rows = c.fetchall()
        conn.close()

        events = []
        for row in rows:
            kwargs = {
                'ID' : row['ID'],
                'title': row['title'],
                'description': row['description'],
                'start_time': row['start_time'],
                'location': row['location'],
                'status': row['status'],
                'capacity': row['capacity'],
                'cover_image': row['cover_image'],
                'payment': row['payment'],
            }
            events.append(Events(**kwargs))
        return events
    
    def event_register_db(telegram_id, event_id):
        conn = sqlite3.connect("sqlite3.db")
        c = conn.cursor()
        c.execute("SELECT ID, is_active FROM Users WHERE telegram_ID = ?", (telegram_id,))
        user_row = c.fetchone()
        if user_row is None:
            conn.close()
            return 'user not found'
        elif user_row[1] == 0:
            conn.close()
            return 'user has been deactivated'
        user_id = user_row[0]

        c.execute("SELECT capacity FROM Events WHERE ID = ?", (event_id,))
        event_row = c.fetchone()
        if event_row is None:
            conn.close()
            return 'event not found'
        if event_row[0] <= 0:
            conn.close()
            return 'event is full'

        c.execute("SELECT 1 FROM Enrollments WHERE event_ID = ? AND user_ID = ?", (event_id, user_id))
        if c.fetchone():
            conn.close()
            return 'already registered'
        c.execute(" SELECT payment FROM Events WHERE ID = ?", (event_id, ))
        event_row = c.fetchone()
        conn.close()
        if event_row == 0:
            registered_At = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO Enrollments (event_ID, user_ID, registered_at, status) VALUES (?, ?, ?, ?)",
                    (event_id, user_id, registered_At, 'confirmed'))
            c.execute("UPDATE Events SET capacity = capacity - 1 WHERE ID = ?", (event_id,))
            conn.commit()
            conn.close()
            return 'successfully registered'
        else:
            return 'payment'
            
        

            

    def get_user_profile(telegram_id):
        try:
            conn = sqlite3.connect("sqlite3.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT first_name, last_name, phone, university, entry_year 
                FROM UserProfile 
                WHERE telegram_ID = ?
            """, (telegram_id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                return {
                    'first_name': result[0],
                    'last_name': result[1], 
                    'phone': result[2],
                    'university': result[3],
                    'entry_year': result[4]
                }
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None

    def save_user_profile(telegram_id, profile_data):
        try:
            conn = sqlite3.connect("sqlite3.db")
            cursor = conn.cursor()
                    
            cursor.execute("SELECT id FROM UserProfile WHERE telegram_ID = ?", (telegram_id,))
            existing = cursor.fetchone()
            last_edit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if existing:
                cursor.execute("""
                    UPDATE UserProfile 
                    SET first_name = ?, last_name = ?, phone = ?, university = ?, entry_year = ?, last_edit = ?
                    WHERE telegram_id = ?
                """, (profile_data['first_name'], profile_data['last_name'], 
                    profile_data['phone'], profile_data['university'], 
                    profile_data['entry_year'], last_edit, telegram_id))
            else:
                cursor.execute("""
                    INSERT INTO UserProfile (telegram_id, first_name, last_name, phone, last_edit, university, entry_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (telegram_id, profile_data['first_name'], profile_data['last_name'],
                    profile_data['phone'], last_edit, profile_data['university'], profile_data['entry_year']))
            
            conn.commit()
            conn.close()
            print(f"Profile saved for user {telegram_id} {profile_data['first_name']} {profile_data['last_name']}")
            
        except Exception as e:
            print(f"Error saving user profile: {e}")
            conn.rollback()
