import os

from peewee import MySQLDatabase
from peewee import Model


mysql_db = MySQLDatabase(
    os.getenv("DB_NAME"),
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    port = int(os.getenv("DB_PORT"), 10),
    password = os.getenv("DB_PASS")
)

class BaseModel(Model):
    class Meta:
        database:MySQLDatabase = mysql_db
