import guilded
from guilded.ext import commands
from modules.generator import _check_values
from modules.generator import _check_inventory
from modules.generator import _check_inventory_member
from modules.generator import _check_values_member
from modules.generator import _check_values_server
from modules.generator import check_leaderboard
from modules.generator import check_leaderboard_author
from modules.generator import command_processed
from core.database import *
import psycopg
from psycopg_pool import ConnectionPool
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from tools.db_funcs import getAllUsers
from tools.db_funcs import getAllServers
from psycopg.rows import dict_row
from tools.dataIO import fileIO
import simplejson
import secrets
import string
import time

class API(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def activate(self, ctx, *, password: str=None):
		author = ctx.author
		server = ctx.server
		curr_time = time.time()
		if author.bot:
			return
		if password == None:
			em = guilded.Embed(title="Dashboard: [<@{}>]".format(author.id), description="The password argument cannot be empty.", color=0x363942)
			await ctx.reply(embed=em)
			return
		await _check_values(author)
		user = await getUser(author.id)
		try:
			takeaway = False
			with db_connection.connection() as conn:
				cursor = conn.cursor()
				for i in user["tokens"]["tokens"]:
					if user["tokens"]["tokens"][i]["password"] == password and user["tokens"]["tokens"][i]["token_active"] == False:
						user["tokens"]["tokens"][i]["token_active"] = True
						user["tokens"]["tokens"][i]["last_use"] = curr_time
						info = user["tokens"]
						infoJson = simplejson.dumps(info)
						cursor.execute(f"UPDATE users SET tokens = %s WHERE ID = '{author.id}'",  [infoJson])
						conn.commit()
						em = guilded.Embed(title="Dashboard: [<@{}>]".format(author.id), description="Token activated. Your token will expire 1 hour after it's latest use.", color=0x363942)
						await ctx.reply(embed=em)
						takeaway = True
					elif user["tokens"]["tokens"][i]["password"] == password and user["tokens"]["tokens"][i]["token_active"] == True:
						em = guilded.Embed(title="Dashboard: [<@{}>]".format(author.id), description="The token you're trying to activate is already activated.", color=0x363942)
						await ctx.reply(embed=em)
						takeaway = True
				if takeaway == False:
					em = guilded.Embed(title="Dashboard: [<@{}>]".format(author.id), description="Invalid password given.", color=0x363942)
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

def setup(bot):
	bot.add_cog(API(bot))
