from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from wheel.models import User

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    if id == current_user.id:
        flash(f'Cannot delete account that is logged in.', 'danger')
        return redirect( url_for('accounts.get'))

    User.delete(id)

    flash(f'Successfully deleted account', 'success')
    return redirect( url_for('accounts.get') )



@accounts.route('/<int:id>/admin', methods=['GET', 'POST'])
@login_required
def admin(id):
    User.makeAdmin(id)

    flash(f'Successfully made account an administrator', 'success')
    return redirect( url_for('accounts.get') )



@accounts.route('/')
@login_required
def get():
    users = User.query.all()

    return render_template('accounts.html', users=users)