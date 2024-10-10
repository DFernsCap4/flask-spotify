import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.models import db, User

from werkzeug.security import check_password_hash, generate_password_hash

from wtforms import Form, StringField, PasswordField, validators

bp = Blueprint('auth', __name__, url_prefix='/auth')

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.length(min=5),
        validators.Regexp( r'^(?=.*[0-9])(?=.*[!@#$%^&*])',message="Password must contain at least one number and one special character.")]
        )

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password= request.form['password']
        user = User.query.get_or_404(username)
        error = None
        if user is None:
            error = "Incorrect username or password."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('song.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))