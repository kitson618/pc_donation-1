import enum
import re
import typing
from datetime import datetime
from time import time

import jwt
from flask import current_app, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Integer, Column, String, ForeignKey, Boolean, DateTime, Text, Float, FLOAT, Index, Enum
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, with_polymorphic, declarative_base, declared_attr, declarative_mixin
from sqlalchemy.util import timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app.azure_ai.translate import ai_translate


db = SQLAlchemy()


class StudentStatusEnum(enum.Enum):
    not_activated = 1
    student_activated_wait_for_teacher_approval = 2
    student_not_activated_and_teacher_approved = 3
    activated = 4


class EquipmentStatusEnum(enum.Enum):
    not_chosen_for_donate = 1
    selected_for_donate = 2
    pending_for_donate = 3
    donate_successful = 4


class EquipmentApplicationStatusEnum(enum.Enum):
    waiting_for_teacher_approval = 1
    teacher_approved = 2
    teacher_rejected = 3
    waiting_for_donation = 4
    confirming_donation = 5
    donation_complete = 6


class RepairApplicationStatusEnum(enum.Enum):
    pending = 1
    repairing = 2
    repaired = 3


class MeetUpMixIn(object):
    time = Column(DateTime, nullable=True)
    latitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    address = Column(String(220))
    Index("idx_location", latitude, longitude)


class ModelBase(AbstractConcreteBase, db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @declared_attr
    def __tablename__(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    @classmethod
    def repr(cls, *keys):
        keys = [str(k) for k in keys]
        return '<%s %s>' % (cls.__name__, ', '.join(keys))

    def __repr__(self) -> str:
        if __debug__:
            return "<{}({})>".format(
                self.__class__.__name__,
                ', '.join(
                    ["{}={}".format(k, repr(self.__dict__[k]))
                     for k in sorted(self.__dict__.keys())
                     if k[0] != '_']
                )
            )
        else:
            return self._repr(id=self.id)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            from sqlalchemy.orm.exc import DetachedInstanceError
            try:
                field_strings.append(f'{key}={field!r}')
            except DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __json__(self):
        return self.fields()

    def fields(self):
        fields = dict()
        for column in self.__table__.columns:
            fields[column.name] = getattr(self, column.name)
        return fields

    def keys(self):
        columns = self.__table__.primary_key.columns
        return tuple([getattr(self, c.name) for c in columns])

    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])


class User(ModelBase, UserMixin):
    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    user_type = Column('user_type', String(10))
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user',
        'with_polymorphic': '*'
    }

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), index=True)
    last_name = Column(String(120), index=True)
    username = Column(String(64), index=True, unique=True)
    _email = Column(String(120), index=True, unique=True)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()

    phone_number = Column(String(20), index=True)

    password_hash = Column(String(128))
    activated = Column(Boolean, default=False)

    last_seen = Column(DateTime, default=datetime.utcnow)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        jwt_id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        return session.get(User, jwt_id)


@login.user_loader
def load_user(current_user_id):
    all_users = with_polymorphic(User, '*')
    return session.get(all_users, current_user_id)


class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    teacher_email = Column(String(100))
    student_card_photo = Column(String(200))
    face_index = Column(String(200))

    user_photo = Column(String(150))
    about_me = Column(String(200))

    # 1 Student with 0...* EquipmentApplication
    equipment_applications = relationship("EquipmentApplication",
                                          uselist=True,
                                          back_populates="student")

    # 1 Student with 0...* RepairApplication
    repair_applications = relationship("RepairApplication",
                                       uselist=True,
                                       back_populates="student")

    latitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    Index("idx_location", latitude, longitude)

    # 1 Region with 0...* Student
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship("Region", back_populates="students", foreign_keys=[region_id])

    # 1 Teacher with 0...* Student
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable=True)
    teacher = relationship("Teacher", uselist=True, back_populates="students", foreign_keys=[teacher_id])

    status = Column(Enum(StudentStatusEnum))

    # 1 School with many Students
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    school = relationship("School", uselist=True, back_populates="students", foreign_keys=[school_id])

    # i student with 0...1 Story
    story = relationship("Story", uselist=False, back_populates="student")


class Teacher(User):
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # 1 School with many Teachers
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    school = relationship("School", uselist=False, back_populates="teachers", foreign_keys=[school_id])
    office_phone_number = Column(Integer, index=True, nullable=True)
    staff_card_photo = Column(String(200), nullable=True)
    user_photo = Column(String(150))

    # 1 Teacher with 0...* Student
    students = relationship('Student', uselist=False, back_populates='teacher', foreign_keys=[Student.teacher_id])


class Donor(User):
    __mapper_args__ = {
        'polymorphic_identity': 'donor'
    }
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_photo = Column(String(150))
    # 1 Donor with 0...* EquipmentApplication
    equipment_applications = relationship("EquipmentApplication",
                                          uselist=True,
                                          back_populates="donor")

    # 1 Donor with 0...* Equipment
    equipments = relationship('Equipment', uselist=True, back_populates='donor')
    

