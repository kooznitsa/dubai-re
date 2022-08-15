#!/usr/bin/python

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from db_info import *


connection = psycopg2.connect(**db_connection_info)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

create_database = 'create database ' + db_name + ';'
cursor.execute(create_database)