from datetime import datetime
from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileField
from wtforms import SubmitField, SelectField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from app.common_form import CommonForm

now = datetime.now()


class DonateForm(CommonForm):
    item = SelectField(_l('Please enter your Item Object'), validators=[DataRequired()], coerce=int)
    item_Status = SelectField(_l('Please enter your Item Status'), validators=[DataRequired()])
    photo = FileField(_l('Please upload your Item photo'), validators=CommonForm.IMAGE_VALIDATORS)
    # TODO: Remove if model event complete.
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    submit = SubmitField(_l('Add'))


class ItemForm(CommonForm):
    item = SelectField(_l('Please enter your Item Object'), validators=[DataRequired()],
                       render_kw={"onchange": "document.getElementById('show_img').src = this.value"})
    submit = SubmitField(_l('Select'))


class SelectedItemForm(CommonForm):
    item = SelectField(_l('Please enter your Item Object'), validators=[DataRequired()], render_kw={'readonly': True})


class DonateDateForm(CommonForm):
    #TODO: No past time!
    # https://stackoverflow.com/questions/56185306/how-to-validate-a-datefield-in-wtforms
    transaction_date = DateField(_l('Please enter your transaction date'), format="%Y-%m-%d",
                                 validators=[DataRequired()])
    transaction_time = TimeField(_l('Please enter your transaction time'), format="%H:%M:%S",
                                 validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


class SelectedDonateDateForm(CommonForm):
    # TODO: No past time!
    # https://stackoverflow.com/questions/56185306/how-to-validate-a-datefield-in-wtforms
    transaction_date = DateField(_l('Please enter your transaction date'), format="%Y-%m-%d",
                                 validators=[DataRequired()], render_kw={'readonly': True})
    transaction_time = TimeField(_l('Please enter your transaction time'), format="%H:%M:%S",
                                 validators=[DataRequired()], render_kw={'readonly': True})
    submit = SubmitField(_l('Cancel'))
