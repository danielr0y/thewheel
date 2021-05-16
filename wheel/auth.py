from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def authenticate(): 
    email = request.form['email']
    password = request.form['password']

    if email and password:
        user = User.query.filter_by(email=email).first()
        error = None

        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'

        if error is not None:
            flash(error, 'danger')
        else:
            flash("welcome back", 'success')
            login_user(user)
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if (form.validate_on_submit()):
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User name already exists', 'danger')
            return redirect(url_for('auth.login'))

        pwd_hash = generate_password_hash(password)
        new_user = User(name=name, password_hash=pwd_hash, email=email)

        db.session.add(new_user)
        db.session.commit()

        flash('Thanks for registering! Please log in', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
