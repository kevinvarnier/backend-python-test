from alayatodo import app, db
from alayatodo.models import Users, Todos
from flask import (
    redirect,
    render_template,
    request,
    session, 
    flash, 
    jsonify
    )
from flask_paginate import Pagination, get_page_args



@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username= username, password=password).first()
    if user:
        session['user'] = {'username': user.username, 'id': user.id}
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo =  Todos.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    page, per_page, offset = get_page_args()
    todo_for_render_template = Todos.query.limit(per_page).offset(offset)
    todo_total = len(Todos.query.all())
    pagination = Pagination(page=page,
                            per_page=per_page,
                            offset=offset,
                            total=todo_total,
                            css_framework='bootstrap4',
                            record_name='todos')
    return render_template('todos.html', todos=todo_for_render_template, pagination=pagination)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    if request.form.get('description'): 
        description = request.form.get('description')
        todo = Todos(
            user_id=session['user']['id'],
            description=request.form.get('description')
            )
        db.session.add(todo)
        db.session.commit()
        flash("Todo correctly added")
    else : 
        flash("Please enter a description to add a todo")
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo_delete = Todos.query.filter_by(id=id).first()
    db.session.delete(todo_delete)
    db.session.commit()
    flash("Todo correctly deleted")
    return redirect('/todo')

@app.route('/todo/mark/<id>', methods=['POST'])
def todo_mark_as_complete(id):
    todo_complete = Todos.query.filter_by(id=id).first()
    todo_complete.completed = 1
    db.session.commit()
    return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
def todo_in_json(id): 
    todo = Todos.query.filter_by(id=id).first()
    todo_json = {
    "id" : todo.id, 
    "user_id" : todo.user_id,
    "description" : todo.description
    }
    return jsonify(todo_json)