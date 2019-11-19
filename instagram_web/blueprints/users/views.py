from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models.user import User 
from models.userimages import Images
import re
from flask_login import login_user, logout_user, current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3
from config import Config




ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        flash("Password should be longer than 6 characters", "alert alert-danger")
        return render_template('users/new.html')

    if not(any(x.isupper() for x in password) and any(x.islower() for x in password)) :
        flash("Password should have both uppercase and lowercase characters", "alert alert-danger")
        return render_template('users/new.html')

    if regex.search(password) == None:
        flash("Password should have at least one special character", "alert alert-danger")
        return render_template('users/new.html')
        
    else:
        s= User(username=username, email=email, password=generate_password_hash(password))
        if s.save():
            flash("New account created", "alert alert-success")
            return redirect(url_for('users.new', id=s.id))
        else:
            flash("Username not unique", "alert alert-danger")
            return render_template('users/new.html')

@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    username = request.form.get('username')
    email= request.form.get('email')
    password= request.form.get('password')

    if current_user ==  user: # current_user method is from Flask-Login
        if len(username) > 0:
            s= User.get_or_none(User.id==user)
            s.username= username
            s.save()
            flash('Username succesfully changed', 'alert alert-success')
        if len(email) > 0:
            s= User.get_or_none(User.id==user)
            s.email= email
            s.save()
            flash('Email successfully changed', 'alert alert-success')
        if len(password) > 0:
            s= User.get_or_none(User.id==user)
            s.password= generate_password_hash(password)
            s.save()
            flash('Password successfully changed', 'alert alert-success')
        else:
            flash('Please enter changes to your account.', 'alert alert-danger')

        return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash('Please first sign up or login to your account.', 'alert alert-danger')
        return redirect(url_for('sessions.sign_in'))
    
    # Don't update
    # Do whatever else

@users_blueprint.route('/<username>/profileimage', methods=["POST"])
def upload_image(username):
    user= User.get_or_none(User.username==username)
    if current_user == user:
        # A
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        # B
        file    = request.files["user_file"]

        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """

        # C.
        if file.filename == "":
            return "Please select a file"

        # D.
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file)

            #saving path to database(image_path)
            s= User.get_or_none(User.username==username)
            s.image_path= str(output[52:])
            s.save()

            flash("Sucessfully uploaded new profile picture", 'alert alert-success')
            return redirect(url_for('users.edit', username=current_user.username))
            

        else:
            return redirect(url_for('users.edit', username=current_user.username))
    else:
        flash('Please first sign up or login to your account.', 'alert alert-danger')
        return redirect(url_for('sessions.sign_in'))

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('users/profile.html')   

@users_blueprint.route('/<username>/userimage', methods=["POST"])
def upload_mainimage(username):
    user= User.get_or_none(User.username==username)
    if current_user == user:
        # A
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        # B
        file    = request.files["user_file"]

        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """

        # C.
        if file.filename == "":
            return "Please select a file"

        # D.
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file)

            #saving path to database(image_path)
            s= Images(images=str(output[52:]), user_id=current_user.id)
            s.save()

            flash("Sucessfully uploaded new picture!", 'alert alert-success')
            return redirect(url_for('users.show', username=current_user.username))
            

        else:
            return redirect(url_for('users.show', username=current_user.username))
    else:
        flash('Please first sign up or login to your account.', 'alert alert-danger')
        return redirect(url_for('sessions.sign_in'))

@users_blueprint.route('/users', methods=["GET"])
def display():
    # pass down database into the front end, dont call directly
    users = User.select()
    return render_template('users/users.html', users=users)

# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"



