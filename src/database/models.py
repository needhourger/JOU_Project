from datetime import datetime
from peewee import *

db = SqliteDatabase("data.db")

class KeyReply(Model):
    kid = PrimaryKeyField()
    keyword = CharField(unique=True,index=True)
    reply = TextField()
    target = IntegerField(default=0)
    priority = IntegerField(default=0)
    enabled = BooleanField(default=True)
    created = DateTimeField(default = datetime.today())

    class Meta:
        database = db

class User(Model):
    uid = PrimaryKeyField()
    username = CharField(unique=True,index=True)
    password = CharField()
    created = DateTimeField(default = datetime.today())

    class Meta:
        database = db

class Prints(Model):
    uid = PrimaryKeyField()
    url = TextField()
    name = TextField()
    updated = DateTimeField(default = datetime.today())

    class Meta:
        database = db
