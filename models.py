import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *
from flask_login import UserMixin

db = SqliteDatabase('social.db')


class User(UserMixin, Model):
    # User Model will inherit from UserMixin, which will give me default implementations of 3
    # attributes :is_authenticated, is_active, is_anonymous; and a method: get_id() which will by default return
    # unicode of integer id that is made by PeeWee by default
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    #  Hashing will usually be around 60 chars
    joined_at = DateTimeField(datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = db
        order_by = ('-joined_at',)
        # desc order, tuple

    # classmethod describes a method (that belongs to a class) that can create a the class it belongs to
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                is_admin = admin,
            )
        except IntegrityError:
            # IntegrityError will happen if username or email are not unique, as unique was set to True
            raise ValueError('User already exists')
