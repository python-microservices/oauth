# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from project.models import db


class User(db.Model, UserMixin):
    __tablename__ = 'auth_user'
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, default="")
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, username, password):
        from project.views.oauth import bcrypt
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, 13
        ).decode()
