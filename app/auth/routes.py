from flask import redirect, url_for, flash, request, render_template, session, g
from flask_babel import _, get_locale
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.azure_ai.Face import get_face_index
from app.auth import bp
from app.auth.email import send_password_reset_email, generate_confirmation_token, confirm_token, send_email
from app.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, \
    TeacherRegistrationForm, StudentRegistrationForm, DonateRegistrationForm, StudentSchoolInformationForm, \
    VolunteerRegistrationForm, \
    SupportTeacherForm
from app.form_helper import populate_form_regions, get_unique_photo_key_with_username, upload_to_azure_blob
from app.google_map import get_address_by_coordinates
from app.models import User, Student, Volunteer, Teacher, School, Region
from app.azure_ai.vision_analyze import vision_analyze
from webconfig import googlemap


@bp.before_request
def before_request():
    g.locale = 'zh_TW' if str(get_locale()).startswith('zh') else str(
        get_locale())
    print(g.locale)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():

        # TODO can login username or email
        # user = db.session.query(User).filter_by(db.or_(username=form.username.data, email=form.username.data)).first()
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        session['user_id'] = user.id
        session['username'] = user.username
        login_user(user, remember=form.remember_me.data)
        if not user.activated:
            return redirect(url_for('auth.unconfirmed'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # if current_user.role == 'teacher':
            #     if not current_user.admin_confirm:
            #         next_page = url_for('admin.admin_unconfirm')
            #     else:
            #         next_page = url_for('support.teacher_view')
            # elif current_user.role == 'volunteer':
            #     next_page = url_for('support.volunteer_view')
            # elif current_user.role == 'student':
            #     is_teacher = db.session.query(User.email).filter_by(
            #         role="teacher",
            #         email=current_user.student.teacher_email).first()
            #     if is_teacher is None:
            #         next_page = url_for("student.student_be_confirm_view")
            #     elif is_teacher is not None and not current_user.admin_confirm:
            #         next_page = url_for("teacher.teacher_unconfirm")
            #     else:
            next_page = url_for('student.student_view')
        next_page = url_for('student.student_view')
        # elif current_user.role == 'donate':
        #     next_page = url_for('donate.donate_view')
        # elif current_user.role == 'admin':
        #     next_page = url_for('admin.admin_view')
        flash(_("Hello " + user.username + "! Welcome to the donate system !"))
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email is not False:
        # user = User.query.filter_by(email=email).first_or_404()
        user = db.session.query(User).filter_by(email=email).first_or_404()
        if user.activated:
            flash(_('Account already confirmed. Please login.'), 'success')
            session['remindbox'] = "stu_step1"
        else:
            user.activated = True
            db.session.add(user)
            db.session.commit()
            flash(_('You have confirmed your account. Thanks!'), 'success')
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
    return redirect(url_for('auth.login'))


@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    flash(_('Please confirm your account!'), 'warning')
    return render_template('auth/unconfirmed.html')


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/confirm.html', confirm_url=confirm_url)
    subject = "Donation System Confirmation Email"
    send_email(current_user.email, subject, html)
    flash(_('A new confirmation email has been sent.'), 'success')
    return redirect(url_for('auth.unconfirmed'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register_volunteer', methods=['GET', 'POST'])
def register_volunteer():
    if User.current_user.is_authenticated:
        return redirect(url_for('support.volunteer_view'))
    form = VolunteerRegistrationForm()
    populate_form_regions(form)
    if form.validate_on_submit():
        # filename may be same if resubmit
        volunteer_photo = get_unique_photo_key_with_username(form, '_volunteer_photo_', 'volunteer_photo')
        # filename = secure_filename(form.photo.data.filename)

        # save photo to local
        photo_path = upload_to_azure_blob(form, volunteer_photo, 'volunteer_photo')
        image_error = vision_analyze(photo_path, check_age_range=True)

        if image_error is not None:
            flash(image_error)
            return render_template('auth/register.html',
                                   title=_('Register'),
                                   form=form,
                                   role="volunteer")

        # session.clear()
        # session['full_name'] = str.lower(form.full_name.data)
        # session['username'] = form.username.data
        # session['email'] = form.email.data
        # session['phone_number'] = form.phone_number.data
        # session['region_id'] = form.region.data
        # session['role'] = form.role.data
        # session['password'] = form.password.data
        # session['photo'] = volunteer_photo
        volunteer_data = dict(form.data)
        del volunteer_data['volunteer_photo']
        del volunteer_data['csrf_token']
        del volunteer_data['submit']

        # user.set_password(form.password.data)
        # db.session.add(user)
        return redirect(url_for('auth.confirm_volunteer'))

    return render_template('auth/register.html',
                           title=_('Register'),
                           form=form)


"""
=======================
Student Register Form
=======================
"""


@bp.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = StudentRegistrationForm()
    populate_form_regions(form)

    if form.validate_on_submit():
        student_card = get_unique_photo_key_with_username(form, '_student_card_', "student_card")
        # local
        photo_path = upload_to_azure_blob(form, student_card, "student_card")
        image_error = vision_analyze(photo_path, check_age_range=True)
        if image_error is not None:
            flash(image_error)
            return render_template('auth/register.html',
                                   title=_('Register'),
                                   form=form)

        student_data = dict(form.data)
        del student_data['student_card']
        del student_data['csrf_token']
        del student_data['submit']

        session['student_data'] = student_data
        session['student_card'] = student_card
        session['face_index'] = get_face_index(photo_path)

        return redirect(url_for('auth.confirm_student'))

    return render_template('auth/register.html',
                           title=_('Register'),
                           form=form,
                           role="student")


# second page of student registration
@bp.route('/student', methods=['GET', 'POST'])
def confirm_student():
    form = StudentSchoolInformationForm()
    # form.school_name.data = session.get('school_name')
    print(session.get('student_card'))
    student_data = session['student_data']
    stu_email = student_data['email']
    school_domain = stu_email.split("@")[1].split(".edu.hk")[0].split(".")[-1]
    domain = school_domain + ".edu.hk"
    print(domain)
    if request.method == "POST":
        location = request.form["location"].split(",")
        latitude = location[0]
        longitude = location[1]
        if request.values.get('teacher_pre_email'):
            teacher_email = str(
                request.values.get('teacher_email')) + "@" + str(
                request.values.get('teacher_pre_email')) + "." + domain
        else:
            teacher_email = str(
                request.values.get('teacher_email')) + "@" + domain

        school_name = request.values.get('school_name')
        school_url = request.values.get('school_URL')
        print(teacher_email)

        print(student_data)

        region = db.session.get(Region, student_data["region"])
        print(region)
        password = student_data['password']
        del student_data['password']
        del student_data['password2']
        del student_data['region']
        student = Student(**student_data)
        student.user_photo = session.get('student_card')
        student.student_card_photo = session.get('student_card')
        student.latitude = latitude
        student.longitude = longitude
        student.face_index = session.get('face_index')
        student.region = region

        # TODO: Dropdown list later!
        school = School(name=school_name, url=school_url)
        student.school = [school]

        student.teacher_email = teacher_email

        student.set_password(password)

        db.session.add(student)
        db.session.commit()
        flash(_('You already successful to register!'))
        token = generate_confirmation_token(student.email)
        confirm_url = url_for('auth.confirm_email',
                              token=token,
                              _external=True)
        html = render_template('auth/confirm.html', confirm_url=confirm_url)
        subject = _("Donation System Registration Confirmation")
        print("before send_email")
        send_email(student.email, subject, html)
        print("after send_email")

        # TODO: Fix email logic
        # is_teacher = db.session.query(User.email).filter_by(
        #     role="teacher", email=student.teacher_email).first()
        # if is_teacher is not None:
        #     token2 = generate_confirmation_token(student.email)
        #     confirm_url2 = url_for('teacher.confirm_email',
        #                            token=token2,
        #                            _external=True)
        #     html2 = render_template('teacher/student_confirm.html',
        #                             confirm_url=confirm_url2,
        #                             name=student.full_name)
        #     subject2 = _(
        #         "Your student {STUDENTNAME} wants you to help create an account at iShare.support!"
        #     ).replace("{STUDENTNAME}", student.full_name)
        #     send_email(student.teacher_email, subject2, html2)
        # else:
        #     host = request.host
        #     confirm_url = "https://" + host + "/auth/register_teacher?email=" + student.teacher_email
        #     html2 = render_template('teacher/teacher_create_account.html',
        #                             confirm_url=confirm_url,
        #                             name=student.last_name + " " + student.first_name)
        #     subject2 = _(
        #         "Your student {STUDENTNAME} wants you to help create an account at iShare.support!"
        #     ).replace("{STUDENTNAME}", student.full_name)
        #     send_email(student.teacher_email, subject2, html2)

        return redirect(url_for('main.index'))
    return render_template('student/student.html',
                           title=_('Student'),
                           form=form,
                           domain=domain,
                           key=googlemap.google_key)


"""
=======================
Teacher Register Form
=======================
"""


@bp.route('/register_donate', methods=['GET', 'POST'])
def register_donate():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = DonateRegistrationForm()
    populate_form_regions(form)
    if form.validate_on_submit():
        donor_photo = get_unique_photo_key_with_username(form, '_donor_photo_', 'donor_photo')
        photo_path = upload_to_azure_blob(form, donor_photo, 'donor_photo')
        image_error = vision_analyze(photo_path)
        if image_error is not None:
            flash(image_error)
            return render_template('auth/register.html',
                                   title=_('Register'),
                                   form=form)
        user = User(role=form.role.data,
                    full_name=form.full_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    phone_number=form.phone_number.data,
                    region_id=form.region.data,
                    user_photo=donor_photo)
        user.set_password(form.password.data)

        flash(_('You already successful to register!'))
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email',
                              token=token,
                              _external=True)
        html = render_template('auth/confirm.html', confirm_url=confirm_url)
        subject = _("Donation System Registration Confirmation")
        send_email(user.email, subject, html)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'),
                           form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/support_volunteer', methods=['GET', 'POST'])
def support_volunteer():
    form = VolunteerRegistrationForm()
    if request.method == "POST":
        location = request.form["location"].split(",")
        latitude = location[0]
        longitude = location[1]
        volunteer_address = get_address_by_coordinates(googlemap.google_key,
                                                       latitude, longitude)
        user = User(full_name=session.get('full_name'),
                    username=session.get('username'),
                    email=session.get('email'),
                    phone_number=session.get('phone_number'),
                    region_id=session.get('region_id'),
                    role=session.get('role'),
                    user_photo=session.get('photo'))
        volunteer = Volunteer(address=volunteer_address,
                              user_id=session.get('username'))
        user.set_password(session.get('password'))
        flash(_('You already successful to register!'))
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email',
                              token=token,
                              _external=True)
        html = render_template('auth/confirm.html', confirm_url=confirm_url)
        subject = _("Donation System Registration Confirmation")
        send_email(user.email, subject, html)
        db.session.add(volunteer)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('support/volunteer.html',
                           title=_('Volunteer'),
                           form=form,
                           key=googlemap.google_key)


"""
=======================
Teacher Register Form
=======================
"""


@bp.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = TeacherRegistrationForm()
    teacher_email = request.args.get('email')
    if teacher_email is not None:
        form.email.data = teacher_email

    populate_form_regions(form)
    if form.validate_on_submit():
        teacher_photo = get_unique_photo_key_with_username(form, '_teacher_photo_')
        try:
            staff_card = get_unique_photo_key_with_username(form, '_staff_card_', "staff_card")
        except AttributeError:
            staff_card = "None"
        # Don't need to change path anymore
        """
        ===================
        teacher photo
        ===================
        """
        photo_path = upload_to_azure_blob(form, teacher_photo, "teacher_photo")
        image_error = vision_analyze(photo_path, check_age_range=True)
        if image_error is not None:
            flash(image_error)
            return render_template('auth/register.html',
                                   title=_('Register'),
                                   form=form)
        """
        ===================
        staff card
        ===================
        """
        # P
        if staff_card != "None":
            photo_path = upload_to_azure_blob(form, staff_card, "staff_card")
            image_error = vision_analyze(photo_path, check_age_range=True)
            if image_error is not None:
                flash(image_error)
                return render_template('auth/register.html',
                                       title=_('Register_Teacher'),
                                       form=form)
        # session.clear()
        # session['full_name'] = form.full_name.data
        # session['username'] = form.username.data
        # session['email'] = form.email.data
        # session['phone_number'] = form.phone_number.data
        # session['region_id'] = form.region.data
        # session['role'] = form.role.data
        # session['password'] = form.password.data
        # session['photo'] = teacher_photo
        # session['staff_card'] = staff_card
        teacher_data = dict(form.data)
        del teacher_data['teacher_data']
        del teacher_data['teacher_photo']
        del teacher_data['staff_card']
        del teacher_data['csrf_token']
        del teacher_data['submit']

        session['teacher_data'] = teacher_data
        session['teacher_photo'] = teacher_photo
        session['staff_card'] = staff_card

        return redirect(url_for('auth.confirm_teacher'))
    return render_template('auth/register.html',
                           title=_('Register_Teacher'),
                           form=form)


@bp.route('/support_teacher', methods=['GET', 'POST'])
def confirm_teacher():
    form = SupportTeacherForm()
    if request.method == "POST":
        # location = request.form["location"].split(",")
        # latitude = location[0]
        # longitude = location[1]
        teacher_data = session['teacher_data']
        password = teacher_data['password']
        office_phone_number = request.values.get('office_phone_number')
        school_name = request.values.get('school_name')
        school_url = request.values.get('school_website')
        del teacher_data['password']
        del teacher_data['password2']
        teacher = Teacher(**teacher_data)
        teacher.user_photo = session.get('teacher_photo')
        teacher.staff_card_photo = session.get('staff_card')
        # TODO: Dropdown list later!
        school = School(name=school_name, url=school_url)
        teacher.school = [school]

        teacher.office_phone_number = office_phone_number

        teacher.set_password(password)

        # school_address = get_address_by_coordinates(googlemap.google_key,
        #                                             latitude, longitude)
        # user = User(full_name=session.get('full_name'),
        #             username=session.get('username'),
        #             email=session.get('email'),
        #             phone_number=session.get('phone_number'),
        #             region_id=session.get('region_id'),
        #             role=session.get('role'),
        #             user_photo=session.get('photo'))
        #
        # teacher = Teacher(school_name=school_name,
        #                   school_address=school_address,
        #                   school_website=school_website,
        #                   office_phone_number=office_phone_number,
        #                   staff_card_photo=session.get('staff_card'),
        #                   user_id=session.get('username'))
        db.session.add(teacher)
        db.session.commit()
        flash(_('You already successful to register!'))
        token = generate_confirmation_token(teacher.email)
        confirm_url = url_for('auth.confirm_email',
                              token=token,
                              _external=True)
        html = render_template('auth/confirm.html', confirm_url=confirm_url)
        subject = _("Donation System Registration Confirmation")
        print("before send_email")
        send_email(teacher.email, subject, html)
        print("after send_email")

        # email = db.session.query(User).filter_by(role="admin").first()
        # # email = User.query.filter_by(role="admin").first()
        # token2 = generate_confirmation_token(user.email)
        # confirm_url2 = url_for('admin.confirm_form',
        #                        token=token2,
        #                        _external=True)
        # html2 = render_template('admin/confirm.html',
        #                         confirm_url=confirm_url2,
        #                         name=user.full_name)
        # subject2 = _("Donation System Registration Confirmation")
        # send_email(email.email, subject2, html2)

        return redirect(url_for('main.index'))
    return render_template('support/teacher.html',
                           title=_('teacher'),
                           form=form)
