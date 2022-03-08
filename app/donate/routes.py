from flask import redirect, url_for, flash, request, render_template, session
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import azure_blob, db
from app.azure_ai import textAnalytics, translate
from app.azure_ai.vision_analyze import vision_analyze
from app.donate import bp
from app.donate.email import send_to_student, send_to_donate
from app.donate.forms import DonateForm, ItemForm, SelectedItemForm, DonateDateForm, SelectedDonateDateForm
from app.donate.map import donate_filter_map
from app.form_helper import upload_to_azure_blob
from app.models import User, EquipmentType, Equipment, EquipmentApplication
from app.donate import index_data
import requests
from webconfig import googlemap, ai_chatbot, ai_analyze
from datetime import datetime
import os
import json
import random
from sqlalchemy import func

now = datetime.now()
current_time = now.strftime("%H_%M_%S")


def get_unique_donate_item_file_name(form):
    return current_user.username + '_' + current_time + '_' + str(
        random.randint(1, 100000)) + '_' + form.photo.data.filename


def populate_form_item_types(form):
    form.item.choices = [(s.id, _(s.item_name)) for s in db.session.query(EquipmentType).all()]


@bp.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = DonateForm()
    donations = db.session.query(DonateApplication).filter_by(user_id=current_user.id).all()
    populate_form_item_types(form)

    # TODO: fill form.item_Status.choices

    if form.validate_on_submit():

        filename = get_unique_donate_item_file_name(form)
        photo_path = upload_to_azure_blob(form, filename)
        image_error = vision_analyze(photo_path)

        if image_error is not None:
            flash(image_error)
            # TODO: check it as unknown old logic!
            return render_template('donate/donate.html', form=form, items=donations,
                                   image=azure_blob.get_img_url_with_blob_sas_token)

        donates = DonateApplication(item_id=form.item.data, item_status_id=form.item_Status.data, date=form.date,
                                    user_id=current_user.id, photo=filename, donate_status_id=1)

        db.session.add(donates)
        db.session.commit()
        flash(_('Your information add successful'))
        return redirect(url_for('donate.donate'))
    # if request.method == 'POST':
    #     del_form = request.form
    #     for ID in del_form.to_dict():
    #         record_id = ID
    #     del_service = db.session.query(Donate).filter_by(id=record_id).first()
    #     db.session.delete(del_service)
    #     db.session.commit()
    #     flash(_('Deleted'))
    #     return redirect(url_for('donate.donate'))
    return render_template('donate/donate.html', form=form, items=donations,
                           image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/donate_del', methods=['GET', 'POST'])
@login_required
def donate_del():
    if request.method == 'POST':
        del_form = request.form
        # TODO: Bug may be here!
        record_id = del_form.lists()[-1]
        del_service = db.session.query(DonateApplication).filter_by(id=record_id).first()
        db.session.delete(del_service)
        db.session.commit()
        flash(_('Deleted'))
        return redirect(url_for('donate.donate'))
    return redirect(url_for('donate.donate'))


@bp.route('/donate_view', methods=['GET', 'POST'])
@login_required
def donate_view():
    lang = str(get_locale())
    # TODO: Will need to support zh_TW
    category = lang == "zh" and index_data.CATEGORY_ZH or index_data.CATEGORY
    conf = index_data.conf
    donate_check = db.session.query(DonateApplication.id).filter_by(user_id=current_user.id).all()
    # donate_check = db.session.query(Donate.id).filter(Donate.user_id == current_user.id).all()
    if 'remindbox' not in session:
        if len(donate_check) == 0:
            session["remindbox"] = "donate_step1"
        else:
            session["remindbox"] = "donate_step2"
    else:
        if len(donate_check) == 0:
            session["remindbox"] = "donate_step1"
        else:
            session["remindbox"] = "donate_step2"
    return render_template('donate/donate_view.html', title=_('Donate View'), categorys=category, conf=conf,
                           key=ai_chatbot.donate_chatbot_key,
                           remindbox=session['remindbox'])


# This page use to show all donate record for the Donor
@bp.route('/donate_record', methods=['GET', 'POST'])
@login_required
def donate_record():
    services = db.session.query(DonateApplication).filter_by(user_id=current_user.id).all()
    return render_template('donate/donate_record.html', services=services, title=_('Donate record'),
                           image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/donate_story', methods=['GET', 'POST'])
@login_required
def donate_story():
    # TODO: Sam please remove outerjoin!
    apply = db.session.query(DonateApplication.title, Equipment.item_id, DonateApplication.id,
                             DonateApplication.created_at).filter(DonateApplication.apply_status_id == 2).order_by(
        DonateApplication.created_at).all()
    filter_name = db.session.query(EquipmentType.item_name, EquipmentType.id).all()

    # story_map = donate_map()
    stu_locations = db.session.query(Equipment).join(DonateApplication).filter_by(apply_status_id=2).order_by(
        DonateApplication.created_at).all()
    return render_template('donate/donate_story.html', title=_('Student story'), apply=apply, filter_name=filter_name,
                           key=googlemap.google_key, stu_locations=stu_locations)


# TODO: Rewrite the map logic
#
# @bp.route('/getdata', methods=['GET', 'POST'])
# @login_required
# def getdata():
#     from_lat = request.values.get('fromLat')
#     to_lat = request.values.get('toLat')
#     from_lng = request.values.get('fromLng')
#     to_lng = request.values.get('toLng')
#     item_id = request.values.get('item_id')
#     if item_id != "":
#         stu_locations = db.session.query(ApplicationItem).join(Application).filter_by(apply_status_id=2).join(
#             ItemType).filter_by(id=item_id).join(StuMap).filter(StuMap.latitude >= from_lat,
#                                                                 StuMap.latitude <= to_lat).filter(
#             StuMap.longitude >= from_lng, StuMap.longitude <= to_lng).order_by(Application.created_at).all()
#     else:
#         stu_locations = db.session.query(ApplicationItem).join(Application).filter_by(apply_status_id=2).join(
#             StuMap).filter(StuMap.latitude >= from_lat, StuMap.latitude <= to_lat).filter(
#             StuMap.longitude >= from_lng, StuMap.longitude <= to_lng).order_by(Application.created_at).all()
#     marker = [(loc.application.title, loc.application.stu_location.latitude, loc.application.stu_location.longitude,
#                render_template('donate/stumap_infobox.html', title=_('stu_info'), loc=loc,
#                                image=azure_blob.get_img_url_with_blob_sas_token))
#               for loc in stu_locations]
#     # print(marker)
#     return json.dumps(marker)


@bp.route('/donate_story/<item_id>', methods=['GET', 'POST'])
@login_required
def donate_story_item(item_id):
    # TODO: Sam please remove outer join!
    apply = db.seesion.query(DonateApplication.title, Equipment.item_id, DonateApplication.id,
                             DonateApplication.created_at).filter(
        DonateApplication.apply_status_id == 2).filter(EquipmentType.id == item_id).order_by(
        DonateApplication.created_at).all()
    filter_name = db.session.query(EquipmentType.item_name, EquipmentType.id).all()
    story_map = donate_filter_map(item_id)
    stu_locations = db.session.query(Equipment).join(DonateApplication).filter_by(apply_status_id=2).join(
        EquipmentType).filter_by(id=item_id).order_by(DonateApplication.created_at).all()
    return render_template('donate/donate_story.html', title=_('Student story'), apply=apply, filter_name=filter_name,
                           story_map=story_map, stu_locations=stu_locations, key=googlemap.google_key)


@bp.route('/donate_story/details/<data_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def donate_detail(data_id, item_id):
    have_donate = False
    story = db.session.query(Equipment).filter_by(application_id=data_id, item_id=item_id).first()
    content = translate.ai_translate(story.application.story)[2]
    # TODO: Move to model events
    textAnalytics.sentiment_analysis_example(textAnalytics.authenticate_client(), content)
    textAnalytics.key_phrase_extraction_example(textAnalytics.authenticate_client(), content)
    # have_donate = db.session.query(Donate.item_id == applicationItem.item_id).filter_by(
    #     user_id=current_user.id).filter(applicationItem.application_id == story.id).scalar()
    donate_check = db.session.query(DonateApplication).filter_by(user_id=current_user.id, donate_status_id=1).all()
    # loop all item in donate to check whether they have that item
    for check in donate_check:
        if story.item_id == check.item_id:
            have_donate = True
    return render_template('donate/show_story.html', title=_('Story'), story=story, have_donate=have_donate)


# next page of donate story
@bp.route('/donate_item/<data_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def donate_item(data_id, item_id):
    # search any item the Donor selected
    # TODO: STATUS removes 2. What is 2?
    search = db.session.query(DonateApplication).filter_by(application_id=data_id, item_id=item_id,
                                                           donate_status_id=2).all()
    default = User.query.filter_by(role="default").first()
    service = db.session.query(Equipment).filter_by(application_id=data_id, item_id=item_id).first()
    donate_file = None
    if len(search) != 0:
        form = SelectedItemForm()
        donate_list = search
        for file in search:
            donate_file = azure_blob.get_img_url_with_blob_sas_token(blob_name="donate_photo/" + file.photo)
    else:
        form = ItemForm()
        # filter the item which the Donor still not donate
        donate_list = db.session.query(DonateApplication).filter_by(user_id=current_user.id, item_id=item_id,
                                                                    donate_status_id=1).all()
        donate_st = db.session.query(DonateApplication).filter_by(user_id=current_user.id, item_id=item_id,
                                                                  donate_status_id=1).first()
        if donate_st is None:
            donate_file = None
        else:
            donate_file = azure_blob.get_img_url_with_blob_sas_token(blob_name="donate_photo/" + donate_st.photo)
    # donate_file = db.session.query(Donate.photo).filter_by(user_id=current_user.id).scalar()
    # form.item.choices = [
    #     ("donate_photo/" + s.photo, s.item.item_name) for s in
    #     donate_list]
    # print(donate_list)
    form.item.choices = [
        (azure_blob.get_img_url_with_blob_sas_token(blob_name="donate_photo/" + s.photo), s.item.item_name) for s in
        donate_list]

    if form.item.data and form.is_submitted():
        chosen_item_photo = os.path.basename(form.item.data.split("?se=")[0])
        print(chosen_item_photo)
        chosen_item = db.session.query(DonateApplication).filter_by(photo=chosen_item_photo).first()
        print(chosen_item)
        chosen_item.donate_status_id = 2
        chosen_item.application_id = data_id
        service.donor_id = current_user.id
        db.session.commit()
        flash(_('Your information add successful'))
        return redirect(url_for('donate.donate_item', data_id=data_id, item_id=item_id))
    if request.method == 'POST':
        print(type(form.item.data))
        print(form.item.data)
        for record in search:
            record.donate_status_id = 1
            record.application_id = None
        service.donor_id = default.id  # This can be None
        db.session.commit()
        flash(_('Cancelled'))
        return redirect(url_for('donate.donate_item', data_id=data_id, item_id=item_id))
    return render_template('donate/donate_item.html', service=service, form=form, data_id=data_id, default=default.id,
                           item_id=item_id, donate_file=donate_file, search=search, check_photo=len(form.item.choices),
                           image=azure_blob.get_img_url_with_blob_sas_token)


# next page of donate item
@bp.route('/donate_date/<data_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def donate_date(data_id, item_id):
    record = db.session.query(DonateApplication).filter_by(user_id=current_user.id, application_id=data_id,
                                                           item_id=item_id).first()
    # check whether the user input the transaction date and time
    if record.transaction_date is None and record.transaction_time is None:
        form = DonateDateForm()
        if form.is_submitted():
            record.transaction_date = request.form.get('transaction_date')
            record.transaction_time = request.form.get('transaction_time')
            db.session.commit()
            flash(_('Your information add successful'))
            return redirect(url_for('donate.donate_date', data_id=data_id, item_id=item_id))
    else:
        form = SelectedDonateDateForm()
        # showing the transaction date and time into the webpage
        form.transaction_date.data = datetime.strptime(record.transaction_date, "%Y-%m-%d").date()
        form.transaction_time.data = datetime.strptime(record.transaction_time, "%H:%M").time()
        if form.is_submitted():
            record.transaction_date = None
            record.transaction_time = None
            db.session.commit()
            flash(_('Cancelled'))
            return redirect(url_for('donate.donate_date', data_id=data_id, item_id=item_id))
    return render_template('donate/donate_date.html', form=form, data_id=data_id, item_id=item_id, record=record)


# final step of donor to donate (choose location)
@bp.route('/donate_location/<data_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def donate_location(data_id, item_id):
    ser = db.session.query(Equipment).filter_by(application_id=data_id, item_id=item_id).first()
    if request.method == 'POST':
        print(data_id + "abc" + item_id + "XD")
    return render_template('donate/donate_location.html', title=_('map'), ser=ser, key=googlemap.google_key,
                           data_id=data_id, item_id=item_id)


@bp.route('/back_and_cancel', methods=['GET', 'POST'])
@login_required
def back_and_cancel():
    default = User.query.filter_by(role="default").first()
    if request.method == 'POST':
        data_id = request.values.get('stu_id')
        item_id = request.values.get('stu_item')
        services = db.session.query(Equipment).filter_by(application_id=data_id, item_id=item_id).first()
        item_record = db.session.query(DonateApplication).filter_by(user_id=current_user.id, item_id=item_id,
                                                                    donate_status_id=2).first()
        if services.donor_id == current_user.id:
            services.donor_id = default.id
            item_record.donate_status_id = 1
            item_record.application_id = None
            item_record.transaction_date = None
            item_record.transaction_time = None
            db.session.commit()
        return redirect(url_for('donate.donate_detail', data_id=data_id, item_id=item_id))


@bp.route('/donate_submit', methods=['GET', 'POST'])
@login_required
def donate_submit():
    if request.method == 'POST':
        location = request.form["location"].split(",")
        data_id = request.values.get('stu_id')
        item_id = request.values.get('stu_item')
        item_record = db.session.query(DonateApplication).filter_by(user_id=current_user.id, application_id=data_id,
                                                                    item_id=item_id).first()
        stu_info = db.session.query(Equipment).filter_by(application_id=data_id, item_id=item_id).first()
        item_record.latitude = location[0]
        item_record.longitude = location[1]
        send_to_student(location=location, item_record=item_record, stu_info=stu_info)
        send_to_donate(location=location, item_record=item_record)
        item_record.donate_status_id = 3
        stu_info.application.apply_status_id = 5
        msg_check = db.session.query(func.max(User.chatroom)).first()
        if msg_check[0] is None:
            msgroom_status = MessageRoom(room_id=1, message="Welcome", timestamp=datetime.now())
            # db.session.add(msgroom)
            room_id = 1
        else:
            room_id = msg_check[0] + 1
            msgroom_status = MessageRoom(room_id=room_id, message="Welcome", timestamp=datetime.now())
        db.session.add(msgroom_status)
        donor_record = db.session.query(User).filter_by(id=current_user.id).first()
        donor_record.chatroom = room_id
        student_record = db.session.query(User).filter_by(id=stu_info.application.user_id).first()
        student_record.chatroom = room_id
        db.session.commit()
        flash(_('You are successful donate to this student'))

        return redirect(url_for('donate.donate_view'))


@bp.route('/msg', methods=['GET', 'POST'])
@login_required
def msg():
    msg_record = db.session.query(User).filter_by(id=current_user.id).first()
    if msg_record.chatroom is None:
        donateItem = None
    else:
        donateItem = db.session.query(MessageRoom).filter_by(room_id=msg_record.chatroom).order_by(
            MessageRoom.timestamp.desc()).first()
        user_status = db.session.query(User).filter_by(chatroom=msg_record.chatroom, role="student").first()
    return render_template('messageList.html', title=_('Message List'), donateItem=donateItem, userStatus=user_status)


@bp.route('/msgbox/<msg_id>', methods=['GET', 'POST'])
@login_required
def msgbox(msg_id):
    msg_record = db.session.query(User).filter_by(id=current_user.id).first()

    if msg_record.chatroom == int(msg_id):
        donateItem = db.session.query(MessageRoom).filter_by(room_id=msg_id).all()
        if request.method == 'POST':
            msg = request.form["msg"]
            msgroom_status = MessageRoom(room_id=msg_id, message=msg, timestamp=datetime.now())
            db.session.add(msgroom_status)
            db.session.commit()
            return redirect(url_for('donate.msgbox', msg_id=msg_id))
    else:
        flash(_('Wrong chat room!'))
        return redirect(url_for('main.index'))
    return render_template('message.html', title=_('Message'), donateItem=donateItem, msg_id=msg_id)
