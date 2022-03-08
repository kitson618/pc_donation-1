from flask import current_app, redirect, url_for, flash, request, render_template, session, jsonify
from flask_babel import _
from flask_login import current_user, login_required
from app import azure_blob, db
from app.role import is_teacher
from app.teacher.email import confirm_token, generate_confirmation_token, send_email
from app.teacher import bp
from app.models import User
from functools import wraps
from datetime import datetime


@bp.route('/teacher_unconfirm')
@login_required
def teacher_unconfirm():
    flash(_('Please wait for your teacher to confirm your account!'), 'warning')
    isTeacher = db.session.query(User.email).filter_by(role=('teacher'),
                                                       email=current_user.student.teacher_email).first()
    return render_template('teacher/teacher_unconfirm.html', isTeacher=isTeacher)


@bp.route('/resend')
@login_required
def resend_confirmation():
    isTeacher = db.session.query(User.email).filter_by(role=('teacher'), email=current_user.student.teacher_email).first()
    if isTeacher is not None:
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('teacher.confirm_email', token=token, _external=True)
        html = render_template('teacher/confirm.html', confirm_url=confirm_url, name=current_user.full_name)
        subject = "Donation System Confirmation Email"
        send_email(current_user.student.teacher_email, subject, html)
        flash(_('A new confirmation email has been sent.'), 'success')
    return redirect(url_for('teacher.teacher_unconfirm'))


@bp.route('/confirm_email/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email is not False:
        user = User.query.filter_by(email=email).first_or_404()
        if user.admin_confirm:
            flash(_('Account already confirmed. Please login.'), 'success')
            session['remindbox'] = "stu_step1"
        else:
            return redirect(url_for('teacher.teacher_confirm', token=token))
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
    return redirect(url_for('teacher.teacher_confirm', token=token))


@bp.route('/teacher_confirm/<token>', methods=['GET', 'POST'])
@login_required
@is_teacher
def teacher_confirm(token):
    form = ConfirmStudentForm()
    email = confirm_token(token)
    student_info = db.session.query(User).filter_by(email=email).first()
    form.full_name.data = student_info.full_name
    form.username.data = student_info.username
    form.email.data = student_info.email
    form.phone_number.data = student_info.phone_number
    form.school_name.data = student_info.student.school_name
    form.school_address.data = student_info.student.school_address
    form.school_URL.data = student_info.student.school_URL
    if form.validate_on_submit():
        teacher_permission = TeacherPermission(full_name=request.form.get('full_name'),
                                       username=request.form.get('username'),
                                       email=request.form.get('email'),
                                       phone_number=request.form.get('phone_number'),
                                       school_name=request.form.get('school_name'),
                                       school_address=request.form.get('school_address'),
                                       #test
                                       school_URL=request.form.get('school_URL'),
                                       permission_status=form.permission.data,
                                       permission_teacher_id=current_user.id,
                                       apply_status_id=1,
                                       idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(teacher_permission)
        db.session.commit()
        if email is not False:
            if teacher_permission.permission_status == True:
                confirm = teacher_permission.query.filter_by(email=email).first_or_404()
                user = db.session.query(User).filter_by(email=email).first()
                #TODO what is 4
                confirm.apply_status_id = 4
                user.admin_confirm = True
                db.session.add(user)
                db.session.add(confirm)
                db.session.commit()
                flash(_('You have approved your teacher\'s application . Thanks!'), 'success')
            elif teacher_permission.permission_status == False:
                confirm = teacher_permission.query.filter_by(email=email).first_or_404()
                user = User.query.filter_by(email=email).first_or_404()
                # TODO what is 6
                confirm.apply_status_id = 6
                user.admin_confirm = False
                db.session.add(user)
                db.session.add(confirm)
                db.session.commit()
                flash(_('You have not approve your teacher\'s application . Thanks!'), 'success')
        else:
            flash(_('The confirmation link is invalid or has expired.'), 'danger')
        return redirect(url_for('support.teacher_view'))
    return render_template('teacher/teacher_confirm.html', title=_('Admin confirm form'), form=form, image=azure_blob.get_img_url_with_blob_sas_token, photo=student_info.user_photo)
