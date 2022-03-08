from flask import render_template
from flask_login import current_user
from functools import wraps


def is_teacher(func):
    @wraps(func)
    def teachers_view(*args, **kwargs):
        try:
            if current_user.role == 'teacher':
                return func(*args, **kwargs)
            else:
                raise
        except:
            return render_template('errors/404.html'), 404

    return teachers_view


def is_volunteer(func):
    @wraps(func)
    def volunteers_view(*args, **kwargs):
        try:
            if current_user.role == 'volunteer':
                return func(*args, **kwargs)
            else:
                raise
        except:
            return render_template('errors/404.html'), 404

    return volunteers_view
