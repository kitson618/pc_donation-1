from flask import current_app, redirect, url_for, flash, request, render_template, session, jsonify
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from app.admin.email import confirm_token, generate_confirmation_token, send_email
from app.admin import bp
from app.admin.forms import ConfirmTeacherForm
from app.admin import index_data
from app.models import User
from functools import wraps
from datetime import datetime


def is_admins(func):
    @wraps(func)
    def teachers_view(*args, **kwargs):
        try:
            if current_user.role == 'admin':
                return func(*args, **kwargs)
            # else:
            #     raise
        except:
            return render_template('errors/404.html'), 404

    return teachers_view


# def send_confirm_item():
#     email = User.query.filter_by(role=('admin')).first()
#     teacher = User.query.filter_by(username=session.get('username')).first()
#     token = generate_confirmation_token(current_user.id)
#     confirm_url = url_for('admin.confirm_form', token=token, _external=True)
#     html = render_template('admin/confirm.html', confirm_url=confirm_url, name=teacher.full_name)
#     subject = "Approve student application"
#     send_email(email.email, subject, html)
#     flash('A new confirmation email has been sent.', 'success')


#
# # @bp.route('/confirm/<token>')
# def confirm_email(token):
#     email = confirm_token(token)
#     if email is not False:
#         user = User.query.filter_by(email=email).first_or_404()
#         if user.teacher_confirm:
#             flash('Account already confirmed. Please login.', 'success')
#             session['remindbox'] = "stu_step1"
#         else:
#             user.teacher_confirm = True
#             db.session.add(user)
#             db.session.commit()
#             flash('You have confirmed your account. Thanks!', 'success')
#     else:
#         flash('The confirmation link is invalid or has expired.', 'danger')
#     return redirect(url_for('auth.login'))

@bp.route('/admin_unconfirm')
@login_required
def admin_unconfirm():
    flash(_('Please confirm your account!'), 'warning')
    return render_template('admin/admin_unconfirm.html')


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('admin.confirm_form', token=token, _external=True)
    html = render_template('admin/confirm.html', confirm_url=confirm_url, name=current_user.full_name)
    subject = "Donation System Confirmation Email"
    user = User.query.filter_by(role=('admin')).first()
    send_email(user.email, subject, html)
    flash(_('A new confirmation email has been sent.'), 'success')
    return redirect(url_for('admin.admin_unconfirm'))


@bp.route('/confirm/<token>')
def confirm_form(token):
    email = confirm_token(token)
    if email is not False:
        user = User.query.filter_by(email=email).first_or_404()
        print(user)
        if user.admin_confirm:
            flash(_('Account already confirmed. Please login.'), 'success')
            session['remindbox'] = "stu_step1"
            # return redirect(url_for('admin.admin_view'))
        else:
            return redirect(url_for('admin.admin_confirm', token=token))
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
    return redirect(url_for('admin.admin_confirm', token=token))


@bp.route('/admin_view', methods=['GET', 'POST'])
@is_admins
@login_required
def admin_view():
    lang = str(get_locale())
    categorys_admin = lang == "zh" and index_data.categorys_admin_zh or index_data.categorys_admin
    return render_template('admin/admin_view.html', title=_('admin View'), categorys_admin=categorys_admin)


@bp.route('/admin_record', methods=['GET', 'POST'])
@login_required
@is_admins
def admin_record():
    record = db.session.query(AdminPermission).filter_by(permission_admin_id=current_user.id).all()
    return render_template('admin/admin_record.html', title=_('Admin record'), record=record)


@bp.route('/admin_confirm/<token>', methods=['GET', 'POST'])
@login_required
@is_admins
def admin_confirm(token):
    form = ConfirmTeacherForm()
    email = confirm_token(token)
    teacher_confirm = db.session.query(User).filter_by(email=email).first()
    form.full_name.data = teacher_confirm.full_name
    form.username.data = teacher_confirm.username
    form.email.data = teacher_confirm.email
    form.phone_number.data = teacher_confirm.phone_number
    form.school_name.data = teacher_confirm.teacher.school_name
    form.school_address.data = teacher_confirm.teacher.school_address
    form.school_website.data = teacher_confirm.teacher.school_website
    form.office_phone_number.data = teacher_confirm.teacher.office_phone_number
    if form.validate_on_submit():
        permission = AdminPermission(full_name=request.form.get('full_name'),
                                     username=request.form.get('username'),
                                     email=request.form.get('email'),
                                     phone_number=request.form.get('phone_number'),
                                     school_name=request.form.get('school_name'),
                                     school_address=request.form.get('school_address'),
                                     school_website=request.form.get('school_website'),
                                     office_phone_number=request.form.get('office_phone_number'),
                                     permission_status=form.permission.data,
                                     permission_admin_id=current_user.id,
                                     apply_status_id= 1,
                                     idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(permission)
        db.session.commit()
        if email is not False:
            if permission.permission_status:
                confirm = permission.query.filter_by(email=email).first_or_404()
                user = db.session.query(User).filter_by(email=email).first()
                confirm.apply_status_id = 4
                user.admin_confirm = True
                db.session.add(user)
                db.session.add(confirm)
                db.session.commit()
                flash(_('You have approved your teacher\'s application . Thanks!'), 'success')
            elif not permission.permission_status:
                confirm = permission.query.filter_by(email=email).first_or_404()
                user = User.query.filter_by(email=email).first_or_404()
                confirm.apply_status_id = 6
                user.admin_confirm = False
                db.session.add(user)
                db.session.add(confirm)
                db.session.commit()
                flash(_('You have not approve your teacher\'s application . Thanks!'), 'success')
        else:
            flash(_('The confirmation link is invalid or has expired.'), 'danger')
        return redirect(url_for('admin.admin_view'))
    return render_template('admin/admin_confirm.html', title=_('Admin confirm form'), form=form)
