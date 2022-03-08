from flask import current_app, render_template
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail

from app.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    text_body = render_template('email/reset_password.txt', user=user, token=token)
    html_body = render_template('email/reset_password.html', user=user, token=token)
    send_email(to=user.email, subject=_("iShare Reset Your Password"), template=html_body)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=604800):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
