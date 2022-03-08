import os

from flask import redirect, url_for, flash, request, render_template, session, jsonify
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from app import azure_blob, db
from app.student import bp
from app.student.decorators import is_student
from app.student.forms import ThankMessageForm, RepairForm, ApplyStoryForm, \
    TestApplyForm, ThankToDonorForm, ThankToVolunteerForm, DateForm, WindowApply
from app.models import Student, User, EquipmentType, Equipment, RepairApplication, EquipmentApplication

from app.student import index_data
from datetime import datetime
from app.student.email import confirm_token, send_email, generate_confirmation_item_token
from app.student.func import confirm_item, send_confirm_item, ai_check
from dateutil.parser import parse
import base64
from webconfig import googlemap, ai_chatbot
import urllib.request

now = datetime.now()
current_time = now.strftime("%H_%M_%S")


# @bp.route('/first_story', methods=['GET', 'POST'])
# @login_required
# def first_story():
#     form = applyStory_Form()
#     return render_template('student/firststory.html', title=_('First Story'), form=form, backId=0)
#
#
# @bp.route('/edit_story', methods=['GET', 'POST'])
# @login_required
# def edit_story():
#     form = applyStory_Form()
#     return render_template('student/firststory.html', title=_('Edit Story'), form=form, backId=1)

# windowApply
@bp.route('/windows_apply', methods=['GET', 'POST'])
@login_required
def windows_apply():
    form = WindowApply()
    if form.validate_on_submit():
        print(form.need.data)

    return render_template('student/windows.html', title=_('Windows Apply'), form=form)


@bp.route('/map/', methods=['GET', 'POST'])
@login_required
@is_student
def stu_map():
    return render_template('student/map.html', title=_('map'), map=map, key=googlemap.google_key)


@bp.route('/map2/', methods=['GET', 'POST'])
@login_required
@is_student
def map2():
    if request.method == 'POST':
        a = db.session.query(Application).filter_by(user=current_user).order_by(Application.id.desc()).first()
        location = request.form["location"].split(",")
        l = StuMap(application_id=a.id, latitude=location[0], longitude=location[1])
        db.session.add(l)
        db.session.commit()
        # flash(get_address(googlemap.google_key, location[0], location[1]))
        return redirect(url_for('student.send_to_teacher'))
    return render_template('student/map.html', title=_('map'), map=map, key=googlemap.google_key)


@bp.route('/dateconfirm-repair', methods=['GET', 'POST'])
@login_required
@is_student
def dateconfirmrepair():
    return render_template('student/repair_time.html', title=_('Date confirm'))


@bp.route('/send_to_volunteer', methods=['GET', 'POST'])
def send_ok_to_volunteer():
    application = db.session.query(RepairApplication).filter_by(user_id=current_user.id, apply_status_id=5).order_by(
        RepairApplication.id.desc()).first()
    volunteer = db.session.query(User).filter_by(id=application.volunteer_id).first()
    student = db.session.query(User).filter_by(id=current_user.id).first()
    if request.method == 'POST':
        html = render_template('student/email/oktime.html', phone=student.phone_number)
        subject = "Thanks for your repair"
        send_email(volunteer.email, subject, html)
        application.apply_status_id = 7
        db.session.commit()
    return redirect(url_for('student.student_view'))


@bp.route('/cancelrepair', methods=['GET', 'POST'])
def cancelrepair():
    application = db.session.query(RepairApplication).filter_by(user_id=current_user.id, apply_status_id=5).order_by(
        RepairApplication.id.desc()).first()
    if request.method == 'POST':
        application.apply_status_id = 1
        application.volunteer_id = 1
        db.session.commit()
    return redirect(url_for('student.student_view'))


@bp.route('/dateconfirm', methods=['GET', 'POST'])
@login_required
@is_student
def dateconfirm():
    return render_template('student/dateconfirm.html', title=_('Date confirm'))


@bp.route('/cancel', methods=['GET', 'POST'])
def cancel():
    application = db.session.query(Application).filter_by(user_id=current_user.id).order_by(
        Application.id.desc()).first()
    cancelitem = db.session.query(Equipment).filter(Equipment.application_id == application.id,
                                                    Equipment.donor_id != 1,
                                                    Equipment.obtained_id == 1).all()
    if request.method == 'POST':
        application.apply_status_id = 2
        for i in cancelitem:
            i.donator_id = 1
        db.session.commit()
    return redirect(url_for('student.student_view'))


