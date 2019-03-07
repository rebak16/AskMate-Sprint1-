import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_csv(filename, one_question_id=None):
    question_list = []
    with open(filename, "r") as questions:
        quest_reader = csv.DictReader(questions)
        sorted_datas = sorted(quest_reader, key=lambda row: row['submission_time'], reverse=True)
        for row in sorted_datas:
            question = dict(row)
            if one_question_id is not None and one_question_id == question['id']:
                return question
            question_list.append(question)

        return question_list


def add_question(new_question):
    with open('question.csv', "a") as question:
        writer = csv.DictWriter(question, fieldnames=DATA_HEADER)
        writer.writerow(new_question)


def add_answer(new_answer):
    with open('answer.csv', 'a') as answer:
        writer = csv.DictWriter(answer, fieldnames=ANSWER_DATA_HEADER)
        writer.writerow(new_answer)

