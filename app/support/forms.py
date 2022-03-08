from datetime import datetime

from flask_babel import lazy_gettext as _l
from wtforms import StringField, BooleanField, SubmitField, IntegerField, TextAreaField, \
    HiddenField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from app.common_form import CommonForm

now = datetime.now()


class AppointmentForm(CommonForm):
    id = HiddenField(_l('id'), render_kw={'readonly': True})
    student_name = StringField(_l('Student Name'), render_kw={'readonly': True},
                               validators=CommonForm.NAME_VALIDATORS)
    student_address = StringField(_l('Student Address'), render_kw={'readonly': True})
    student_phone_number = IntegerField(_l('Phone Number'), render_kw={'readonly': True},
                                        validators=CommonForm.PHONE_VALIDATORS)
    title = TextAreaField(_l('Problem'), render_kw={'readonly': True}, validators=CommonForm.TITTLE_VALIDATORS)
    description = TextAreaField(_l('Description Problem'), render_kw={'readonly': True},
                                validators=CommonForm.DESCRIPTION_VALIDATORS)
    # TODO will go pass time
    appointment_date = DateField(_l('Appointment Repair Data'), format="'%Y-%m-%d'", validators=[DataRequired()])
    appointment_time = TimeField(_l('Appointment Repair Time'), format="'%H:%M:%S'", validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class StoryPermissionForm(CommonForm):
    id = HiddenField(_l('id'), render_kw={'readonly': True})
    student_name = StringField(_l('Student Name'), render_kw={'readonly': True})
    title = TextAreaField(_l('Title'), render_kw={'readonly': True})
    story = TextAreaField(_l('Story'), render_kw={'readonly': True})
    item_name = StringField(_l('Item Name'), render_kw={'readonly': True})
    permission = BooleanField(_l('Permission'))
    submit = SubmitField(_l('Submit'))
