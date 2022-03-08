import requests
from flask import redirect, url_for, flash, request, render_template, session
from flask_babel import _, get_locale
from flask_googlemaps import Map
from flask_login import current_user, login_required

from app import azure_blob, db
from app.google_map import get_student_location, get_current_volunteer_location
from app.models import User, RepairApplication
from app.role import is_teacher, is_volunteer
from app.student.email import send_email
from app.support import bp
from app.support import index_data
from app.support.forms import AppointmentForm
from webconfig import ai_chatbot


@bp.route('/volunteer_view', methods=['GET', 'POST'])
@login_required
@is_volunteer
def volunteer_view():
    lang = str(get_locale())
    categorys_volunteer = lang == "zh" and index_data.categorys_volunteer_zh or index_data.categorys_volunteer
    categorys_volunteer_googlemap = lang == "zh" and index_data.categorys_volunteer_googlemap_zh or index_data.categorys_volunteer_googlemap
    return render_template('support/volunteer_view.html', title=_('Volunteer View'),
                           categorys_volunteer=categorys_volunteer,
                           categorys_volunteer_googlemap=categorys_volunteer_googlemap,
                           key=ai_chatbot.volunteer_chatbot_key)


@bp.route('/teacher_view', methods=['GET', 'POST'])
@login_required
@is_teacher
def teacher_view():
    lang = str(get_locale())
    categorys_teacher = lang == "zh" and index_data.categorys_teacher_zh or index_data.categorys_teacher
    categorys_teacher_permission = lang == "zh" and index_data.categorys_teacher_permission_zh or index_data.categorys_teacher_permission
    return render_template('support/teacher_view.html', title=_('teacher View'), categorys_teacher=categorys_teacher,
                           categorys_teacher_permission=categorys_teacher_permission,
                           key=ai_chatbot.teacher_chatbot_key)


# TODO: No more Permission table
#
# @bp.route('/teacher_apply/<token>', methods=['GET', 'POST'])
# @login_required
# @is_teacher
# def teacher_apply(token):
#     form = PermissionForm()
#     email = confirm_item(token)
#     item_name = []
#     # appointment = db.session.query(User.full_name, Application.title, Application.story, Item.item_name,
#     #                                Application.apply_photo).order_by(
#     #     Application.id.desc()).outerjoin(applicationItem,
#     #                                      Item.id == applicationItem.item_id).outerjoin(
#     #     Application, applicationItem.application_id == Application.id).outerjoin(User,
#     #                                                                              Application.user_id == User.id).filter(
#     #     Application.user_id == email).first()
#     appointment = db.session.query(Application).filter_by(user_id=email).order_by(Application.id.desc()).first()
#     # print(appointment.applications)
#     # outerjoin(Application, applicationItem.application_id == Application.id)
#     # information_data = appointment.split(",")
#     # print(information_data)
#     form.student_name.data = appointment.user.full_name
#     form.title.data = appointment.title
#     form.story.data = appointment.story
#     for record in appointment.applications:
#         item_name.append(record.item.item_name)
#     item_name = ", ".join(item_name)
#     print(item_name)
#     form.item_name.data = item_name
#     # form.student_name.data = appointment.full_name
#     # form.title.data = appointment.title
#     # form.story.data = appointment.story
#     # form.item_name.data = appointment.item_name
#     print(len(appointment.story))
#     try:
#         print(save_sentiment_analysis_result(authenticate_client(), [appointment.story]))
#     except Exception as e:
#         print(e)
#     if form.validate_on_submit():
#         story_permission = Permission(student_name=request.form.get('student_name'),
#                                       title=request.form.get('title'),
#                                       story=request.form.get('story'),
#                                       item_name=request.form.get('item_name'),
#                                       permission_status=form.permission.data,
#                                       permission_id=current_user.id,
#                                       idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#         db.session.add(story_permission)
#         db.session.commit()
#         if email is not False:
#             if story_permission.permission_status:
#                 item = Application.query.filter_by(user_id=email).order_by(Application.id.desc()).first_or_404()
#                 item.apply_status_id = 2
#                 item.status_id = 1
#                 db.session.add(item)
#                 db.session.commit()
#                 flash(_('You have approved your student\'s application . Thanks!'), 'success')
#             elif not story_permission.permission_status:
#                 item = Application.query.filter_by(user_id=email).order_by(Application.id.desc()).first_or_404()
#                 item.apply_status_id = 6
#                 item.status_id = 2
#                 db.session.add(item)
#                 db.session.commit()
#                 flash(_('You have not approve your student\'s application . Thanks!'), 'success')
#         else:
#             flash(_('The confirmation link is invalid or has expired.'), 'danger')
#         return redirect(url_for('support.teacher_view'))
#     return render_template('support/teacher_apply.html', title=_('teacher apply'), form=form,
#                            appointment=appointment, image=azure_blob.get_img_url_with_blob_sas_token)
#
#
# @bp.route('/teacher_record', methods=['GET', 'POST'])
# @login_required
# @is_teacher
# def teacher_record():
#     record = db.session.query(Permission).filter_by(permission_id=current_user.id).all()
#     return render_template('support/teacher_record.html', title=_('teacher record'), record=record)
#
#
# @bp.route('/teacher_permission_record', methods=['GET', 'POST'])
# @login_required
# @is_teacher
# def teacher_permission_record():
#     records = db.session.query(TeacherPermission).filter_by(permission_teacher_id=current_user.id).all()
#     print(records)
#     return render_template('teacher/teacher_permission_record.html', title=_('teacher permission record'),
#                            records=records)
#

