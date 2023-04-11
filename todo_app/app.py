from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
username = 'flask'
password = 'CKMMymVGKnTVW%2B62Z5K5H8Hxp3jA9Mmf%2FC98E82FWyA%3D'

client = MongoClient(
    f'mongodb://username:password@localhost:27017/ferretdb?authMechanism=PLAIN', serverSelectionTimeoutMS=100)


db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        tag = request.form['tag']
        todos.insert_one({'content': content, 'degree': degree, 'tag': tag})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
