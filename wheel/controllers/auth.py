from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required, logout_user

from wheel.models import User
from wheel.forms import RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login(): 
    email = request.form['email']
    password = request.form['password']

    if email and password:
        success, message = User.login(email, password)
        flash( message, 'success' if success else 'danger')
            
    return redirect(url_for('index.get'))



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if (form.validate_on_submit()):
        name = form.name.data
        email = form.email.data
        password = form.password.data

        if not User.register(name, email, password):
            flash('User name already exists', 'danger')
            return redirect(url_for('auth.login'))

        flash('Thanks for registering! Please log in', 'success')
        return redirect(url_for('index.get'))

    return render_template('register.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.get'))