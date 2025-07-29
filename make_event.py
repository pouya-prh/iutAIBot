import sqlite3
from datetime import datetime

title = input('title: ')
description = input('description: ')
start_time = input('start_time: ')
location = input('location: ')
status = input('status: ')
capacity = input('capacity: ')
cover_image = input('cover_image: ')

if not capacity:
    capacity = None
else:
    capacity = int(capacity)

created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

conn = sqlite3.connect('sqlite3.db')
c = conn.cursor()

query = """INSERT INTO Events 
    (title, description, start_time, location, created_at, status, capacity, cover_image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

c.execute(query, (title, description, start_time, location , created_at, status, capacity, cover_image))

conn.commit()
conn.close()
print("Event inserted successfully 🙌")
