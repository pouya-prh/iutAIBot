import sqlite3

title = input('title: ')
description = input('description: ')
instructor = input('instructor: ')
cover_image = input('cover_image: ')

conn = sqlite3.connect('sqlite3.db')
c = conn.cursor()

query = """INSERT INTO Course 
    (title, description, instructor, cover_image)
    VALUES (?, ?, ?, ?)"""

c.execute(query, (title, description, instructor, cover_image))

conn.commit()
conn.close()
print("course inserted successfully 🙌")
