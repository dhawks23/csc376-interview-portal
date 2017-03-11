import sqlite3


def add_user(conn, name, pass_hash, perms):
    '''Add a new user with the specified username, password hash, and
    permissions.
    '''

    curs = conn.cursor()
    curs.execute('INSERT INTO Users (user_name, user_password, user_perms) VALUES (?, ?)', (name, pass_hash, perms))
    curs.close()
    conn.commit()


def delete_user(conn, user_id):
    '''Delete the user with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Users WHERE user_id = ?', (user_id))
    curs.close()
    conn.commit()


def retrieve_user_name(conn, user_id):
    '''Retrieve the username of the user with the given ID.'''

    curs = conn.cursor()
    curs.execute('SELECT user_name FROM Users WHERE user_id = ?', (user_id))
    username = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return username


def retrieve_user_by_name(conn, username):
    '''Retrieve the user ID of the user with the given name.'''

    curs = conn.cursor()
    curs.execute('SELECT user_id FROM Users WHERE user_name = ?', (username,))
    user_id = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return user_id


def create_interview(conn, interview_id, name, description, user):
    '''Create a new interview with the given name and description.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Interviews VALUES (?, ?, ?, ?)',
                 (interview_id, name, description, user))
    curs.close()
    conn.commit()


def delete_interview(conn, interview_id):
    '''Delete the interview with the given ID.

    This will also delete any questions where question_interview =
    interview_id.
    '''

    curs = conn.cursor()
    curs.execute('DELETE FROM Interviews WHERE interview_id = ?',
                 (interview_id))
    curs.execute('DELETE FROM Questions WHERE question_interview = ?',
                 (interview_id))
    curs.close()
    conn.commit()


def retrieve_interview_title(conn, interview_id):
    '''Retrieve the title of the interview with the given ID.'''

    curs = conn.cursor()
    curs.execute('''SELECT interview_name FROM Interviews
                      WHERE interview_id = ?''',
                 (interview_id,))
    title = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return title

def retrieve_interview_all(conn):
	curs = conn.cursor()
	interviews = curs.execute('SELECT interview_id, interview_name FROM Interviews') 
	#curs.close()
	conn.commit()
	return interviews

def assign_interview(conn, interview_id, interview_user ):
	curs = conn.cursor()
	interviews = curs.execute('UPDATE Interviews set interview_user = ? where interview_id = ?',
		(interview_user, interview_id)) 
	curs.close()
	conn.commit()

def add_question(conn, question_id, interview, text):
    '''Add a new question with the given text to the given interview.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Questions VALUES (?, ?, ?)',
                 (question_id, interview, text))
    curs.close()
    conn.commit()


def delete_question(conn, question_id):
    '''Delete the question with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Questions WHERE question_id = ?', (question_id))
    curs.execute('DELETE FROM Answers WHERE answer_question = ?',
                 (question_id))
    curs.close()
    conn.commit()


def retrieve_question(conn, question_id):
    '''Retrieve the question with the given ID.'''

    curs = conn.cursor()
    curs.execute('SELECT question_text FROM Questions WHERE question_id = ?')
    text = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return text


def add_answer(conn, user_id, question_id, text):
    '''Add an answer by user_id to question_id with the given text.'''

    curs = conn.cursor()
    curs.execute('''INSERT INTO Answers (answer_user, answer_question, answer_text)
                      VALUES (?, ?, ?)''', (user_id, question_id, text))
    curs.close()
    conn.commit()


def delete_answer(conn, answer_id):
    '''Delete the answer with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Answers WHERE answer_id = ?', (answer_id))
    curs.close()
    conn.commit()


def retrieve_answer(conn, user_id, question_id):
    '''Retrieve the given user's answer to the given question.'''

    curs = conn.cursor()
    curs.execute('''SELECT answer_text FROM Answers
                      WHERE answer_user = ?
                      AND answer_question = ?''',
                 (user_id, question_id))
    ans = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return ans


if __name__ == '__main__':
    try:
        conn = sqlite3.connect('test.db')
        add_user(conn, 'cobrien', None, 0)
        conn.close()
    finally:
        import os
        os.remove('test.db')