@bp.route('/send_to_donator', methods=['GET', 'POST'])
def send_ok_to_donator():
    item = db.session.query(Application).filter_by(user_id=current_user.id).order_by(Application.id.desc()).first()
    email = db.session.query(Equipment).filter(Equipment.application_id == item.id,
                                               Equipment.donor_id != 1,
                                               Equipment.obtained_id == 1).first()
    donator = db.session.query(User).filter_by(id=email.donor_id).first()
    student = db.session.query(User).filter_by(id=current_user.id).first()
    # loc = db.session.query(stuMap).filter_by(application_id=item.id).order_by(stuMap.id.desc()).first()
    if request.method == 'POST':
        print(item.id)
        print(email.donator_id)
        html = render_template('student/email/oktime.html', phone=student.phone_number)
        subject = "Thanks for your donation"
        send_email(donator.email, subject, html)
        item.apply_status_id = 3
        db.session.commit()
    return redirect(url_for('student.student_view'))


@bp.route('/student_view', methods=['GET', 'POST'])
@login_required
@is_student
def student_view():
    lang = str(get_locale())
    categorys = lang == "zh" and index_data.categorys_zh or index_data.categorys
    stepcheck = db.session.query(Application).filter_by(user_id=current_user.id).order_by(Application.id.desc()).count()
    print(stepcheck)
    if stepcheck == 0:
        session["remindbox"] = "stu_step1"
    elif stepcheck != 0:
        s = db.session.query(Application).filter_by(user_id=current_user.id).order_by(Application.id.desc()).first()
        if s.apply_status_id == 2:
            session["remindbox"] = "stu_step2"
        elif s.apply_status_id == 3:
            session["remindbox"] = "stu_step3"
        elif s.apply_status_id == 4:
            session["remindbox"] = "stu_step1"
    if 'remindbox' in session:
        remindbox = session['remindbox']
        print(remindbox)
    # else:
    #     session["remindbox"] = "stu_step1"
    return render_template('student/student_view.html', title=_('Student View'), categorys=categorys, lang=lang,
                           key=ai_chatbot.student_chatbot_key)


