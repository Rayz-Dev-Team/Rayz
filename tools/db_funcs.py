import psycopg
from psycopg_pool import ConnectionPool 
from core.database import *
from psycopg.rows import dict_row
import asyncio
import datetime

## Get User :)
## id = user id
async def getUser(id):
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from users where id = '{id}'")
        user = cursor.fetchone()
    return user

async def getUserLB(id):
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from leaderboard where id = '{id}'")
        user = cursor.fetchone()
    return user

# Get Server
# id = Server ID :)
async def getServer(id):
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from servers where id = '{id}'")
        server = cursor.fetchone()
    return server

# Get all users
async def getAllUsers():
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from users")
        users = cursor.fetchall()
    return users

# Get all servers
async def getAllServers():
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * FROM servers")
        servers = cursor.fetchall()
    return servers

# Get all items
async def getAllItems():
    with db_connection.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from items")
        items = cursor.fetchall()
    return items

# Get an item
# id = Item 
async def getItem(id):
    with db_connection.connection() as conn:    
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute(f"SELECT * from items where item = '{id}'")
        item = cursor.fetchone()
    return item