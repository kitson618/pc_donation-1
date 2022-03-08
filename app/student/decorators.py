from functools import wraps
from flask import render_template
from flask_login import current_user


def is_student(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            if current_user.role == 'student' :
                return func(*args, **kwargs)
            else:
                raise
        except:
            # return render_template(url_for('main.index'))
            return render_template('errors/404.html'), 404

    return decorated_view