@bp.route('/checkstory/', methods=['GET', 'POST'])
@login_required
@is_student
def checkstory():
    applicationCount = db.session.query(Application).filter_by(user=current_user).count()
    if applicationCount == 0:
        return redirect(url_for('student.application_story'))
    elif applicationCount != 0:
        applicationTime = db.session.query(Application).filter_by(user=current_user).order_by(
            Application.id.desc()).first()
        timeCheck = datetime.now() - datetime.strptime(applicationTime.idtime, "%Y-%m-%d %H:%M:%S")
        if applicationTime.apply_status_id == 6:
            if timeCheck.days < 30:
                flash(_('Each time the application was rejected, Need after 30 days apart to be able to re-apply'))
                return redirect(url_for('student.student_view'))
        elif timeCheck.days < 180:
            flash(_('Each application needs to be at least 180 days apart'))
            return redirect(url_for('student.student_view'))
    if request.method == 'POST':
        old_story = db.session.query(Application).filter_by(user_id=current_user.id).order_by(
            Application.id.desc()).first()
        applications = Application(title=old_story.title, story=old_story.story,
                                   user=current_user, apply_status_id=8,
                                   apply_photo=old_story.apply_photo,
                                   idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(applications)
        db.session.commit()
        return redirect(url_for('student.item_application'))
    return render_template('student/checkstory.html', title=_('Change Story'))


@bp.route('/application_story', methods=['GET', 'POST'])
@login_required
@is_student
def application_story():
    applicationCount = db.session.query(Application).filter_by(user=current_user).count()
    if applicationCount != 0:
        applicationCheck = db.session.query(Application).filter_by(user=current_user).order_by(
            Application.id.desc()).first()
        if applicationCheck.apply_status_id == 8:
            return redirect(url_for('student.draft', data_id=applicationCheck.id))
    #     timeCheck = datetime.now() - datetime.strptime(applicationTime.idtime, "%Y-%m-%d %H:%M:%S")
    #     if applicationTime.apply_status_id == 6:
    #         if timeCheck.days < 30:
    #             flash(_('Each time the application was rejected, Need after 30 days apart to be able to re-apply'))
    #             return redirect(url_for('student.student_view'))
    #     elif timeCheck.days < 180:
    #         flash(_('Each application needs to be at least 180 days apart'))
    #         return redirect(url_for('student.student_view'))
    form = ApplyStoryForm()
    flash(_('Press submit your Item application will be created'))
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + form.photo.data.filename
        # # form.photo.data.save('/mnt/share1/pictures/' + filename)
        if ai_check(form.photo.data, filename) == True:
            applications = Application(title=form.title.data, story=form.your_story.data,
                                       user=current_user, apply_status_id=8,
                                       apply_photo=filename, idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(applications)
            db.session.commit()
            return redirect(url_for('student.item_application'))
    return render_template('student/application.html', title=_('Item Application'), form=form)


@bp.route('/item_application', methods=['GET', 'POST'])
@login_required
@is_student
def item_application():
    default = db.session.query(User).filter_by(role="default").first()
    form = TestApplyForm()
    app = db.session.query(Application).filter(Application.user_id == current_user.id).order_by(
        Application.id.desc()).first()
    items = db.session.query(Equipment).filter_by(application_id=app.id).all()
    form.item.choices = [(s.id, s.item_name) for s in db.session.query(EquipmentType).all()]
    if form.validate_on_submit():
        a = Equipment(item_id=form.item.data, quantity=form.quantity.data,
                      application_id=app.id, obtained_id=form.obtained.data, donator_id=default.id)
        check = db.session.query(Equipment).filter_by(item_id=a.item_id, application_id=app.id).count()
        total = db.session.query(Equipment).filter_by(application_id=app.id).count()
        desktop = db.session.query(Equipment).filter_by(item_id=1, application_id=app.id).count()
        labtop = db.session.query(Equipment).filter_by(item_id=2, application_id=app.id).count()
        if form.item.data == 2:
            if desktop == 1:
                flash(_('You can only select one type of computer'))
                return redirect(url_for('student.item_application'))
        if form.item.data == 1:
            if labtop == 1:
                flash(_('You can only select one type of computer'))
                return redirect(url_for('student.item_application'))
        if check >= 1:
            flash(_('Each item can only be selected once'))
            return redirect(url_for('student.item_application'))
        if total >= 2:
            flash(_('Only two items can be selected for each application'))
            return redirect(url_for('student.item_application'))
        db.session.add(a)
        db.session.commit()
        flash(_('Added'))
        return redirect(url_for('student.item_application'))
    if request.method == 'POST':
        del_form = request.form
        for ID in del_form.to_dict():
            record_id = ID
        del_items = db.session.query(Equipment).filter_by(id=record_id).first()
        db.session.query(Equipment).filter_by(application_id=int(del_items.application_id),
                                              item_id=int(del_items.item_id)).delete()
        db.session.commit()
        flash(_('Deleted'))
        return redirect(url_for('student.item_application'))
    return render_template('student/item_application.html', title=_('Item Application'), form=form, items=items,
                           test1=app)


@bp.route('/send_to_teacher', methods=['GET', 'POST'])
def send_to_teacher():
    if request.method == 'POST' or request.method == 'GET':
        send_confirm_item()
        app = db.session.query(Application).filter_by(user_id=current_user.id).order_by(
            Application.id.desc()).first()
        # TODO apply status id romoves 1. what is 1
        app.apply_status_id = 1
        db.session.commit()
    flash(_('Application has been submitted to the teacher'))
    return redirect(url_for('student.student_view'))


@bp.route('/apply_repair', methods=['GET', 'POST'])
@login_required
@is_student
def apply_repair():
    default = db.session.query(User).filter_by(role="default").first()
    form = RepairForm()
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + '_repair_' + form.photo.data.filename
        description = RepairApplication(title=form.title.data, description=form.description.data,
                                        user_id=current_user.id, apply_repair_photo=filename,
                                        idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        address=form.address.data, volunteer_id=default.id, apply_status_id=1)
        if ai_check(form.photo.data, filename) == True:
            db.session.add(description)
            db.session.commit()
            flash(_('Your application has been accepted !'))
            return redirect(url_for('student.student_view'))
    return render_template('student/application.html', title=_('Repair Application'), form=form, youtube='Repair')


@bp.route('/application_history', methods=['GET', 'POST'])
@login_required
@is_student
def application_history():
    apply = db.session.query(Application).filter_by(user=current_user).order_by(Application.id.desc()).all()
    return render_template('student/application_history.html', title=_('Application History'), apply=apply)


@bp.route('/application_history/draft/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def draft(data_id):
    story = db.session.query(Application).filter_by(id=data_id).first()
    if story.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    items = db.session.query(Equipment).outerjoin(ItemObtain,
                                                  Equipment.obtained_id == ItemObtain.id).outerjoin(
        EquipmentType,
        Equipment.item_id == EquipmentType.id).filter(
        Equipment.application_id == data_id).all()
    itemsCheck = db.session.query(Equipment).filter_by(application_id=data_id).count()
    mapCheck = db.session.query(StuMap).filter_by(application_id=data_id).count()
    if itemsCheck or mapCheck == 0:
        allCheck = False
    else:
        allCheck = True
    print(allCheck)
    return render_template('student/draft.html', title=_('Draft'), story=story, items=items, itemsCheck=itemsCheck,
                           mapCheck=mapCheck, image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/application_history/details/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def details_story(data_id):
    default = db.session.query(User).filter_by(role="default").first()
    number = default.id
    story = db.session.query(Application).filter_by(id=data_id).first()
    items = db.session.query(Equipment).outerjoin(ItemObtain,
                                                  Equipment.obtained_id == ItemObtain.id).outerjoin(
        EquipmentType,
        Equipment.item_id == EquipmentType.id).filter(
        Equipment.application_id == data_id).all()
    obtained_check = db.session.query(Equipment).filter(Equipment.application_id == data_id,
                                                        Equipment.obtained_id == 2).count()
    total_check = db.session.query(Equipment).filter(Equipment.application_id == data_id).count()
    donate_check = db.session.query(Equipment).filter(Equipment.application_id == data_id,
                                                      Equipment.donor_id != default.id).count()
    # print("obtained_check:", obtained_check)
    # print("total_check:", total_check)
    # print("donate_check:", donate_check)
    if story.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    if story.apply_status_id != 1:
        if total_check != 0:
            if obtained_check == total_check:
                story.apply_status_id = 4
                db.session.commit()
            elif donate_check < total_check:
                if donate_check == obtained_check:
                    story.apply_status_id = 2
                    db.session.commit()
    return render_template('student/show_story.html', title=_('Application History'), story=story, items=items,
                           obtained_check=obtained_check, number=number, total_check=total_check,
                           image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/send_thanks', methods=['GET', 'POST'])
def send_thanks():
    if request.method == 'POST':
        item = request.form.get("Obtained")
        obtained_items = db.session.query(Equipment).filter_by(id=item).first()
        return redirect(
            url_for('student.thankyou', application_id=obtained_items.application_id, order_id=obtained_items.id))


@bp.route('/application_history/edit_title/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def edit_title(data_id):
    form = ApplyStoryForm()
    change_story = db.session.query(Application).filter_by(id=data_id).first()
    # 加咗改唔到data
    # form.title.data = change_story.title
    # form.your_story.data = change_story.story
    if change_story.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + '_apply_' + form.photo.data.filename
        change_story.title = form.title.data
        change_story.story = form.your_story.data
        change_story.apply_photo = filename
        if ai_check(form.photo.data, filename) == True:
            # form.photo.data.save('/mnt/share1/pictures/' + filename)
            db.session.commit()
            flash(_('Updated'))
            return redirect(url_for('student.application_history'))
    return render_template('student/editapplication.html', title=_('Edit Title And Story'), form=form,
                           change_story=change_story, data_id=data_id, image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/application_history/edit_item/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def edit_item(data_id):
    default = db.session.query(User).filter_by(role="default").first()
    testid = int(data_id)
    form = TestApplyForm()
    application = db.session.query(Application.apply_status_id).filter_by(id=data_id).first()
    items = db.session.query(Equipment).filter_by(application_id=data_id).all()
    form.item.choices = [(s.id, s.item_name) for s in db.session.query(EquipmentType).all()]
    change_story = db.session.query(Application).filter_by(id=data_id).first()
    if change_story.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    if form.validate_on_submit():
        item = Equipment(item_id=form.item.data, quantity=form.quantity.data,
                         application_id=data_id, obtained_id=1, donator_id=default.id)
        check = db.session.query(Equipment).filter_by(item_id=item.item_id, application_id=data_id).count()
        total = db.session.query(Equipment).filter_by(application_id=data_id).count()
        desktop = db.session.query(Equipment).filter_by(item_id=1, application_id=data_id).count()
        labtop = db.session.query(Equipment).filter_by(item_id=2, application_id=data_id).count()
        if total >= 2:
            flash(_('Only two items can be selected for each application'))
            return redirect(url_for('student.edit_item', data_id=data_id))
        if form.item.data == 2:
            if desktop == 1:
                flash(_('You can only select one type of computer'))
                return redirect(url_for('student.edit_item', data_id=data_id))
        if form.item.data == 1:
            if labtop == 1:
                flash(_('You can only select one type of computer'))
                return redirect(url_for('student.edit_item', data_id=data_id))
        if check >= 1:
            flash(_('Each item can only be selected once'))
            return redirect(url_for('student.edit_item', data_id=data_id))
        db.session.add(item)
        db.session.commit()
        flash(_('Updated'))
        return redirect(url_for('student.edit_item', data_id=data_id))
    if request.method == 'POST':
        del_form = request.form
        for ID in del_form.to_dict():
            record_id = ID
        del_items = db.session.query(Equipment).filter_by(id=record_id).first()
        db.session.query(Equipment).filter_by(application_id=int(del_items.application_id),
                                              item_id=int(del_items.item_id)).delete()
        db.session.commit()
        flash(_('Deleted'))
        return redirect(url_for('student.edit_item', data_id=data_id))
    return render_template('student/edit_item.html', form=form, items=items, data_id=data_id, application=application)


@bp.route('/edit_map/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def edit_map(data_id):
    change_story = db.session.query(Application).filter_by(id=data_id).first()
    if change_story.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    checkmap = db.session.query(StuMap).filter_by(application_id=data_id).count()
    if checkmap == 1:
        return render_template('student/editmap.html', title=_('map'), map=map, key=googlemap.google_key,
                               data_id=data_id, mapCreated=1)
    else:
        return render_template('student/editmap.html', title=_('map'), map=map, key=googlemap.google_key,
                               data_id=data_id, mapCreated=0)


@bp.route('/edit_map2/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def edit_map2(data_id):
    if request.method == 'POST':
        # a = db.session.query(Application).filter_by(user=current_user).order_by(Application.id.desc()).first()
        location = request.form["location"].split(",")
        l = db.session.query(StuMap).filter_by(application_id=data_id).first()
        l.latitude = location[0]
        l.longitude = location[1]
        db.session.commit()
        return redirect(url_for('student.details_story', data_id=data_id))
    return render_template('student/map.html', title=_('map'), map=map, key=googlemap.google_key)


@bp.route('/repair_history', methods=['GET', 'POST'])
@login_required
@is_student
def repair_history():
    apply = db.session.query(RepairApplication).filter_by(user=current_user).order_by(RepairApplication.id.desc()).all()
    return render_template('student/repair_history.html', title=_('Repair History'), apply=apply)


@bp.route('/repair_history/details/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def repair_details(data_id):
    repair = db.session.query(RepairApplication).filter_by(id=data_id).first()
    if repair.user_id != current_user.id:
        return render_template('errors/404.html'), 404

    return render_template('student/show_repair.html', title=_('Application History'), repair=repair,
                           image=azure_blob.get_img_url_with_blob_sas_token)


@bp.route('/send_repairthanks', methods=['GET', 'POST'])
def send_repairthanks():
    if request.method == 'POST':
        repair_id = request.form.get("repair")
        print(repair_id)
        return redirect(url_for('student.thankyou_repair', data_id=repair_id))


@bp.route('/repair_history/edit_problem/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def edit_problem(data_id):
    form = RepairForm()
    edit_problem = db.session.query(RepairApplication).filter_by(id=data_id).first()
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + '_repair_' + form.photo.data.filename
        edit_problem.title = form.title.data
        edit_problem.story = form.description.data
        edit_problem.apply_photo = filename
        if ai_check(form.photo.data, filename) == True:
            # form.photo.data.save('/mnt/share1/pictures/' + filename)
            db.session.commit()
            flash(_('Updated'))
            return redirect(url_for('student.repair_history'))
    return render_template('student/application.html', title=_('Edit Problem'), form=form,
                           edit_problem=edit_problem)


@bp.route('/thankyou/<application_id>/<order_id>', methods=['GET', 'POST'])
@login_required
@is_student
def thankyou(application_id, order_id):
    # default = db.session.query(User).filter_by(role="default").first()
    form = ThankToDonorForm()
    # application = db.session.query(Application).filter_by(id=application_id).first()
    item = db.session.query(Equipment).filter_by(id=order_id).first()
    name = db.session.query(EquipmentType).filter_by(id=item.item_id).first()
    donator = db.session.query(User).filter_by(id=item.donor_id).first()
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + '_think_you_' + form.photo.data.filename
        thankyou = ThanksMessage(message_to_Donor=form.message_to_Donor.data,
                                 thanks_photo=filename, user=current_user, application_type='Item',
                                 application_id=application_id
                                 )
        if ai_check(form.photo.data, filename) == True:
            img_file = urllib.request.urlopen(
                azure_blob.get_img_url_with_blob_sas_token(blob_name="student/photo/" + filename))
            thank_photo = base64.b64encode(img_file.read())
            html = render_template('student/email/thanks.html', message=form.message_to_Donor.data,
                                   item_name=name.item_name,
                                   image=azure_blob.get_img_url_with_blob_sas_token("student/photo/" + filename),
                                   photo=thank_photo.decode('utf-8')
                                   )
            subject = "Thanks for your donation"
            send_email(donator.email, subject, html)
            # send_email("190320056@stu.vtc.edu.hk", subject, html)
            item.obtained_id = 2
            db.session.add(thankyou)
            db.session.commit()
            flash(_('Thank You For Your Message'))
            return redirect(url_for('student.details_story', data_id=item.application_id))
    return render_template('student/thankyou.html', title=_('Thank You'), form=form)


@bp.route('/thankyou_repair/<data_id>', methods=['GET', 'POST'])
@login_required
@is_student
def thankyou_repair(data_id):
    print(data_id)
    form = ThankToVolunteerForm()
    application = db.session.query(RepairApplication).filter_by(id=data_id).first()
    volunteer = db.session.query(User).filter_by(id=application.volunteer_id).first()
    if form.validate_on_submit():
        filename = current_user.username + '_' + current_time + form.photo.data.filename
        # TOOD: Update RepairApplication record.
        # thankyou = ThanksMessage(message_to_Volunteer=form.message_to_Volunteer.data,
        #                          thanks_photo=filename, user=current_user, application_type='Repair'
        #                          )
        if ai_check(form.photo.data, filename):
            img_file = urllib.request.urlopen(
                azure_blob.get_img_url_with_blob_sas_token(blob_name="student/photo/" + filename))
            thank_photo = base64.b64encode(img_file.read())
            html = render_template('student/email/thankrepair.html', message=form.message_to_Volunteer.data,
                                   image=azure_blob.get_img_url_with_blob_sas_token("student/photo/" + filename),
                                   photo=thank_photo.decode('utf-8'))
            subject = "Thanks for your repair"
            send_email(volunteer.email, subject, html)
            application.apply_status_id = 4
            db.session.add(thankyou)
            db.session.commit()
            flash(_('Thank You For Your Message'))
            return redirect(url_for('student.student_view'))
    return render_template('student/thankyou.html', title=_('Thank You'), form=form, application=application)


@bp.route('/confirm/item/<token>')
def confirm_item_application(token):
    confirm_item(token)
    return redirect(url_for('support.teacher_apply', token=token))


@bp.route('/resend/item')
@login_required
def resend_item():
    send_confirm_item()
    app = db.session.query(EquipmentApplication).filter(EquipmentApplication.user_id == current_user.id).order_by(
        EquipmentApplication.id.desc()).first()
    app.apply_status_id = 1
    db.session.commit
    flash(_('Application has been submitted to the teacher'))
    return redirect(url_for('student.student_view'))


@bp.route('/student_be_confirm_view', methods=['GET', 'POST'])
@login_required
def student_be_confirm_view():
    isTeacher = db.session.query(User.email).filter_by(role=('teacher'),
                                                       email=current_user.student.teacher_email).first()
    print(current_user.student.teacher_email)
    return render_template('student/not_have_teacher_email.html', title=_('student  be confirm View'),
                           isTeache=isTeacher)


@bp.route('/msg', methods=['GET', 'POST'])
@login_required
def msg():
    msg_record = db.session.query(User).filter_by(id=current_user.id).first()
    if msg_record.chatroom is None:
        donateItem = None
    else:
        donateItem = db.session.query(MessageRoom).filter_by(room_id=msg_record.chatroom).order_by(
            MessageRoom.timestamp.desc()).first()
        user_status = db.session.query(User).filter_by(chatroom=msg_record.chatroom, role="donate").first()
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
