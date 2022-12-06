from modules.generator import _check_values_guild
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
	guild = message.guild
	await _check_values_guild(guild)
	server = await getServer(guild.id)
	prefix = server["server_prefix"]
	return [prefix, "@Rayz ", "@Rayz", "Rayz ", "Rayz"]