from flask_login import UserMixin
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

# from app import login

db = SqliteDatabase('cats.db')


class Base(Model):
    class Meta:
        database = db


class Breed(Base):
    name = CharField()


class Gender(Base):
    name = CharField(unique=True)


class Cat(Base):
    name = CharField()
    breed = ForeignKeyField(Breed)
    gender = ForeignKeyField(Gender)
    age = DecimalField()
    color = CharField()
    weight = DecimalField()
    temper = CharField()
    description = CharField(null=True)
    has_passport = BooleanField(default=False)
    image_path = CharField(null=True)


# class User(UserMixin, Base):
#     username = CharField(unique=True)
#     email = CharField(unique=True)
#     password_hash = CharField()
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# @login.user_loader
# def load_user(user_id):
#     return User.get_or_none(User.id == user_id)


db.connect()
db.create_tables((Cat, Breed, Gender))

if not Gender.select().exists():
    Gender.insert_many([
        {'name': 'Кот'},
        {'name': 'Кошка'}
    ]).execute()
