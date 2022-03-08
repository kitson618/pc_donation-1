from flask_babel import lazy_gettext as _l
from wtforms import StringField, BooleanField, SubmitField, IntegerField, \
    HiddenField

from app.common_form import CommonForm


class ConfirmTeacherForm(CommonForm):
    id = HiddenField(_l('id'), render_kw={'readonly': True})
    username = StringField(_l('Username'), validators=CommonForm.NEW_USERNAME_VALIDATORS, render_kw={'readonly': True})
    first_name = StringField(_l('First Name'), validators=CommonForm.NAME_VALIDATORS,
                             render_kw={'readonly': True})
    last_name = StringField(_l('Last Name'), validators=CommonForm.NAME_VALIDATORS,
                            render_kw={'readonly': True})
    email = StringField(_l('Email'), validators=CommonForm.EMAIL_VALIDATORS, render_kw={'readonly': True})
    phone_number = IntegerField(_l('Phone Number'), validators=CommonForm.PHONE_VALIDATORS,
                                render_kw={'readonly': True})
    school_name = StringField(_l('School Name'), validators=CommonForm.SCHOOL_NAME_VALIDATORS,
                              render_kw={'readonly': True})
    school_address = StringField(_l('School Address'), render_kw={'readonly': True})
    school_website = StringField(_l('School Website', validators=CommonForm.SCHOOL_URL_VALIDATORS),
                                 render_kw={'readonly': True})
    office_phone_number = StringField(_l('Office Phone Number', validators=CommonForm.OFFICE_PHONE_VALIDATORS),
                                      render_kw={'readonly': True})
    permission = BooleanField(_l('Permission'))
    submit = SubmitField(_l('Submit'))
