#!/usr/local/bin/python3

from cgi import FieldStorage

import pymysql as db

from html import escape

from cgitb import enable
enable()

print('Content-type: text/html')
print()

form_data = FieldStorage()

outcome = ''
low_scores = []
name = ''

try:
    connection = db.connect('localhost', 'username', 'password', 'database_name')
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute('''SELECT name FROM game_data''')
    if len(form_data) > 0:
        for row in cursor.fetchall():
            if row['name'] == 'anon':
                name = escape(form_data.getfirst('name'))
                if name != '':
                    cursor.execute('''UPDATE game_data SET name = %s WHERE name=%s ''', (name, row['name']))
                    connection.commit()
    # cursor.execute('''INSERT INTO game_data (name, score, difficulty) VALUES ('creator is best', '107', 'hard')''')
    # connection.commit()
    cursor.execute('''SELECT * FROM game_data ORDER BY score DESC, name''')
    outcome = '''<table>
                        <th colspan="4">Top 10 Scorers</th>
                        <tr>
                            <th scope='col'>Rank</th><th scope='col'>Name</th><th scope='col'>Score</th><th scope='col'>Difficulty</th>
                        </tr>'''

    acc = 1
    acc2 = 7
    for row in cursor.fetchall():
        if int(row['score']) >= 100:
            outcome += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (acc, row['name'].title(), row['score'], row['difficulty'].capitalize())
            acc += 1
        else:
            low_scores.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (acc2, row['name'].title(), row['score'], row['difficulty'].capitalize()))
            acc2 += 1
        if acc > 6:
            break

    for row in low_scores:
        if acc > 10:
            break
        outcome += row
        acc += 1
        
    outcome += '</table>'
    cursor.close()
    connection.close()

except db.Error:
    outcome = '<p>My leaderboard is having some technical difficulties right now, try again later</p>'


print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Climb</title>
            <link rel="stylesheet" href="climb.css">
            <script src="climb.js" type="module"></script>
        </head>
        <body>
            <header>
                <img src='images/ladder.png' />
                <h1>Climb: A Game by Me*</h1>
                <img src='images/ladder.png' />
            </header>

            <p>
                I made this website while involuntarily locked inside my own home.
            </p>

            <button onclick="controls()">Click here for Controls</button>
            <section id = 'instructions'></section>

            <form>
                <input type='text' name='name' placeholder='Name' value='%s' maxlength='15'/>
                <input type='submit' value='Submit'>
            </form>
            <section id ='game'>
                <canvas width="700" height="500">
                </canvas>
                %s
            </section>

            <button onclick="read_more()">Click here to Read about my Game</button>
            <section id = 'inspiration'></section>

            <script>
                function controls() {
                    let section1 = document.getElementById('instructions')
                    if (section1.innerHTML === '') {
                    section1.innerHTML = "<h1>How to Play</h1><p>The aim of the game is to reach the bottle of blue \
                        liquid at the top level before time runs out or the enemy (coronavirus) catches you.</p><p>You \
                        can change the difficulty of the game by clicking the buttons at the top of the screen. Note \
                        that changing this will also change the score in the top right corner. When you get to the first\
                        level, the game will start and the score will tick down. If you go for 'Easy' mode. Your score \
                        starts at 75. 'Medium' starts at 100 and 'Hard' at 125. This also means you have less time to \
                        complete the game. You have 25, 35, and 45 seconds to complete easy, medium, and hard \
                        respectively.</p><h1>Controls</h1><p>UP Arrow or W to climb when on a ladder</p><p>DOWN Arrow or \
                        S to descend when above or on a ladder</p><p>LEFT and RIGHT Arrows or A and D to move your player \
                        left or right</p>"
                    } else {
                        section1.innerHTML = ''
                    }
                }
                function read_more() {
                    let section2 = document.getElementById('inspiration')
                    if (section2.innerHTML === '') {
                        section2.innerHTML = "<h1>My Inspiration for this Game</h1><p>When this assignment was given to me,\
                            I wasn't sure what to do. I had a few ideas, such as:<ul><li>A movie database (like \
                            <a href='https://www.letterboxd.com'>Letterboxd</a>)</li><li>A replica of a famous arcade \
                            game which involves a yellow monster ruthlessly murdering his stalker ghosts (they were \
                            just following orders!)</li><li>another replica of a game Nintendo made back in the day \
                            with some kind of gorilla throwing barrels at a moustache'd plumber trying to keep the \
                            princess safe, only for the plumber to kidnap the princess in the end.</li></ul></p>\
                            <p>After thinking about it for a few days, I decided to try and recreate the Nintendo \
                            game. Another day later, when I realised how big and scary the Nintendo trademark is, \
                            I decided to come up with my own game which would be loosely based on the two games I \
                            describe above.</p>"
                    } else {
                        section2.innerHTML = ''
                    }
                }
            </script>
            <footer>
                <p>*Me = Patrick Barry</p>
            </footer>
        </body>
    </html>""" % (name, outcome))
