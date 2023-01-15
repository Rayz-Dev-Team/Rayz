import psycopg
from psycopg_pool import ConnectionPool 
from core.database import *
from psycopg.rows import dict_row
import asyncio
import datetime

## Get User
## id = user id
async def getUser(id):
    #connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    #with connection.connection() as conn:
    #    cursor = conn.cursor(row_factory=dict_row)
    #    cursor.execute(f"SELECT * from users where id = '{id}'")
    #    user = cursor.fetchone()
    connection = psycopg.connect("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from users where id = '{id}'")
        user = cursor.fetchone()
    return user

# Get Server
# id = Server ID
async def getServer(id):
    #connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    #with connection.connection() as conn:
    #    cursor = conn.cursor(row_factory=dict_row)
    #    cursor.execute(f"SELECT * from servers where id = '{id}'")
    #    server = cursor.fetchone()
    connection = psycopg.connect("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from servers where id = '{id}'")
        server = cursor.fetchone()
    return server