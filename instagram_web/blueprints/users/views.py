from flask import Blueprint, render_template, url_for, redirect, request, flash
# from werkzeug.security import generate_password_hash, secure_filename
from models.user import User 
import re
# from .helpers import *

# app.config.from_object("flask_s3_upload.config")

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
        flash("Password should be longer than 6 characters")
        return render_template('users/new.html')

    if not(any(x.isupper() for x in password) and any(x.islower() for x in password)) :
        flash("Password should have both uppercase and lowercase characters")
        return render_template('users/new.html')

    if regex.search(password) == None:
        flash("Password should have at least one special character")
        return render_template('users/new.html')
        
    else:
        s= User(username=username, email=email, password=generate_password_hash(password))
        if s.save():
            return redirect(url_for('users.new', id=s.id))
        else:
            flash("Username not unique")
            return render_template('users/new.html')


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

# @app.route("/", methods=["POST"])
# def upload_file():

# 	# A
#     if "user_file" not in request.files:
#         return "No user_file key in request.files"

# 	# B
#     file    = request.files["user_file"]

#     """
#         These attributes are also available

#         file.filename               # The actual name of the file
#         file.content_type
#         file.content_length
#         file.mimetype

#     """

# 	# C.
#     if file.filename == "":
#         return "Please select a file"

# 	# D.
#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
#         return str(output)

#     else:
#         return redirect("/")