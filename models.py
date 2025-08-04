from peewee import *

db = SqliteDatabase('cats.db')


class Breed(Model):
    name = CharField()

    class Meta:
        database = db

class Gender(Model):
    name = CharField()

    class Meta:
        database = db

class Cat(Model):
    name = CharField()
    breed = ForeignKeyField(Breed)
    gender = ForeignKeyField(Gender)
    age = DecimalField()
    color = CharField()
    weight = DecimalField()
    temper = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables((Cat, Breed, Gender))
