from bson.objectid import ObjectId
from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import current_user, login_required
from todo_app.models import Degree, Tag, Todo
from . import todos

main = Blueprint('main', __name__)


@main.route('/', methods=('GET', 'POST'))
@login_required
def index():
    userid = current_user.id
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        tag = request.form['tag']
        todo = Todo(tag, degree, content, userid)
        todos.insert_one(dict(todo))
        return redirect(url_for('main.index'))

    user_todos = list(todos.find({'userid': userid}))
    user_todos = [] if user_todos is None else user_todos
    user_todos = sorted(user_todos, key=todo_sort_key)
    return render_template('index.html', todos=user_todos)


def todo_sort_key(todo):
    todo = Todo.fromdict(todo)
    key = int(todo.tag == Tag.WORK) + \
        int(todo.degree == Degree.IMPORTANT) * 2
    # reverse
    key *= -1
    return key


@main.post('/<id>/delete/')
@login_required
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