class Volunteer(User):
    __mapper_args__ = {
        'polymorphic_identity': 'volunteer'
    }
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_photo = Column(String(150))

    # 1 Volunteer with 0...* RepairApplication
    repair_applications = relationship("RepairApplication",
                                       uselist=True,
                                       back_populates="volunteer")


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)


class Region(ModelBase):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)

    # 1 Region with 0...* Student
    students = relationship('Student', uselist=True, back_populates='region', foreign_keys=[Student.region_id])


class EquipmentType(ModelBase):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)

    # 1 EquipmentType with 0...* Equipment
    equipments = relationship('Equipment', uselist=True, back_populates='equipment_type')


class Equipment(ModelBase):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    # 1 EquipmentApplication with 0...1 Equipment
    equipment_application = relationship("EquipmentApplication", back_populates="equipment",
                                         uselist=False)

    # 1 Donor with 0...* Equipment
    donor_id = Column(Integer, ForeignKey('donor.id'))
    donor = relationship("Donor", back_populates="equipments", foreign_keys=[donor_id])

    # 1 EquipmentType with 0...* Equipment
    equipment_type_id = Column(Integer, ForeignKey('equipment_type.id'))
    equipment_type = relationship("EquipmentType", back_populates="equipments", foreign_keys=[equipment_type_id])

    status = Column(Enum(EquipmentStatusEnum))


class EquipmentApplication(MeetUpMixIn, ModelBase):
    id = Column(Integer, primary_key=True)
    status = Column(Enum(EquipmentApplicationStatusEnum))
    home_photo = Column(String(200))

    # 1 Student with 0...* EquipmentApplication
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", uselist=False, back_populates="equipment_applications", foreign_keys=[student_id])

    # 1 Donor with 0...* EquipmentApplication
    donor_id = Column(Integer, ForeignKey('donor.id'), nullable=True)
    donor = relationship("Donor", uselist=False, back_populates="equipment_applications", foreign_keys=[donor_id])

    # 1 EquipmentApplication with 0...1 Equipment
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=True)
    equipment = relationship('Equipment',
                             back_populates='equipment_application',
                             uselist=False,
                             foreign_keys=[equipment_id])

    thanks_photo = Column(String(200), nullable=True)
    thanks_message = Column(String(200), nullable=True)

    # 1 EquipmentApplication with 0...1 Message
    messages = relationship('Message',
                            back_populates='equipment_application',
                            uselist=True)


# Student ask for Support
class RepairApplication(MeetUpMixIn, ModelBase):
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(String(240))
    status = Column(Enum(RepairApplicationStatusEnum))
    repair_photo = Column(String(200))

    # 1 Student with 0...* RepairApplication
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", uselist=False, back_populates="repair_applications", foreign_keys=[student_id])

    # 1 Volunteer with 0...* RepairApplication
    volunteer_id = Column(Integer, ForeignKey('volunteer.id'), nullable=True)
    volunteer = relationship("Volunteer", uselist=False, back_populates="repair_applications",
                             foreign_keys=[volunteer_id])

    thanks_photo = Column(String(200), nullable=True)
    thanks_message = Column(String(200), nullable=True)

    # 1 RepairApplication with 0...1 Message
    messages = relationship('Message',
                            back_populates='repair_application',
                            lazy='dynamic',
                            uselist=True)


class Message(ModelBase):
    id = Column(Integer, primary_key=True)
    message = Column(String(240))

    # 1 EquipmentApplication with 0...1 Message
    equipment_application_id = Column(Integer, ForeignKey('equipment_application.id'), nullable=True)
    equipment_application = relationship('EquipmentApplication',
                                         back_populates='messages',
                                         foreign_keys=[equipment_application_id])

    # 1 EquipmentApplication with 0...1 Message
    repair_application_id = Column(Integer, ForeignKey('repair_application.id'), nullable=True)
    repair_application = relationship('RepairApplication',
                                      back_populates='messages',
                                      foreign_keys=[repair_application_id])


class School(ModelBase):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    url = Column(String(100))
    # 1 School with many Students
    students = relationship('Student', back_populates='school', uselist=True)
    # 1 School with many Teachers
    teachers = relationship('Teacher', back_populates='school', uselist=True)


class Story(ModelBase):
    id = Column(Integer, primary_key=True)

    title = Column(String(100))
    title_zh_Hant = Column(String(100))
    title_en = Column(String(100))
    content = Column(Text)
    content_zh_Hant = Column(Text)
    content_en = Column(Text)
    urgency = Column(Float, index=True)
    approved = Column(Boolean, default=False)
    # i student with 0...1 Story
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="story")


@event.listens_for(Story, 'before_insert')
def translate_story_before_insert(mapper, connect, target):
    translate_story(target)


@event.listens_for(Story, 'before_update')
def translate_story_before_update(target, value, initiator):
    translate_story(target)


def translate_story(target):
    print(target)
    target.title_zh_Hant = ai_translate(target.story, "zh_Hant")[2]
    target.title_en = ai_translate(target.story, "en")[2]
    target.content_zh_Hant = ai_translate(target.story, "zh_Hant")[2]
    target.content_en = ai_translate(target.story, "en")[2]

