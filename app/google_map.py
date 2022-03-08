from app import db
from app.models import User, RepairApplication
import requests
from webconfig import googlemap
# from flask_googlemaps import get_coordinates
from app.student.email import confirm_token


def get_student_location():
    # coordinate = db.session.query(applyRepair.address, applyRepair.id).outerjoin(User, applyRepair.user_id == User.id).filter(
    #     applyRepair.confirm_button == False).all()
    coordinate = db.session.query(RepairApplication).filter_by(confirm_button=False).all()
    student_coordinate = {}
    title_list = ""
    y = 0
    count = 0

    for x in coordinate:
        # full_str = ' , '.join([str(elem) for elem in x])
        # print(x.address)
        student = 'student' + str(y)
        student_coordinate[student] = get_coordinates_by_address(googlemap.google_key, x.address)
        student_coordinate[student]['id'] = x.id
        y += 1
    # print(type(student_coordinate))
    return student_coordinate


def get_current_volunteer_location(username):
    json_data2 = {}
    # current_volunteer = db.session.query(Volunteer.address).outerjoin(User,
    #                                                                   Volunteer.user_id == User.username).filter_by(
    #     username=username).first()
    # print(current_volunteer)
    current_volunteer = db.session.query(User).filter_by(username=username).first()
    volunteer_coordinate = get_coordinates_by_address(googlemap.google_key, current_volunteer.volunteer.address)
    # print(volunteer_coordinate)
    y = 0
    list_location = []
    for x, c in volunteer_coordinate.items():
        user = 'volunteer' + str(y)
        json_data2[user] = c
        y += 1
    for key in json_data2:
        list_location.append(json_data2[key])
    return list_location


def get_coordinates_by_address(API_KEY, address_text):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + address_text
        + "&key="
        + API_KEY
    ).json()
    return response["results"][0]["geometry"]["location"]


# def get_address_by_coordinates(API_KEY, lat, lng):
#     response = requests.get(
#         "https://maps.googleapis.com/maps/api/geocode/json?latlng="
#         + lat
#         + ","
#         + lng
#         + "&key="
#         + API_KEY
#     ).json()
#     return response["results"][0]["formatted_address"]


def get_address_by_coordinates(API_KEY, lat, lon):
    # add_dict = dict()
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?latlng="
        + ",".join(map(str, [lat, lon]))
        + "&key="
        + API_KEY
    ).json()
    # add_dict["zip"] = response["results"][0]["address_components"][-1][
    #     "long_name"
    # ]
    # add_dict["country"] = response["results"][0]["address_components"][-2][
    #     "long_name"
    # ]
    # add_dict["state"] = response["results"][0]["address_components"][-3][
    #     "long_name"
    # ]
    # add_dict["city"] = response["results"][0]["address_components"][-4][
    #     "long_name"
    # ]
    # add_dict["locality"] = response["results"][0]["address_components"][-5][
    #     "long_name"
    # ]
    # add_dict["road"] = response["results"][0]["address_components"][-6][
    #     "long_name"
    # ]
    # add_dict["address"] = response["results"][0]["formatted_address"]
    return response["results"][0]["formatted_address"]

# def get_title():
#     title = db.session.query(applyRepair.title).outerjoin(User, applyRepair.user_id == User.id).filter(
#         applyRepair.confirm_button == False).all()
#     y = 0
#     student_title = ""
#
#     for x in title:
#         full_str = ' , '.join([str(elem) for elem in x])
#         student_title += full_str + '\n'
#         print(student_title)
#     return student_title
