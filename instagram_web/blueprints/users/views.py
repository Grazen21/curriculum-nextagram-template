from flask import Blueprint, render_template, url_for, redirect, request
from werkzeug.security import generate_password_hash
from models.user import User 
import re


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    if len(password)<7:
        errors="Password should be longer than 6 characters"
        return render_template('users/new.html',errors=errors)

    if not(any(x.isupper() for x in password) and any(x.islower() for x in password)) :
        errors="Password should have both uppercase and lowercase characters"
        return render_template('users/new.html', errors=errors)

    if regex.search(password) == None:
        errors="Password should have at least one special character"
        return render_template('users/new.html', username=username ,errors=errors)
        
    else:
        s= User(username=username, email=email, password=generate_password_hash(password))
        if s.save():
            return redirect(url_for('users.new', id=s.id))
        else:
            return render_template('users/new.html', username=username ,errors=s.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
