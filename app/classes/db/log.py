import datetime
from peewee import *


from .base import BaseModel
from .user import User

class Log(BaseModel):
    user = ForeignKeyField(User, backref='name')
    page = CharField()
    message = CharField()
    datetime = DateTimeField(default=datetime.datetime.now)

