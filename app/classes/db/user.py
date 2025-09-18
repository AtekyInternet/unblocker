from peewee import *

from .base import BaseModel

class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    permission = IntegerField()
    active = BooleanField(default=True)
