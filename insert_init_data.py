from flask_babel import _

from app import SQLAlchemy, create_app
from app.models import Region, EquipmentType, Admin

app = create_app()
db = SQLAlchemy(app)


def region_data():
    try:
        r = ['Central and Western', 'Eastern', 'Southern', 'Wan Chai', 'Kowloon City', 'Kwun Tong', 'Sham Shui Po',
             'Wong Tai Sin', 'Yau Tsim Mong', 'Islands', 'Kwai Tsing', 'North', 'Sai Kung', 'Sha Tin', 'Tai Po',
             'Tsuen Wan', 'Tuen Mun', 'Yuen Long']
        db.session.add_all(list(map(lambda x: Region(name=x), r)))
        db.session.commit()
    except Exception as e:
        print(e)


def student_data():
    try:
        r = ['Desktop', 'Laptop', 'Router', 'SIM card', 'Keyboard', 'Mouse', 'Monitor', 'Microphone', 'Headphone',
             'Webcam', 'Tablet']

        db.session.add_all(list(map(lambda x: EquipmentType(name=x), r)))

        db.session.commit()
    except Exception as e:
        print(e)


def admin_data():
    try:
        admin_user = Admin(first_name="Cyrus", last_name="Wong", username="admin", email="vtcfyp123@gmail.com",
                           phone_number=12345678,
                           password_hash="pbkdf2:sha256:150000$OrIOj85q$14a802d85a098e7adcf905ad80d4d92bb4ab10176070242bc011b8bf18c28a56",
                           activated=True)
        db.session.add_all([admin_user])
        db.session.commit()
        print(admin_user)
    except Exception as e:
        print(e)


# the required data
region_data()
student_data()
admin_data()
