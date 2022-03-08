import os
from datetime import datetime

from flask_babel import _

from app import azure_blob, db
from app.models import Region


def populate_form_regions(form):
    form.region.choices = [(s.id, _(s.name))
                           for s in db.session.query(Region).all()]


def get_unique_photo_key_with_username(form, prefix, photo_field="photo"):
    return form.username.data + datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S"
    ) + prefix + form[photo_field].data.filename


def upload_to_azure_blob(form, photo, field_name="photo"):
    form[field_name].data.save(
        os.path.abspath('app/static/user/' + photo))
    # upload local file to blob
    azure_blob.save_image(blob_name="user/" + photo,
                          file_path=os.path.abspath('app/static/user/' +
                                                    photo))
    # remove local file
    os.remove(os.path.abspath('app/static/user/' + photo))
    # photo_path = os.path.abspath('app/static/storage/pictures/image/' + volunteer_photo)
    photo_path = azure_blob.get_img_url_with_blob_sas_token(
        "user/" + photo)
    return photo_path