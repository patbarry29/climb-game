#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage
from html import escape
import pymysql as db
            
print('Content-Type: text/plain')
print()

form_data = FieldStorage()
score = escape(form_data.getfirst('score', '').strip())
difficulty = ''
q_mark = False
for i in score:
    if i == '?':
        q_mark = True
        score = score.replace(i, '')
    if q_mark and i != '?':
        score = score.replace(i, '')
        difficulty += i
# print(score)
try:    
    connection = db.connect('localhost', 'pb22', 'ivohj', 'cs6503_cs1106_pb22')
    cursor = connection.cursor(db.cursors.DictCursor)
    # cursor.execute("""INSERT INTO game_data (score, difficulty) VALUES ('%s', '%s')""" % (score, difficulty))
    # connection.commit()
    print('success', score)
    cursor.close()  
    connection.close()
except db.Error:
    print('nope')