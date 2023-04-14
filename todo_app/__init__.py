from pymongo import MongoClient
from flask import Flask
from flask_login import LoginManager

from todo_app.models import User

SECRET_KEY = 'qnmbyDqsp2/VT7SwrZ96FuA1zHjOu2X8AAyTaFHDcsP5RQRuafAuSYbTD8TJUfiSkps25wIRUCbC/lkg0GBeBA=='

client = MongoClient(
    'mongodb://username:password@localhost:27017/ferretdb?authMechanism=PLAIN',
    serverSelectionTimeoutMS=100)


db = client.flask_db

todos = db.todos
users = db.users


def create_app():
    app: Flask = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id) -> User:
        user = users.find_one(filter={'id': user_id})
        if user is None:
            return None
        user = User.fromdict(user)
        return user

    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    return app
