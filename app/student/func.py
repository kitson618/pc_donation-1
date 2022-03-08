from app.models import User
from app.student.email import confirm_token, send_email, generate_confirmation_item_token
from app import azure_blob
from flask import flash, session, url_for, render_template, request, redirect
from flask_login import current_user
from webconfig import ai_analyze
from app.models import Student
import requests
import os
from datetime import datetime
from flask_babel import _


def confirm_item(token):
    email = confirm_token(token)
    # if email is not False:
    #     item = Application.query.filter_by(user_id=email).order_by(Application.id.desc()).first_or_404()
    #     item.apply_status_id = 2
    #     item.status_id = 1
    #     db.session.add(item)
    #     db.session.commit()
    #     flash('You have approved your student\'s application . Thanks!', 'success')
    # else:
    #     flash('The confirmation link is invalid or has expired.', 'danger')
    return email


def send_confirm_item():
    email = Student.query.filter_by(user_username=session.get('username')).first()
    student = User.query.filter_by(username=session.get('username')).first()
    token = generate_confirmation_item_token(current_user.id)
    confirm_url = url_for('student.confirm_item_application', token=token, _external=True)
    html = render_template('student/email/confirm.html', confirm_url=confirm_url, name=student.full_name)
    subject = "Approve student application"
    send_email(email.teacher_email, subject, html)


def ai_check(photo, filename):
    if ai_analyze.subscription_key is not None and ai_analyze.endpoint is not None:
        analyze_url = ai_analyze.endpoint + "vision/v3.1/analyze"
        photo.save(os.path.abspath('app/static/student/photo/' + filename))
        azure_blob.save_image(blob_name="student/photo/" + filename,
                              file_path=os.path.abspath('app/static/student/photo/' + filename))
        os.remove(os.path.abspath('app/static/student/photo/' + filename))
        photo_path = azure_blob.get_img_url_with_blob_sas_token("student/photo/" + filename)
        print(photo_path)
        image_data = photo_path
        headers = {'Ocp-Apim-Subscription-Key': ai_analyze.subscription_key,
                   'Content-Type': 'application/json'}
        params = {'visualFeatures': 'Description,Adult'}
        data = {"url": image_data}
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        print(analysis)
        if analysis["adult"]["isAdultContent"]:
            # The photo cannot upload since it have wrong condition
            print("None")
            os.remove(photo_path)
            flash(_('Adult Content,Please upload right photo'))
            return False
        elif analysis["adult"]["isGoryContent"]:
            # The photo cannot upload since it have wrong condition
            print("None")
            os.remove(photo_path)
            flash(_('Gory Content,Please upload right photo'))
            return False
        elif analysis["adult"]["isRacyContent"]:
            # The photo cannot upload since it have wrong condition
            print("None")
            os.remove(photo_path)
            flash(_('Racy Content,Please upload right photo'))
            return False
    return True
