import connection
import util
from datetime import datetime
import time
import database_common

def get_current_time(format='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(time.time()).strftime(format)

@database_common.connection_handler
def read_datas(cursor):
    cursor.execute("""SELECT * FROM question order by submission_time desc """)
    names = cursor.fetchall()
    return names

@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""select * from question where id = %(id)s""",
                    {'id' : question_id})
    quest_datas = cursor.fetchall()
    return quest_datas
    '''questions = connection.read_datas()
    question_data = []
    for item in questions:
        item['id'] = int(item['id'])
        if question_id == item['id']:
            question_data.append(item)
    return question_data'''

@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""select * from answer where question_id = %(question_id)s""",
                   {'question_id' : question_id})
    answ_datas = cursor.fetchall()
    return answ_datas
    '''answers = connection.read_csv("answer.csv")
    answer_data = []
    for answer in answers:
        answer['question_id'] = int(answer['question_id'])
        if question_id == answer['question_id']:
            answer_data.append(answer)
    return answer_data'''

@database_common.connection_handler
def question_add(cursor, title, message):
    dt = datetime.now()
    cursor.execute("insert into question (submission_time, title, message) values(%(submission_time)s,"
                   "%(title)s, %(message)s)",
                    {'submission_time': dt,
                     'title': title,
                    'message': message})


@database_common.connection_handler
def get_newest_id(cursor):
    cursor.execute("select id from question order by id desc limit 1")
    return cursor.fetchall()


@database_common.connection_handler
def answer_add(cursor, message, question_id):
    dt = datetime.now()
    cursor.execute("insert into answer (submission_time, message, question_id) values(%(submission_time)s,"
                   "%(message)s,%(question_id)s)",
                {'submission_time': dt,
                  'message': message,
                 'question_id':question_id})


@database_common.connection_handler
def edit_question(cursor, title, message, question_id):
    cursor.execute("update question set title = %(title)s, message = %(message)s where id=%(id)s",
                    {'title':title,
                     'message':message,
                     'id':question_id})