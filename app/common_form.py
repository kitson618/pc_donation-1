import re
from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, URL, AnyOf


from app.models import User, Teacher


class CommonForm(FlaskForm):
    class NewUsername(object):
        def __call__(self, form, field):
            username = field.data

            if re.search('[-+!@#$%^&*(){}<>_=~`:;?/,.|]',
                         username) is not None:
                raise ValidationError(
                    _("Please make sure your full name does not contain special character in it"
                      ))
            user = User.query.filter_by(username=username).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

    class Password(object):
        def __call__(self, form, field):
            password = field.data
            if re.search('[0-9]', password) is None:
                raise ValidationError(
                    _('Please make sure your password at least one number in it'
                      ))
            elif re.search('[A-Z]', password) is None:
                raise ValidationError(
                    _('Please make sure your password at least one capital letter in it'
                      ))
            elif re.search('[a-z]', password) is None:
                raise ValidationError(
                    _('Please make sure your password at least one lowercase letter in it'
                      ))
            elif re.search('[-+!@#$%^&*(){}><_=~`:;?/,.|]', password) is None:
                raise ValidationError(
                    _('Please make sure your password at least one special character in it'
                      ))

    class Name(object):
        def __call__(self, form, field):
            full_name = field.data
            if re.search('[-+!@#$%^&*(){}<>_=~`:;?/,.| ]',
                         full_name) is not None:
                raise ValidationError(_('No special character or space'))

    class PhoneNumber(object):
        def __call__(self, form, field):
            phone_number = field.data
            if re.search('[0-9]', phone_number) is None:
                raise ValidationError(_('Please use digits.'))

    class DuplicateEmail(object):
        def __call__(self, form, field):
            email = field.data
            user = User.query.filter_by(email=email).first()
            if user is not None:
                raise ValidationError(_('Please use a different email address.'))

    class SchoolEmail(object):
        def __call__(self, form, field):
            email = field.data
            if not email.lower().endswith("edu.hk"):
                raise ValidationError(_("The email must be school email"))

    class SchoolName(object):
        def __call__(self, form, field):
            name = field.data
            if re.search('[-+!@#$%^&*(){}><_=~`:;?/,.|]', name) is not None:
                raise ValidationError(
                    _("Please make sure your school name does not contain special character in it"
                      ))
            elif re.search('[0-9]', name) is not None:
                raise ValidationError(_("Please make sure your school name does not contain digit in it"))

    class OfficePhoneNumber(object):
        def __call__(self, form, field):
            office_phone_number = field.data
            user = Teacher.query.filter_by(
                office_phone_number=office_phone_number.data).first()
            if user is not None:
                raise ValidationError(
                    _('Please use a different office phone number.'))


    EMAIL_VALIDATORS = [
        DataRequired(),
        Email(message=_l('email_error_msg')),
        Length(max=30, message=_l('leng error'))
    ]
    # noinspection PyTypeChecker
    NEW_EMAIL_VALIDATORS = EMAIL_VALIDATORS + [DuplicateEmail()]
    NEW_SCHOOL_EMAIL_VALIDATORS = NEW_EMAIL_VALIDATORS + [SchoolEmail()]

    USERNAME_VALIDATORS = [
        DataRequired(),
        Length(min=3, max=30, message=_l('leng_error_2_30')),
        Name()
    ]
    # noinspection PyTypeChecker
    NEW_USERNAME_VALIDATORS = USERNAME_VALIDATORS + [NewUsername()]

    NAME_VALIDATORS = [
        DataRequired(),
        Length(min=1),
        Regexp('[a-zA-Z]')
    ]
    PASSWORD_VALIDATORS = [
        DataRequired(),
        Regexp(r'^[\w.@+-]+$'),
        Length(min=8),
        Password()
    ]
    # noinspection PyTypeChecker
    PASSWORD2_VALIDATORS = PASSWORD_VALIDATORS + [EqualTo('password', message=_l('pass_error'))]

    PHONE_VALIDATORS = [DataRequired(), Length(min=8, max=8), PhoneNumber()]

    IMAGE_VALIDATORS = [
        FileAllowed(['jpg', 'png', 'jpeg'],
                    message=_l('Only jpg,jpeg and png')),
        FileRequired(message=_l('File must be uploaded'))
    ]

    MESSAGE_VALIDATORS = [
        DataRequired(),
        Length(min=10, max=300, message=_l("leng_error")),
        Regexp('[a-zA-Z]')
    ]

    TITTLE_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=100, message=_l("leng_error"))
    ]

    STORY_VALIDATORS = [
        DataRequired(),
        Length(min=50, max=1000, message=_l("leng error")),
    ]

    SCHOOL_NAME_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=30, message=_l("leng_error")),
        SchoolName()
    ]

    SCHOOL_URL_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=200, message=_l("leng_error")),
        URL(message=_l("Must be a valid URL")),
        AnyOf(values=["edu.hk"], message=_l("must contain edu.hk"))
    ]

    DESCRIPTION_VALIDATORS = [
        DataRequired(),
        Length(min=10, message=_l("leng error")),
        Length(max=1000, message=_l("leng error"))
    ]

    OFFICE_PHONE_VALIDATORS = [DataRequired(), Length(min=8, max=8), OfficePhoneNumber()]
