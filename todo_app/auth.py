from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
import uuid

from todo_app.models import User
from . import users

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = users.find_one(filter={'email': email})

    # check if the user actually exists
    # take the user-supplied password, hash it,
    # and compare it to the hashed password in the database
    if user is None or \
            password is None or \
            not check_password_hash(user['password'], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # convert user dict to user class
    user = User.fromdict(user)

    # the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    id = str(uuid.uuid4())

    if password is None:
        flash('Please provide a password')
        return redirect(url_for('auth.signup'))

    if email is None:
        flash('Please provide an email')
        return redirect(url_for('auth.signup'))

    if name is None:
        flash('Please provide a name')
        return redirect(url_for('auth.signup'))

    # Hash the password so the plaintext version isn't saved.
    password = generate_password_hash(password, method='sha256')

    user = users.find_one(filter={'email': email})

    if user is not None:
        # if the email is already in use, the user already exists
        # so we redirect them to the signup page again
        flash('Email address already exists!')
        return redirect(url_for('auth.signup'))

    new_user = User(id, email, password, name)
    users.insert_one(dict(new_user))
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
