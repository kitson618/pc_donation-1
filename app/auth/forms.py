from flask_babel import lazy_gettext as _l, _
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, \
    TextAreaField, HiddenField
from wtforms.validators import DataRequired
import re
from flask_wtf.file import FileField
from app.common_form import CommonForm
from webconfig import recaptcha as Recaptcha


class LoginForm(CommonForm):
    username = StringField(_l('Username or email'), validators=CommonForm.USERNAME_VALIDATORS)
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class VolunteerRegistrationForm(CommonForm):
    username = StringField(_l('Username'),
                           validators=CommonForm.NEW_USERNAME_VALIDATORS)
    first_name = StringField(_l('First Name'),
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l('Last Name'),
                            validators=CommonForm.NAME_VALIDATORS)
    email = StringField(_l('Email'),
                        validators=CommonForm.NEW_EMAIL_VALIDATORS)
    phone_number = StringField(_l('Phone Number'),
                               validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"placeholder": _l('phone_require')})
    region = SelectField(_l('Region'), validators=[DataRequired()], coerce=int)
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l('Repeat Password'),
                              validators=CommonForm.PASSWORD2_VALIDATORS)

    photo = FileField(_l('Photo'), validators=CommonForm.IMAGE_VALIDATORS)

    if Recaptcha.Enable:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l('Next'))


class TeacherRegistrationForm(CommonForm):
    username = StringField(_l('Username'),
                           validators=CommonForm.NEW_USERNAME_VALIDATORS)
    first_name = StringField(_l('First Name'),
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l('Last Name'),
                            validators=CommonForm.NAME_VALIDATORS)
    email = StringField(_l('Email'),
                        validators=CommonForm.NEW_SCHOOL_EMAIL_VALIDATORS)
    phone_number = StringField(_l('Phone Number'),
                               validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"placeholder": _l('phone_require')})
    # region = SelectField(_l('Region'), validators=[DataRequired()], coerce=int)
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l('Repeat Password'),
                              validators=CommonForm.PASSWORD2_VALIDATORS)

    photo = FileField(_l('Teacher Photo'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    staff_card = FileField(_l('Staff Card'),
                           validators=CommonForm.IMAGE_VALIDATORS)
    if Recaptcha.Enable:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l('Next'))


class StudentRegistrationForm(CommonForm):
    username = StringField(_l('Username'),
                           validators=CommonForm.NEW_USERNAME_VALIDATORS)
    first_name = StringField(_l('First Name'),
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l('Last Name'),
                            validators=CommonForm.NAME_VALIDATORS)
    email = StringField(_l('Email'),
                        validators=CommonForm.NEW_SCHOOL_EMAIL_VALIDATORS,
                        render_kw={"placeholder": _l('school_email')})
    phone_number = StringField(_l('Phone Number'),
                               validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"placeholder": _l('phone_require')})
    region = SelectField(_l('Region'), validators=[DataRequired()], coerce=int)
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l('Repeat Password'),
                              validators=CommonForm.PASSWORD2_VALIDATORS)
    student_card = FileField(_l('Student card'),
                             render_kw={"readonly": True},
                             validators=CommonForm.IMAGE_VALIDATORS)
    if Recaptcha.Enable:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l('Next'))


class DonateRegistrationForm(CommonForm):
    username = StringField(_l('Username'),
                           validators=CommonForm.NEW_USERNAME_VALIDATORS)
    first_name = StringField(_l('First Name'),
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l('Last Name'),
                            validators=CommonForm.NAME_VALIDATORS)
    email = StringField(_l('Email'),
                        validators=CommonForm.NEW_EMAIL_VALIDATORS)
    phone_number = StringField(_l('Phone Number'),
                               validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"placeholder": _l('phone_require')})
    region = SelectField(_l('Region'), validators=[DataRequired()], coerce=int)
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l('Repeat Password'),
                              validators=CommonForm.PASSWORD2_VALIDATORS)
    photo = FileField(_l('Please upload your photo'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    if Recaptcha.Enable:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l('Register'))


class ResetPasswordRequestForm(CommonForm):
    email = StringField(
        _l('Email'),
        validators=CommonForm.EMAIL_VALIDATORS)
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(CommonForm):
    password = PasswordField(_l('Password'),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l('Repeat Password'),
                              validators=CommonForm.PASSWORD2_VALIDATORS)
    submit = SubmitField(_l('Request Password Reset'))


class DonateDataForm(CommonForm):
    photo = FileField(_l('Photo'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    phone_number = StringField(
        _l('Phone Number', validators=CommonForm.PHONE_VALIDATORS))
    email = StringField(
        _l('Email'),
        validators=CommonForm.NEW_EMAIL_VALIDATORS)
    if Recaptcha.Enable:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l('Submit'))


class StudentSchoolInformationForm(CommonForm):
    teacher_email = StringField(
        _l('Please enter your teacher\'s email'),
        validators=CommonForm.EMAIL_VALIDATORS)
    school_name = TextAreaField(_l('Please enter your school name'),
                                validators=CommonForm.SCHOOL_NAME_VALIDATORS)
    school_URL = TextAreaField(_l('Please enter your school URL'),
                               validators=CommonForm.SCHOOL_URL_VALIDATORS)
    if Recaptcha.Enable:
        recaptcha = RecaptchaField()

    submit = SubmitField(_l('Submit'))


class SupportTeacherForm(CommonForm):
    school_name = StringField(
        _l('School Name'), validators=CommonForm.SCHOOL_NAME_VALIDATORS)
    school_website = StringField(
        _l('School Website'),
        validators=CommonForm.SCHOOL_URL_VALIDATORS)
    office_phone_number = StringField(
        _l('Office Phone Number'), validators=CommonForm.OFFICE_PHONE_VALIDATORS)
    submit = SubmitField(_l('Submit'))
