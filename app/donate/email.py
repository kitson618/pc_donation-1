from flask import render_template
from flask_login import current_user
from app import azure_blob
from app.google_map import get_address_by_coordinates
from app.student.email import send_email
from webconfig import googlemap
import base64
import urllib.request


def send_to_student(location, item_record, stu_info):
    address = get_address_by_coordinates(googlemap.google_key, location[0], location[1])
    time = item_record.transaction_date, item_record.transaction_time
    # with open(os.path.abspath('app/static/donate_photo/' + item_record.photo), "rb") as img_file:
    #     donate_photo = base64.b64encode(img_file.read())
    # with open(azure_blob.get_img_url_with_blob_sas_token(blob_name='donate_photo/' + item_record.photo),
    #           "rb") as img_file:
    #     donate_photo = base64.b64encode(img_file.read())
    img_file = urllib.request.urlopen(
        azure_blob.get_img_url_with_blob_sas_token(blob_name='donate_photo/' + item_record.photo))
    donate_photo = base64.b64encode(img_file.read())
    html = render_template('donate/send_to_student.html', item_name=stu_info.item.item_name,
                           name=stu_info.user.full_name, date=time, address=address,
                           phone=current_user.phone_number, photo=donate_photo.decode('utf-8'),
                           item_record=item_record, key=googlemap.google_key)
    subject = "Congratulations you already have donors donating the items you need"
    send_email(stu_info.application.user.email, subject, html)
    pass


def send_to_donate(location, item_record):
    address = get_address_by_coordinates(googlemap.google_key, location[0], location[1])
    time = item_record.transaction_date, item_record.transaction_time
    # with open(os.path.abspath('app/static/donate_photo/' + item_record.photo), "rb") as img_file:
    #     donate_photo = base64.b64encode(img_file.read())
    # with open(azure_blob.get_img_url_with_blob_sas_token(blob_name='donate_photo/' + item_record.photo),
    #           "rb") as img_file:
    #     donate_photo = base64.b64encode(img_file.read())
    img_file = urllib.request.urlopen(
        azure_blob.get_img_url_with_blob_sas_token(blob_name='donate_photo/' + item_record.photo))
    donate_photo = base64.b64encode(img_file.read())
    html = render_template('donate/send_to_donate.html', item_name=item_record.item.item_name,
                           name=item_record.user.full_name, date=time, address=address,
                           photo=donate_photo.decode('utf-8'), item_record=item_record, key=googlemap.google_key)
    subject = "Congratulations you already have donors donating the items you need"
    send_email(item_record.user.email, subject, html)
    pass
