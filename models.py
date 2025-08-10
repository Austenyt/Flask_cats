from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

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


class User(Base):
    email = CharField(unique=True)
    username = CharField(unique=True)
    password_hash = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db.connect()
db.create_tables((Cat, Breed, Gender))

if not Gender.select().exists():
    Gender.insert_many([
        {'name': 'Кот'},
        {'name': 'Кошка'}
    ]).execute()
