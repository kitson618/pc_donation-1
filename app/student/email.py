from flask import current_app, render_template
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import urllib.request
from app.email import send_email
from app import azure_blob, mail
import base64

# def send_password_reset_email(user):
#     token = user.get_reset_password_token()
#     send_email(_('[pc_donation] Reset Your Password'),
#                sender=current_app.config['ADMINS'][0],
#                recipients=[user.email],
#                text_body=render_template('email/reset_password.txt',
#                                          user=user, token=token),
#                html_body=render_template('email/reset_password.html',
#                                          user=user, token=token))


def generate_confirmation_item_token(userid):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(userid, salt=current_app.config['SECURITY_PASSWORD_SALT'])


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

# def send_to_student(message, item_name, photo,email):
#     img_file = urllib.request.urlopen(
#         azure_blob.get_img_url_with_blob_sas_token(blob_name="student/photo/" + photo))
#     photo = base64.b64encode(img_file.read())
#     html = render_template('student/email/thanks.html', message=message,item_name=item_name,photo=photo.decode('utf-8'))
#     subject = "Congratulations you already have donors donating the items you need"
#     send_email(email, subject, html)
#     pass