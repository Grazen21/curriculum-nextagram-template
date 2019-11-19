from flask import Blueprint, render_template, url_for, redirect, request, flash, session, escape, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User 
import re
from is_safe_url import is_safe_url
from instagram_web.util.google_oauth import oauth

from flask_login import login_user, logout_user, current_user, login_required

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


#create new blueprint in _int_.py

@sessions_blueprint.route('/sign_in', methods=['GET'])
def sign_in():
    return render_template('sessions/sign_in.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    username=request.form.get('username')
    password=request.form.get('password')
    verify_username= User.get_or_none(username==User.username)

    if verify_username:
        password_to_check = request.form['password'] # password keyed in by the user in the sign in form
        hashed_password = User.get(username==User.username).password # password hash stored in database for a specific user

        result = check_password_hash(hashed_password, password_to_check) # what is result? Test it in Flask shell and implement it in your view function!
        if result:
            # session["user_id"] = User.get(username==User.username).id # tells the browser to store `user.id` in session with the key as `user_id`
            #                              # then redirect them somewhere
            # flash("Succeed on login")
            # return redirect(url_for('sessions.sign_in'))
            login_user(verify_username)

            flash('Logged in successfully.', 'alert alert-success')

            return redirect(url_for('home'))
        else: 
            flash("Invalid Username or Password", 'alert alert-danger')
            return redirect(url_for('sessions.sign_in'))
    else: 
        flash("Invalid Username or Password", 'alert alert-danger')
        return redirect(url_for('sessions.sign_in'))


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

@sessions_blueprint.route('/', methods=["GET"])
def index():
    # if 'username' in session:
    #     return 'Logged in as %s' % escape(session['username'])
    # return 'You are not logged in'
    pass

@sessions_blueprint.route('/login/google', methods=["GET"])
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=["GET"])
def google_authorize():
    token = oauth.google.authorize_access_token()
    if not token:
        flash("Something went wrong, please try again", 'alert alert-danger')
        return redirect(url_for('home'))
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email==email)
    if not user:
        flash("Sorry, no account registered with this email", 'alert alert-danger')
        return redirect(url_for('home'))
    flash ("welcome back" , "alert alert-success")
    login_user(user)
    return redirect(url_for('home'))
        
    

# @sessions_blueprint.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

@sessions_blueprint.route("/logout", methods=["POST"])
# @login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'alert alert-success')
    return redirect(url_for('sessions.sign_in'))