import psycopg2
import psycopg
from psycopg_pool import ConnectionPool 
from psycopg import connect, ClientCursor
from core.database import *

## Get User
## id = user id
async def getUser(id):
    connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from users where id = '{id}'")
        user = cursor.fetchone()
    return user

# Get Server
# id = Server ID
async def getServer(id):
    connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from servers where id = '{id}'")
        server = cursor.fetchone()
    return server
