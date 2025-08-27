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


class User(Base):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password_hash = CharField()


db.connect()
db.create_tables((Cat, Breed, Gender, User))

if not Gender.select().exists():
    Gender.insert_many([
        {'name': 'Кот'},
        {'name': 'Кошка'}
    ]).execute()
