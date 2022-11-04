import psycopg2
from core.database import *

## Get User
## id = user id
async def getUser(id):
  connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
  with connection:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from users where id = '{id}'")
    user = cursor.fetchone()
  return user

# Get Server
# id = Server ID
async def getServer(id):
  connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
  with connection:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from servers where id = '{id}'")
    server = cursor.fetchone()
  return server
