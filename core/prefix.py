from modules.generator import _check_values_server
from core.database import *
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row

database_name = config["database_name"]
database_port = config["database_port"]
database_password = config["database_password"]
database_username = config["database_username"]

async def prefix(bot, message):
	server = message.server
	await _check_values_server(server)
	server = await getServer(server.id)
	prefix = server["server_prefix"]
	return [prefix, "@Rayz ", "@Rayz", "Rayz ", "Rayz"]