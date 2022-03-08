from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, \
    TextAreaField, BooleanField, HiddenField, SelectField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from app.common_form import CommonForm


class WindowApply(CommonForm):
    need = BooleanField(_l('Need'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class ApplyStoryForm(CommonForm):
    title = StringField(_l('Please enter your title of your story to donator'), validators=CommonForm.TITTLE_VALIDATORS)
    your_story = TextAreaField(
        _l('Please elaborate your story about your life to make the donor is willing to donate items to you'),
        validators=CommonForm.STORY_VALIDATORS)
    photo = FileField(_l('Please Upload a photo about your life the photo will show to the donator'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l('Submit'))


class ThankMessageForm(CommonForm):
    # TODO what is default = 3
    apply_status = HiddenField(_l('apply_status'), render_kw={'readonly': True}, default=3)
    message_to_Donor = TextAreaField(_l('Please Enter Message To Your Donator'),
                                     validators=CommonForm.MESSAGE_VALIDATORS)
    message_to_Teacher = TextAreaField(_l('Please Enter Message To Your teacher '),
                                       validators=CommonForm.MESSAGE_VALIDATORS)
    message_to_Volunteer = TextAreaField(_l('Please Enter Message To Volunteer'),
                                         validators=CommonForm.MESSAGE_VALIDATORS)
    photo = FileField(_l('Photo'), validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l('Submit'))


class ThankToDonorForm(CommonForm):
    message_to_Donor = TextAreaField(_l('Please Enter Message To Your Donator'),
                                     validators=CommonForm.MESSAGE_VALIDATORS)
    photo = FileField(_l('Please upload a photo to confirm you are obtained the item'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l('Submit'))


class ThankToVolunteerForm(CommonForm):
    message_to_Volunteer = TextAreaField(_l('Please Enter Message To Your Volunteer'),
                                         validators=CommonForm.MESSAGE_VALIDATORS)
    photo = FileField(_l('Please upload pictures to confirm that there are volunteers to help repair'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l('Submit'))


class RepairForm(CommonForm):
    address = StringField(_l('Please Enter Your Address'))
    title = TextAreaField(_l('This is title.Please briefly describe what you need to repair let volunteer know.'),
                          validators=CommonForm.TITTLE_VALIDATORS)
    description = TextAreaField(
        _l('This is description. Please provide detailed information about the item you need to repair.'),
        validators=CommonForm.DESCRIPTION_VALIDATORS)
    photo = FileField(_l('Please upload photo of items you need to repair'),
                      validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l('Submit'))


class TestApplyForm(CommonForm):
    item = SelectField(_l('Please Choices Your Item'), validators=[DataRequired()], coerce=int)
    # TODO what is default 1 or 0
    quantity = HiddenField(_l('Please select your quantity'), default=1,
                           render_kw={'readonly': True})
    obtained = HiddenField(_l('Please select your quantity'), default=1,
                           render_kw={'readonly': True})
    donator = HiddenField(_l('Please select your quantity'), default=0,
                          render_kw={'readonly': True})

    submit = SubmitField(_l('Add Item'))


class DateForm(CommonForm):
    # TODO will go pass time
    appointment_date = DateField(_l('What date would be convenient for you?)'), format='%Y-%m-%d',
                                 validators=[DataRequired()])
    appointment_time = TimeField(_l('What time would be convenient for you? (AM/PM:HH:MM)'),
                                 validators=[DataRequired()])
    reason = TextAreaField(_l('Please tell your reason to donator.'), validators=CommonForm.MESSAGE_VALIDATORS)
    submit = SubmitField(_l('Send'))
