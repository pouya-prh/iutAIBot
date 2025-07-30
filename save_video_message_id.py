import sqlite3

course_id = input('course id: ')
message_id = input('message_id: ')
course_title = input('course title: ')
course_episode = input('course episode: ')
instructor = input('instructor: ')

conn = sqlite3.connect('sqlite3.db')
c = conn.cursor()

c.execute(" INSERT INTO Course_MessageID (course_ID, message_ID, course_title, episode, instructor) VALUES (?, ?, ?, ?, ?)",
(course_id, message_id, course_title, course_episode, instructor))

conn.commit()
conn.close()
print("course inserted to Course&MessageID successfully 🙌")