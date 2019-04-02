from flask import Flask, render_template, request, redirect, url_for, session, escape
import data_manager
import password_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.read_question_datas()
    return render_template('/index.html', questions=questions)


@app.route('/questions/<int:question_id>')
def get_question_and_answer_and_comments_by_id(question_id=None):
    quest_datas = data_manager.get_question_by_id(question_id)
    answ_datas = data_manager.get_answers_by_question_id(question_id)
    q_comm_datas = data_manager.get_comment_by_question_id(question_id)
    a_comm_datas = data_manager.get_comment_by_question_id(question_id)
    return render_template('questions.html',
                           question_id=question_id,
                           quest_datas=quest_datas,
                           answ_datas=answ_datas,
                           q_comm_datas=q_comm_datas,
                           a_comm_datas=a_comm_datas,
                           )


@app.route("/add-new-question", methods=['GET', 'POST'])
def route_question_add():
    if request.method == 'POST':
        data_manager.question_add(request.form['title'], request.form['message'])
        _id = data_manager.get_newest_id()
        question_id = max(_id)
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id['id']))
    return render_template('/add_new_question.html')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def route_answer_add(question_id=None):
    if request.method == 'POST':
        data_manager.answer_add(request.form['message'], question_id)
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))

    return render_template('/add_new_answer.html', question_id=question_id)


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def route_edit_question(question_id=None):
    if request.method == 'POST':
        data_manager.edit_question(request.form['title'], request.form['message'], question_id)
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))
    datas = data_manager.get_question_by_id(question_id)
    return render_template('/edit_question.html', datas=datas)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id=None):
    answer_datas = data_manager.get_answer_datas(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(request.form['message'], answer_id)
        question_id = answer_datas[0]['question_id']
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))
    return render_template('/edit_answer.html', datas=answer_datas)


@app.route("/search", methods=['GET', 'POST'])
def search():
    search_phrase = request.form.get('search_phrase')
    search_result = data_manager.search_question(search_phrase)
    return render_template('search_results.html', search_phrase=search_phrase, search_result=search_result)


@app.route("/question/<int:question_id>/delete", methods=['GET'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('route_list'))


@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id=None):
    comment_datas = data_manager.get_comment_datas(comment_id)
    if request.method == 'POST':
        data_manager.edit_comment(request.form['message'], comment_id)
        question_id = comment_datas[0]['question_id']
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))
    return render_template('/edit_comment.html', datas=comment_datas)


@app.route('/comment/<int:comment_id>/delete')
def route_delete_comment(comment_id=None):
    comment_datas = data_manager.get_comment_datas(comment_id)
    data_manager.delete_comment( comment_id)
    question_id = comment_datas[0]['question_id']
    return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))


@app.route("/question/<int:question_id>/new-q_comment", methods=['GET', 'POST'])
def q_comment_add(question_id):
    if request.method == 'POST':
        data_manager.q_comment_add(request.form.get('message'), question_id)
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))

    return render_template('/add_new_q_comment.html', question_id=question_id)


@app.route("/question/<int:question_id>/<int:answer_id>/new-a_comment", methods=['GET', 'POST'])
def a_comment_add(question_id, answer_id=None):
    if request.method == 'POST':
        data_manager.a_comment_add(request.form.get('message'), question_id, answer_id)
        return redirect(url_for('get_question_and_answer_and_comments_by_id', question_id=question_id))

    return render_template('/add_new_a_comment.html', question_id=question_id, answer_id=answer_id)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hash_pw = data_manager.login(request.form['username'])
        if hash_pw and password_manager.verify_password(request.form['password'], hash_pw) is False:
            invalid_username_or_password = 'Invalid username or password!'
            return render_template('/login.html', invalid_username_or_password=invalid_username_or_password)
        elif hash_pw and password_manager.verify_password(request.form['password'], hash_pw):
            session['username'] = request.form['username']
        return redirect('/')
    return render_template('/login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pw = request.form['confirm_password']
        if password == confirm_pw:
            try:
                data_manager.register(username, password, request.form['first_name'], request.form['last_name'], request.form['email'])
                return redirect('/')
            except:
                invalid_username = "Username is already used"
                return render_template("register.html", invalid_username=invalid_username)
    return render_template("register.html")


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def vote_up(question_id):
    data_manager.vote_up(question_id)
    return redirect(url_for('route_list', question_id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def vote_down(question_id):
    data_manager.vote_down(question_id)
    return redirect(url_for('route_list', question_id=question_id))


@app.route('/users')
def list_of_users():
    users = data_manager.list_of_users()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True,
            port=8000)
