from peewee import *

from .base import BaseModel

class Ne(BaseModel):
    description = CharField()
    host = CharField()
    username = CharField()
    password = CharField()
    port = CharField()
    poolname = CharField()
    vendor = CharField()