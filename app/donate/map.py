from flask import url_for, render_template
from flask_babel import _
from flask_googlemaps import Map
from app import db

from app.models import EquipmentApplication, Equipment, EquipmentType, RepairApplication


def donate_map():
    # If you don't have foreign key, you need to use outerjoin to link between database stu_location =
    # db.session.query(stuMap.latitude, stuMap.longitude, Application.title).outerjoin(Application,
    # stuMap.application_id == Application.id).all()
    # If model have relationship, you can use the query as below
    # stu_locations = db.session.query(Application).filter_by(apply_status_id=2).order_by(Application.idtime).all()
    # stu_locations = db.session.query(applicationItem).first()
    # stu_locations = stu_locations.application.query.filter_by(apply_status_id=2).all()
    stu_locations = db.session.query(Equipment).join(EquipmentApplication).filter_by(apply_status_id=2).order_by(
        EquipmentApplication.created_at).all()
    # for loc in stu_locations:
    #     print(loc.application.title, loc.application.stu_location.latitude, loc.application.stu_location.longitude,
    #           loc.item.item_name)
    # reverse call using stuMap
    # stu_locations = db.session.query(stuMap).all()
    # (loc.latitude, loc.longitude, loc.application.title) for loc in stu_locations
    stu_story_map = Map(
        identifier="cluster-map",
        style="height:500px;width:1000px;margin:0;",
        lat=22.302711,
        lng=114.177216,
        markers=[(loc.application.stu_location.latitude, loc.application.stu_location.longitude,
                  render_template('donate/stumap_infobox.html', title=_('stu_info'), loc=loc)) for loc in
                 stu_locations],
        cluster=True,
        cluster_gridsize=60,
        zoom=11,
        cluster_imagepath=url_for('static', filename='map_icon/m')
    )
    return stu_story_map


def donate_filter_map(item_id):
    stu_locations = db.session.query(Equipment).join(EquipmentApplication).filter_by(apply_status_id=2).join(
        EquipmentType).filter_by(id=item_id).order_by(EquipmentApplication.created_at).all()
    # for loc in stu_locations:
    #     print(loc.application.title, loc.application.stu_location.latitude, loc.application.stu_location.longitude,
    #           loc.item.item_name)
    stu_story_map = Map(
        identifier="cluster-map",
        style="height:500px;width:1000px;margin:0;",
        # TODO current location
        lat=22.302711,
        lng=114.177216,
        markers=[(loc.application.stu_location.latitude, loc.application.stu_location.longitude,
                  render_template('donate/stumap_infobox.html', title=_('stu_info'), loc=loc)) for loc in
                 stu_locations],
        cluster=True,
        cluster_gridsize=60,
        zoom=11,
        cluster_imagepath=url_for('static', filename='map_icon/m')
    )
    return stu_story_map