@bp.route('/map', methods=['GET', 'POST'])
@login_required
@is_volunteer
def map():
    student_location = get_student_location()

    volunteer_user = get_current_volunteer_location(current_user.username)
    map = Map(
        identifier="map", varname="map",
        style="height:1100px;width:1100px;margin:0;",
        # set identifier, varname
        lat=volunteer_user[0], lng=volunteer_user[1],  # have to change user_location
        # set map base to user_location
        zoom=14,  # set zoomlevel
        # markers=[(loc, loc, render_template('support/marker.html', title=title, information=information)) for loc
        #          in
        #          student_location.values()]
        markers=[(loc, loc, render_template('support/marker.html', title=loc['id'])) for loc
                 in
                 student_location.values()]
        # render_template('support/marker.html')
    )
    return render_template('support/map.html', title=_('Volunteer Repair'), map=map)


@bp.route('/appointment_repair', methods=['GET', 'POST'])
@login_required
@is_volunteer
def appointment_repair():
    form = AppointmentForm()
    if request.method == "POST":
        # information = request.form.get('fill in')
        title = request.form.get('repair id')
        information = db.session.query(RepairApplication).filter_by(id=title, confirm_button=False).first()
        print(information)
        if information is not None:
            information_data = information
            form.student_name.data = information_data.user.full_name
            form.student_address.data = information_data.address
            form.student_phone_number.data = information_data.user.phone_number
            form.title.data = information_data.title
            form.description.data = information_data.description
            form.id.data = information_data.id
            return render_template('support/appointment_repair.html', title=_('Volunteer Record'), form=form,
                                   information_data=information_data.apply_repair_photo,image=azure_blob.get_img_url_with_blob_sas_token)
    if form.is_submitted():
        # TODO: Update appoinment field.
        # appointment = AppointmentTime(student_name=request.form.get('student_name'),
        #                               student_address=request.form.get('student_address'),
        #                               phone_number=request.form.get('student_phone_number'),
        #                               title=request.form.get('title'),
        #                               description=request.form.get('description'),
        #                               appointment_data=request.form.get('appointment_date'),
        #                               appointment_time=request.form.get('appointment_time'),
        #                               appointment_id=current_user.id)
        confirm = RepairApplication.query.get(request.form.get('id'))
        confirm.confirm_button = True
        confirm.apply_status_id = 5
        confirm.volunteer_id = current_user.id
        student = User.query.filter_by(id=confirm.user_id).first()
        db.session.add(confirm)
        db.session.commit()
        html = render_template('support/volunteer_confirm_time.html', date=request.form.get('appointment_date'),
                               name=student.full_name,
                               time=request.form.get('appointment_time'), phone=current_user.phone_number)

        subject = "Congratulations you already have volunteer to repair your item "
        send_email(student.email, subject, html)
        flash(_('Appointment Complete'))
        if 'remindbox' in session:
            remindbox = session['remindbox']
            print(remindbox)
        else:
            session["remindbox"] = "vol_step1"

        return redirect(url_for('support.volunteer_view'))
    return render_template('support/volunteer_view.html', title=_('Volunteer Record'), form=form)


@bp.route('/getdata', methods=['GET', 'POST'])
def getdata():
    json_data = requests.get.args('json')
    return json_data


@bp.route('/volunteer_record', methods=['GET', 'POST'])
@login_required
@is_volunteer
def volunteer_record():
    repair_record = db.session.query(RepairApplication).filter_by(appointment_id=current_user.id).all()
    if 'remindbox' in session:
        remindbox = session['remindbox']
    else:
        session["remindbox"] = "vol_step2"
    return render_template('support/volunteer_record.html', title=_('Volunteer Record'), repair_record=repair_record)


@bp.route('/volunteer_repair_case', methods=['GET', 'POST'])
@login_required
@is_volunteer
def volunteer_repair_case():
    return render_template('support/volunteer_repair_case.html', title=_('Volunteer Rapair Case'))
