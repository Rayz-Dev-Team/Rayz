from modules.generator import _check_values_guild
import psycopg2
from core.database import *

database_name = config["database_name"]
database_port = config["database_port"]
database_password = config["database_password"]
database_username = config["database_username"]

async def prefix(bot, message):
	guild = message.guild
	await _check_values_guild(guild)
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		async def getGuild():
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
				content = cursor.fetchone()
			return content
		server = await getGuild()
		prefix = server[3]
		return [prefix, "@Rayz ", "@Rayz", "Rayz ", "Rayz"]
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')
