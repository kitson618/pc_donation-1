from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField, \
    SelectField
from wtforms.validators import DataRequired
from app.common_form import CommonForm


class EditProfileForm(CommonForm):
    username = StringField(_l('Username'), validators=CommonForm.NEW_USERNAME_VALIDATORS, render_kw={'readonly': True})
    full_name = StringField(_l('Full Name'), validators=CommonForm.NAME_VALIDATORS)
    region = SelectField(_l('Region'), validators=[DataRequired()], coerce=int)
    phone_number = StringField(_l('Phone Number'),
                               validators=CommonForm.PHONE_VALIDATORS, render_kw={"placeholder": _l('phone_require')})
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
