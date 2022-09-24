import asyncio
import psycopg2
from core.database import *

## Get User
## id = user id
async def getUser(id):
  connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
  cursor = connection.cursor()
  cursor.execute("SELECT * from users where id = '{id}'")
  user = cursor.fetchone()
  connection.close()
  return user