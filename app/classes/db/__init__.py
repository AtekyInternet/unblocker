
from .base import mysql_db as mysql_db
from .ip_pool import IpPool as IpPool
from .user import User as User
from .log import Log as Log
from .ne import Ne as Ne

with mysql_db:
    mysql_db.create_tables([User, Ne, IpPool, Log])