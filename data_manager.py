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
                    {'id': question_id})
    quest_datas = cursor.fetchall()
    return quest_datas


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""select * from answer where question_id = %(question_id)s""",
                   {'question_id': question_id})
    answ_datas = cursor.fetchall()
    return answ_datas

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
    cursor.execute("insert into answer (submission_time, question_id, message) values(%(submission_time)s, %(question_id)s,"
                   "%(message)s)",
                   {'submission_time': dt,
                    'question_id': question_id,
                    'message': message})


@database_common.connection_handler
def edit_question(title, message, id_, view_number=0, vote_number=0, image=""):
    edited_question = {'id': id_,
                       'submission_time': get_current_time(),
                       'title': title,
                       'message': message,
                       'view_number': view_number,
                       'vote_number': vote_number,
                       'image': image,
                       }
    connection.edit_question(edited_question)
    return edited_question
