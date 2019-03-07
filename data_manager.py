import connection
from datetime import datetime
import time
import calendar

def get_all_questions():
    questions = connection.read_csv('question.csv')
    for item in questions:
        item['submission_time'] = datetime.utcfromtimestamp(int(item['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return questions

def get_all_answers():
    answers = connection.read_csv('answer.csv')
    for item in answers:
        item['submission_time'] = datetime.utcfromtimestamp(int(item['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return answers


def get_question_by_id(question_id):
    questions = get_all_questions()
    question_data = []
    for item in questions:
        item['id'] = int(item['id'])
        if question_id == item['id']:
            question_data.append(item)
    return question_data


def get_answers_by_question_id(question_id):
    answers = get_all_answers()
    answer_data = []
    for answer in answers:
        answer['question_id'] = int(answer['question_id'])
        if question_id == answer['question_id']:
            answer_data.append(answer)
    return answer_data


def question_add(ids, submission_time, title, message, image, view_number=0, vote_number=0):
    question_added = {'id': ids,
                      'submission_time': submission_time,
                      'view_number': view_number,
                      'vote_number': vote_number,
                      'title': title,
                      'message': message,
                      'image': image,
                      }
    connection.add_question(question_added)
    return question_added


def answer_add(ids, submission_time, message, image, question_id, vote_number=0):
    answer_added= {'id': ids,
                  'submission_time': submission_time,
                  'vote_number': vote_number,
                  'question_id': question_id,
                  'message': message,
                  'image': image}
    connection.add_answer(answer_added)
    return answer_added
