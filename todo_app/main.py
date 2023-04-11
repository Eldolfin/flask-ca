from bson.objectid import ObjectId
from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import current_user, login_required
from todo_app.models import Todo
from . import todos

main = Blueprint('main', __name__)


@main.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        tag = request.form['tag']
        todo = Todo(tag, degree, content)
        # todos.insert_one({'content': content, 'degree': degree, 'tag': tag})
        todos.insert_one(dict(todo))
        return redirect(url_for('main.index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@main.post('/<id>/delete/')
@login_required
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
