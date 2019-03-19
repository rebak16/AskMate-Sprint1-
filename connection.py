import csv
import os
import database_common

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def add_question(new_question):
    with open('question.csv', "a") as question:
        writer = csv.DictWriter(question, fieldnames=DATA_HEADER)
        writer.writerow(new_question)

def edit_question(edited_question):
    question_list = read_csv("question.csv")
    with open('question.csv', "w") as f:
        writer = csv.DictWriter(f, fieldnames=DATA_HEADER)
        writer.writeheader()
        for question in question_list:
            if question["id"] == edited_question["id"]:
                writer.writerow(edited_question)
            else:
                writer.writerow(question)


def add_answer(new_answer):
    with open('answer.csv', 'a') as answer:
        writer = csv.DictWriter(answer, fieldnames=ANSWER_DATA_HEADER)
        writer.writerow(new_answer)

