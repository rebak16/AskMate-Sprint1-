from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.read_datas()
    return render_template('/index.html', questions=questions)


@app.route('/questions/<int:question_id>')
def get_question_and_answer_by_id(question_id=None):
    quest_datas = data_manager.get_question_by_id(question_id)
    answ_datas = data_manager.get_answers_by_question_id(question_id)
    return render_template('questions.html',
                           question_id=question_id,
                           quest_datas=quest_datas,
                           answ_datas=answ_datas)


@app.route("/add-new-question", methods=['GET', 'POST'])
def route_question_add():
    if request.method == 'POST':
        data_manager.question_add(request.form['title'], request.form['message'])
        _id = data_manager.get_newest_id()
        question_id = max(_id)
        return redirect(url_for('get_question_and_answer_by_id', question_id=question_id['id']))
    return render_template('/add_new_question.html')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def route_answer_add(question_id=None):
    if request.method == 'POST':
        data_manager.answer_add(request.form['message'], question_id)
        return redirect(url_for('get_question_and_answer_by_id', question_id=question_id))

    return render_template('/add_new_answer.html', question_id=question_id)


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def route_edit(question_id=None):
    if request.method == 'POST':
        data_manager.edit_question(request.form['title'], request.form['message'], question_id)
        return redirect(url_for('get_question_and_answer_by_id', question_id=question_id))
    datas = data_manager.get_question_by_id(question_id)
    return render_template('/edit_question.html', datas=datas, question_id=question_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True,
            port=8000)
