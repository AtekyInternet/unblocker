from peewee import *

from .base import BaseModel

class IpPool(BaseModel):
    description = CharField()
    pool = CharField()