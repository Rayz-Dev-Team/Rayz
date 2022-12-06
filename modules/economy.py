import guilded
from guilded.ext import commands
import typing
import json
import random
import math
import traceback
import time
from tools.dataIO import fileIO
from modules.generator import _check_values
from modules.generator import _check_inventory
from modules.generator import _check_inventory_member
from modules.generator import _check_values_member
from modules.generator import _check_values_guild
from modules.generator import check_leaderboard
from modules.generator import check_leaderboard_author
from modules.generator import command_processed
import psycopg
from psycopg_pool import ConnectionPool
from core.database import *
from tools.db_funcs import getUser
from tools.db_funcs import getServer
from psycopg.rows import dict_row
from tools.functions import paginate
from tools.functions import roll_chance

class Economy(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def tos(self, ctx:commands.Context):
		em = guilded.Embed(title="Rayz's ToS", description="__**A**__\n`a.1` `-` By inviting/using Rayz, you agree for it to save data using your UserID/ServerID.\n`a.2` `-` By being in a mutual server with Rayz and sending a message, you agree for it to save data using your UserID.\n`a.3` `-` To break down the above 2 lines, 'data' is refered to Rayz's economy system, and other misc.\n\n__**B**__\n`b.1` `-` Any abuse/usage of loopholes will subject in a **ban** via the Economy.\n`b.2` `-` By using Rayz's economy, you agree for your username, and data to be displayed in other servers.\n`b.3` `-` Alt accounts to farm 'coins' is **not** allowed.\n`b.4` `-` Any use of programs or automatic tools for farming will result in a **ban** via the Economy.\n\n__**C**__\n`c.1` `-` Repeated attempts to break/crash the bot is **not** allowed unless you are allowed by a Rayz developer.\n`c.2` `-` [Guilded's ToS is our ToS](https://support.guilded.gg/hc/en-us/articles/360039728313-Terms-of-Use)", color=0x363942)
		await ctx.reply(embed=em)

	#@commands.command()
	#async def test_values(self, ctx):
	#	author = ctx.author
	#	guild = ctx.guild
	#	await _check_values_guild(guild)
	#	try:
	#		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
	#		async def getUser():
	#			with connection:
	#				cursor = connection.cursor()
	#				cursor.execute(f"SELECT * FROM users")
	#				content = cursor.fetchall()
	#			return content
	#		user = await getUser()
	#		for i in user:
	#			new_account = i[10]
	#			try:
	#				for a in new_account["inventory"]["items"]:
	#					if "description" in new_account["inventory"]["items"][a]:
	#						del new_account["inventory"]["items"][a]["description"]
	#					if "display_name" in new_account["inventory"]["items"][a]:
	#						del new_account["inventory"]["items"][a]["display_name"]
	#				infoJson = json.dumps(new_account)
	#				cursor = connection.cursor()
	#				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{i[0]}'",  [infoJson])
	#				connection.commit()
	#				print(f"Moved halloween items for: {i[0]}")
	#			except:
	#				pass
	#		else:
	#			await ctx.reply(user[10])
	#		connection.close()
	#	except psycopg2.DatabaseError as e:
	#		em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
	#		await ctx.reply(embed=em)

	@commands.command()
	async def test2(self, ctx):
		author = ctx.author
		await _check_inventory(author)

	@commands.command()
	async def test1(self, ctx):
		author = ctx.author
		guild = await self.bot.fetch_server("Mldgz04R")
		await _check_values_guild(guild)
		roles_list = await author.fetch_role_ids()
		boost_or_not = False
		if 30053069 in roles_list:
			boost_or_not = True
		if boost_or_not:
			await ctx.reply("Has role")
		else:
			await ctx.reply("Doesn't have role")

	@commands.command()
	async def test(self, ctx):
		author = ctx.author
		guild = ctx.guild
		await _check_values_guild(guild)
		user = await getUser(author.id)
		print(user)
		if user["inventory"] == None or user["inventory"]["inventory"] == None:
			await ctx.reply("Is None")
		else:
			await ctx.reply(user["inventory"]["inventory"])

	@commands.command()
	async def add(self, ctx, member: guilded.Member=None, *, amount: int=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		DEV = fileIO("config/config.json", "load")
		await _check_values_guild(guild)
		if not author.id in DEV["Developer"]:
			return
		try:
			connection = asyncConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				cursor = conn.cursor()
				total_amount = user["bank"] + amount
				cursor.execute(f"UPDATE users SET bank = {total_amount} WHERE ID = '{member.id}'")
				conn.commit()
				connection.close()
				em = guilded.Embed(title="Woo hoo!".format(author.name), description="<@{}> has been given {:,} coins".format(member.id, amount), color=0x363942)
				await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def e_ban(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		DEV = fileIO("config/config.json", "load")
		await _check_values(author)
		await _check_values_guild(guild)
		if not author.id in DEV["Developer"]:
			return
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if member.id in LB_bans["bans"]:
			LB_bans["bans"].remove(member.id)
			fileIO("economy/bans.json", "save", LB_bans)
			em = guilded.Embed(title="Hurray!", description="<@{}> has been **unbanned** from the Economy.".format(member.id), color=0x363942)
			await ctx.reply(embed=em)
		elif not member.id in LB_bans["bans"]:
			LB_bans["bans"].append(member.id)
			fileIO("economy/bans.json", "save", LB_bans)
			em = guilded.Embed(title="Oh no :(", description="<@{}> has been **banned** from the Economy.".format(member.id), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def toggle_partner(self, ctx):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		DEV = fileIO("config/config.json", "load")
		if not author.id in DEV["Developer"]:
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				server = await getServer(guild.id)
				if server["partner_status"] == "False":
					cursor = conn.cursor()
					add_value = 0.25
					add_data = float(server["economy_multiplier"]) + add_value
					cursor.execute(f"UPDATE servers SET partner_status = 'True' WHERE ID = '{guild.id}'")
					cursor.execute(f"UPDATE servers SET economy_multiplier = '{add_data}' WHERE ID = '{guild.id}'")
					conn.commit()
					em = guilded.Embed(title="Woo hoo!".format(author.name), description="`-` {} is now partnered!\n`-` All partner benefits have been activated!".format(guild.name), color=0x363942)
					em.set_footer(text="This servers currency multiplier has been set to x{}".format(add_data))
					em.set_thumbnail(url="https://cdn.discordapp.com/attachments/546687295684870145/988278191678435378/guilded_image_4bd81f3a0067c6025ab935d019169b71.png")
					await ctx.reply(embed=em)
					connection.close()
				elif server["partner_status"] == "True":
					cursor = conn.cursor()
					neg_value = 0.25
					add_data = float(server["economy_multiplier"]) - neg_value
					cursor.execute(f"UPDATE servers SET partner_status = 'False' WHERE ID = '{guild.id}'")
					cursor.execute(f"UPDATE servers SET economy_multiplier = '{add_data}' WHERE ID = '{guild.id}'")
					conn.commit()
					em = guilded.Embed(title="Uh oh!".format(author.name), description="`-` {} is now un-partnered.\n`-` All partner benefits have been revoked!".format(guild.name), color=0x363942)
					em.set_footer(text="This servers currency multiplier has been set to x{}".format(add_data))
					await ctx.reply(embed=em)
					connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def prices(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		prices = fileIO("economy/prices.json", "load")
		item_list = fileIO("economy/items.json", "load")
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				info = user["inventory"]
				cursor = conn.cursor()
				current_item_list = []
				for i in info["inventory"]["items"]:
					current_item_list.append(i)
				say_list = []
				for key, i in prices["items"].items():
					if key in current_item_list:
						if info["inventory"]["items"][key]["amount"] > 0:
							say_list.append("{} - {:,} {}".format(item_list["items"][key]["display_name"], i["price"], economy_settings["currency_name"]))
				em = guilded.Embed(title="Prices list", description="Item - Price\n\n{}".format(" \n".join(say_list)), color=0x363942)
				em.set_footer(text="This only shows the items in your inventory that are currently sellable.")
				await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def sell(self, ctx, *, item: str=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		prices = fileIO("economy/prices.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if item == None:
			em = guilded.Embed(title="Uh oh!", description="Item cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				info = user["inventory"]
				cursor = conn.cursor()
				accepted_responses = []
				for key, i in prices["items"].items():
					accepted_responses.append(i["display_name"].lower())
					if i["display_name"].lower() == item.lower():
						em = guilded.Embed(description="How many would you like to sell?", color=0x363942)
						em.set_footer(text="Accepted response: Must be an integer.")
						await ctx.reply(embed=em)
						def pred(m):
							return m.message.author == message.author
						answer1 = await self.bot.wait_for("message", check=pred)
						try:
							if int(answer1.message.content) < 0:
								em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
								await ctx.reply(embed=em)
								return
							if int(answer1.message.content) > info["inventory"]["items"][key]["amount"]:
								em = guilded.Embed(title="Uh oh!", description="You don't have that much!", color=0x363942)
								await ctx.reply(embed=em)
							else:
								price_amount = prices["items"][key]["price"]
								total_amount = price_amount * int(answer1.message.content)
								pocket_before = user["pocket"]
								pocket_after = pocket_before + total_amount
								loss_amount = info["inventory"]["items"][key]["amount"] - int(answer1.message.content)
								info["inventory"]["items"][key]["amount"] = loss_amount
								infoJson = json.dumps(info)
								cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
								cursor.execute(f"UPDATE users SET pocket = '{pocket_after}' WHERE ID = '{author.id}'")
								conn.commit()
								em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s inventory.\n`-` <@{}> was given {:,} {}.".format(int(answer1.message.content), i["display_name"], author.id, author.id, total_amount, economy_settings["currency_name"]), color=0x363942)
								await ctx.reply(embed=em)
						except Exception as e:
							em = guilded.Embed(description="There was an error processing your command.", color=0x363942)
							em.set_footer(text="Accepted response: Must be an integer.")
							await ctx.reply(embed=em)
				if not item.lower() in accepted_responses:
					em = guilded.Embed(title="Uh oh!", description="That item cannot be sold.", color=0x363942)
					em.set_footer(text="Check the prices command to see what you can sell.")
					await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def give(self, ctx, item: str=None, amount: int=None, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		LB_bans = fileIO("economy/bans.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if item == None:
			em = guilded.Embed(title="Uh oh!", description="Item cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if amount == None:
			em = guilded.Embed(title="Uh oh!", description="Amount cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if amount < 0:
			em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
			await ctx.reply(embed=em)
			return
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="Member cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		await _check_inventory_member(member)
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				member1 = await getUser(member.id)
				info = user["inventory"]
				accepted_responses = ["jolly_ranchers", "candycorn", "nerds", "dots"]
				cursor = conn.cursor()
				if item.lower() in accepted_responses:
					if amount > info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"]:
						em = guilded.Embed(title="Uh oh!", description="You don't have that much!", color=0x363942)
						await ctx.reply(embed=em)
					else:
						info_member = member1["inventory"]
						#Take from info
						info_amount = info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"]
						new_info_amount = info_amount - amount
						info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"] = new_info_amount
						infoJson = json.dumps(info)
						cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
						#Give to info_member
						info_member_amount = info_member["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"]
						new_info_member_amount = info_member_amount + amount
						info_member["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"] = new_info_member_amount
						infoJsonMember= json.dumps(info_member)
						cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJsonMember])
						conn.commit()
						em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s inventory.\n`-` <@{}> was given {:,} {}.".format(amount, item.lower(), author.id, member.id, amount, item.lower()), color=0x363942)
						em.set_footer(text="All transfers are logged in order to keep track of alt account farming, which is against our Economy ToS.")
						await ctx.reply(embed=em)
						guild1 = await self.bot.fetch_server("Mldgz04R")
						channel = await guild1.fetch_channel("22048e41-bcfc-49e9-a1fa-5b57171299bb")
						em = guilded.Embed(title="A transfer was made", description="{}[{}] gifted {}[{}] {:,} {}.".format(author.name, author.id, member.name, member.id, amount, item.lower()), color=0x363942)
						await channel.send(embed=em)
					connection.close()
				else:
					em = guilded.Embed(title="Uh oh!", description="That item doesn't exist!\n\n__**Accepted items:**__\n{}".format(" \n".join(accepted_responses)), color=0x363942)
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def gift(self, ctx, amount: int=None, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		LB = fileIO("config/economy_settings.json", "load")
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if amount == None:
			em = guilded.Embed(title="Uh oh!", description="Amount cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		if amount < 0:
			em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
			await ctx.reply(embed=em)
			return
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="Member cannot be NoneType.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				member1 = await getUser(member.id)
				server = await getServer(guild.id)
				prefix = server["server_prefix"]
				if amount > user["pocket"]:
					em = guilded.Embed(title="Uh oh!", description="`You don't have {:,} in your pocket.".format(amount), color=0x363942)
					await ctx.reply(embed=em)
					return
				else:
					if member1 == None:
						await _check_values_member(member)
					cursor = conn.cursor()
					reducted_amount = user["pocket"] - amount
					new_amount = member1["pocket"] + amount
					cursor.execute(f"UPDATE users SET pocket = {reducted_amount} WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET pocket = {new_amount} WHERE ID = '{member.id}'")
					conn.commit()
					em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s pocket.\n`-` <@{}> was given {:,} {}.".format(amount, economy_settings["currency_name"], author.id, member.id, amount, economy_settings["currency_name"]), color=0x363942)
					em.set_footer(text="All transfers are logged in order to keep track of alt account farming, which is against our Economy ToS.")
					await ctx.reply(embed=em)
					guild1 = await self.bot.fetch_server(economy_settings["support_server_id"])
					channel = await guild1.fetch_channel("82204345-aa8d-487f-8808-17afc525a735")
					em = guilded.Embed(title="A transfer was made", description="{}[{}] gifted {}[{}] {:,} {}.".format(author.name, author.id, member.name, member.id, amount, economy_settings["currency_name"]), color=0x363942)
					await channel.send(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command(aliases=["with"])
	async def withdraw(self, ctx, amount: str=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				if amount.lower() == "all":
					if user["bank"] <= 0:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, your bank balance is 0.".format(author.id), color=0x363942)
						await ctx.reply(embed=em)
						return
					bank_bal = user["bank"]
					bank_bal = bank_bal
					pocket_val = user["pocket"]
					pocket_val = pocket_val
					new_pocket_val = pocket_val + bank_bal
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET bank = 0 WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET pocket = {new_pocket_val} WHERE ID = '{author.id}'")
					conn.commit()
					connection.close()
					em = guilded.Embed(title="Bank:", description="<@{}>, you withdrew {:,} {} from your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
					await ctx.reply(embed=em)
				else:
					if user[3] <= 0:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, your bank balance is 0.".format(author.id), color=0x363942)
						await ctx.reply(embed=em)
						return
					if int(amount) > user["bank"]:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, you don't have {:,} {} in your bank to withdraw.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
						await ctx.reply(embed=em)
						return
					bank_bal = int(amount)
					pocket_val = user["pocket"]
					pocket_val = pocket_val
					new_pocket_val = pocket_val + bank_bal
					new_bank_bal = user["bank"] - int(amount)
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET bank = {new_bank_bal} WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET pocket = {new_pocket_val} WHERE ID = '{author.id}'")
					conn.commit()
					connection.close()
					em = guilded.Embed(title="Bank:", description="<@{}>, you withdrew {:,} {} from your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command(aliases=["dep"])
	async def deposit(self, ctx, amount: str=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			if author.id in LB["tracker"]:
				del LB["tracker"][author.id]
				fileIO("config/economy_settings.json", "save", LB)
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				if amount.lower() == "all":
					if user["pocket"] <= 0:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, your pocket balance is 0.".format(author.id), color=0x363942)
						await ctx.reply(embed=em)
						return
					bank_bal = user["pocket"]
					bank_new_bal = user["bank"] + user["pocket"]
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET bank = '{bank_new_bal}' WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET pocket = 0 WHERE ID = '{author.id}'")
					conn.commit()
					connection.close()
					em = guilded.Embed(title="Bank:", description="<@{}>, you deposited {:,} {} into your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
					await ctx.reply(embed=em)
				else:
					if user["pocket"] <= 0:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, your pocket balance is 0.".format(author.id), color=0x363942)
						await ctx.reply(embed=em)
						return
					if int(amount) > user["pocket"]:
						em = guilded.Embed(title="Uh oh!", description="<@{}>, you don't have {:,} {} in your pocket into deposit.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
						await ctx.reply(embed=em)
						return
					bank_bal = user["bank"] + int(amount)
					pocket_val = user["pocket"] - int(amount)
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET bank = '{bank_bal}' WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET pocket = {pocket_val} WHERE ID = '{author.id}'")
					conn.commit()
					connection.close()
					em = guilded.Embed(title="Bank:", description="<@{}>, you deposited {:,} {} into your bank.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	# Time to start commenting the code. :)
	# Below we add a page argument and default it to 1 if it's not provided
	@commands.command(aliases=["lb"])
	async def leaderboard(self, ctx, page: typing.Optional[int] = 1):
		# We need to know where to offset our query by if the number is greater than 1
		# We need it to be greater because we need to start at 0 otherwise
		offset = (page - 1) * 10 if page > 1 else 0

		if page < 1:
			page = 1

		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			connection.close()
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:

				async def getUserLB():
					with connection:
						cursor = conn.cursor()
						# We don't use all the data so we're not going to bother to fetch all the values.
						cursor.execute(f"SELECT name, currency FROM leaderboard ORDER BY currency DESC LIMIT 10 OFFSET {offset}")
						result = cursor.fetchall()
						# We want the total of all users in the leaderboard
						cursor.execute('SELECT COUNT(*) from leaderboard')
						total = cursor.fetchone()
						# We return both in an array for ease of use
					return [result,total]

				[LB,total] = await getUserLB()
				[description, numOfPages] = paginate(LB,total[0],page)

				if page > numOfPages:
					em = guilded.Embed(title="Uh oh!", description="You provided a page number that does not exist", color=0x363942)
					await ctx.reply(embed=em)
					connection.close()
					return

				# We're now importing this function
				user = await getUser(author.id)

				em = guilded.Embed(title="Global leaderboard:".format(author.name), description=description, color=0x363942)
				# Add our footer with the page we're on out of the total
				em.set_footer(text=f"Page {page}/{numOfPages}")
				await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def rob(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="The member argument was left empty.\n\nEx: `{}rob <member>`".format(prefix), color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
			return
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await _check_inventory_member(member)
		await command_processed(message, author)
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				server = await getServer(guild.id)
				economy_settings = fileIO("config/economy_settings.json", "load")
				LB_bans = fileIO("economy/bans.json", "load")
				if author.id in LB_bans["bans"]:
					em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
					await ctx.reply(embed=em)
					connection.close()
					return
				prefix = server["server_prefix"]
				if author == member:
					em = guilded.Embed(title="Uh oh!", description="You cannot rob yourself. Smhhhhhhh", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
					return
				user = await getUser(author.id)
				member1 = await getUser(member.id)
				if member1 == None:
					await _check_values_member(member)
				if user == None:
					await _check_values(author)
				curr_time = time.time()
				delta = float(curr_time) - float(user["rob_timeout"])
				if delta >= 900.0 and delta>0:
					if user["pocket"] >= 250:
						if member1[6] < 250:
							em = guilded.Embed(title="Uh oh!", description="<@{}> doesn't have x250 or more {} in their pocket.".format(member.id, economy_settings["currency_name"]), color=0x363942)
							em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
							await ctx.reply(embed=em)
						else:
							num = random.randint(1, 10)
							num = num
							random_rob = random.randint(1, 250)
							random_rob = random_rob
							new_member_calc = member1["pocket"] - random_rob
							new_user_calc = user["pocket"] + random_rob
							new_user_calc_caught = user["pocket"] - random_rob
							if num > 6:
								cursor = conn.cursor()
								cursor.execute(f"UPDATE users SET pocket = '{new_member_calc}' WHERE ID = '{member.id}'")
								cursor.execute(f"UPDATE users SET pocket = '{new_user_calc}' WHERE ID = '{author.id}'")
								cursor.execute(f"UPDATE users SET rob_timeout = '{curr_time}' WHERE ID = '{author.id}'")
								conn.commit()
								connection.close()
								em = guilded.Embed(title="Nice!", description="<@{}> successfully robbed <@{}> for x{} {}.".format(author.id, member.id, random_rob, economy_settings["currency_name"]), color=0x363942)
								await ctx.reply(embed=em)
							else:
								cursor = conn.cursor()
								cursor.execute(f"UPDATE users SET rob_timeout = '{curr_time}' WHERE ID = '{author.id}'")
								cursor.execute(f"UPDATE users SET pocket = '{new_user_calc_caught}' WHERE ID = '{author.id}'")
								conn.commit()
								connection.close()
								em = guilded.Embed(title="Oh no :(", description="<@{}> got caught robbing <@{}> and got fined for x{} {}.".format(author.id, member.id, random_rob, economy_settings["currency_name"]), color=0x363942)
								await ctx.reply(embed=em)
					else:
						em = guilded.Embed(title="Uh oh!", description="You need more than x250 {} in your pocket to rob someone.".format(economy_settings["currency_name"]), color=0x363942)
						em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						await ctx.reply(embed=em)
				else:
					seconds = 900 - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot rob someone yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def weekly(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
		members_support_guild = await support_guild.fetch_members()
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				server = await getServer(guild.id)
				if user == None:
					await _check_values(author)
				gen_amount = random.randint(5000, 12000)
				multiplier_amount = float(server["economy_multiplier"])
				edit_message = None
				if author in members_support_guild:
					author_support_guild = await support_guild.fetch_member(author.id)
					roles_list = await author_support_guild.fetch_role_ids()
					if 30053086 in roles_list:
						edit_message = ":Gold_tier: Elite supporter boosted you by `x3`"
						multiplier_amount += 3
					elif 30053078 in roles_list:
						edit_message = ":Silver_tier: Epic supporter boosted you by `x2`"
						multiplier_amount += 2
					elif 30053069 in roles_list:
						edit_message = ":Copper_tier: Supporter boosted you by `x1.5`"
						multiplier_amount += 1.5
					else:
						pass
				gen_amount = gen_amount * int(multiplier_amount)
				gen_amount = math.ceil(gen_amount)
				curr_time = time.time()
				curr_cooldown = 604800
				delta = float(curr_time) - float(user[7])
				if delta >= curr_cooldown and delta>0:
					if author in members_support_guild:
						author_support_guild = await support_guild.fetch_member(author.id)
						roles_list = await author_support_guild.fetch_role_ids()
						if 30053086 in roles_list or 30053078 in roles_list or 30053069 in roles_list:
							em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!\n\n{}".format(author.id, gen_amount, economy_settings["currency_name"], edit_message), color=0x363942)
						else:
							em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!".format(author.id, gen_amount, economy_settings["currency_name"]), color=0x363942)
					else:
						em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!".format(author.id, gen_amount, economy_settings["currency_name"]), color=0x363942)
					if server["economy_multiplier"] > 1:
						em.set_footer(text="The multiplier in this server boosted you by x{}".format(server["economy_multiplier"]))
					await ctx.reply(embed=em)
					gen_amount = user["pocket"] + gen_amount
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET pocket = '{gen_amount}' WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET weekly_timeout = '{curr_time}' WHERE ID = '{author.id}'")
					conn.commit()
					await check_leaderboard_author(author)
				else:
					seconds = curr_cooldown - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					d, h = divmod(h, 24)
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot get your weekly bonus yet.\n`Time left:` {}d {}m {}s".format(author.id, int(d), int(m), int(s)), color=0x363942)
					await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def slots(self, ctx, *, amount: int=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_drops = fileIO("economy/drops.json", "load")
		item_list = fileIO("economy/items.json", "load")
		support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
		members_support_guild = await support_guild.fetch_members()
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				server = await getServer(guild.id)
				prefix = server["server_prefix"]

				slots_bet_min = economy_settings["slots_bet_min"]
				slots_bet_max = economy_settings["slots_bet_max"]

				slots_win_multiplier = economy_settings["slots_win_multiplier"]
				slots_jackpot_multiplier = economy_settings["slots_jackpot_multiplier"]

				slots_win_min = economy_settings["slots_win_min"]
				slots_win_max = economy_settings["slots_win_max"]
				slots_win_chance = economy_settings["slots_win_chance"]

				slots_jackpot_min = economy_settings["slots_jackpot_min"]
				slots_jackpot_max = economy_settings["slots_jackpot_max"]
				slots_jackpot_chance = economy_settings["slots_jackpot_chance"]
				curr_time = time.time()
				if server[4] == "True":
					curr_cooldown = 5
				else:
					curr_cooldown = 10
				delta = float(curr_time) - float(user["slots_timeout"])
				if delta >= curr_cooldown and delta>0:
					if amount == None:
						em = guilded.Embed(title="Welcome to slots", description="**__Goal__**\n`-` Get `x3💰` to win.\n`-` Get `x3💎` to win a JACKPOT.\n\n**__Payouts__**\nWin `-` x{} bonus.\nJACKPOT `-` x{} bonus\n\nUse `{}slots <amount>` to place a bet.".format(slots_win_multiplier, slots_jackpot_multiplier, prefix), color=0x363942)
						await ctx.reply(embed=em)
						return
					if amount < slots_bet_min or amount > slots_bet_max:
						em = guilded.Embed(title="Uh oh!", description="Your bet was out of range. Acceptable range is `{:,}-{:,}`".format(slots_bet_min, slots_bet_max), color=0x363942)
						await ctx.reply(embed=em)
						return
					if amount > user["pocket"]:
						em = guilded.Embed(title="Uh oh!", description="You don't have {:,} in your pocket.".format(amount), color=0x363942)
						await ctx.reply(embed=em)
						return
					cursor = conn.cursor()
					row_1 = []
					row_2 = []
					row_3 = []
					display_output = []
					multiplier_amount = 0
					win_bool = False
					for i in range(3):
						row_1_item_list = ['💚', '💜', '🖤']
						row_1_chance_win = random.randint(slots_win_min, slots_win_max)
						row_1_chance_jackpot = random.randint(slots_jackpot_min, slots_jackpot_max)
						if row_1_chance_win <= slots_win_chance:
							row_1_item_list.append('💰')
						if row_1_chance_jackpot == slots_jackpot_chance:
							row_1_item_list.append('💎')
						row_1_a = random.choice(row_1_item_list)
						row_1.append(row_1_a)
						#ROW 2
						row_2_item_list = ['💚', '💜', '🖤']
						row_2_chance_win = random.randint(slots_win_min, slots_win_max)
						row_2_chance_jackpot = random.randint(slots_jackpot_min, slots_jackpot_max)
						if row_2_chance_win <= slots_win_chance:
							row_2_item_list.append('💰')
						if row_2_chance_jackpot == slots_jackpot_chance:
							row_2_item_list.append('💎')
						row_2_a = random.choice(row_2_item_list)
						row_2.append(row_2_a)
						#ROW 3
						row_3_item_list = ['💚', '💜', '🖤']
						row_3_chance_win = random.randint(slots_win_min, slots_win_max)
						row_3_chance_jackpot = random.randint(slots_jackpot_min, slots_jackpot_max)
						if row_3_chance_win <= slots_win_chance:
							row_3_item_list.append('💰')
						if row_3_chance_jackpot == slots_jackpot_chance:
							row_3_item_list.append('💎')
						row_3_a = random.choice(row_3_item_list)
						row_3.append(row_3_a)
					if row_1.count('💰') == 3:
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1.count('💎') ==3:
						multiplier_amount += slots_jackpot_multiplier
					if row_2.count('💰') == 3:
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_2.count('💎') ==3:
						multiplier_amount += slots_jackpot_multiplier
					if row_3.count('💰') == 3:
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_3.count('💎') ==3:
						multiplier_amount += slots_jackpot_multiplier
						win_bool = True
					if row_1[0] == '💰' and row_2[0] == '💰' and row_3[0] == '💰':
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1[1] == '💰' and row_2[1] == '💰' and row_3[1] == '💰':
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1[2] == '💰' and row_2[2] == '💰' and row_3[2] == '💰':
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1[0] == '💰' and row_2[1] == '💰' and row_3[2] == '💰':
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1[2] == '💰' and row_2[1] == '💰' and row_3[0] == '💰':
						multiplier_amount += slots_win_multiplier
						win_bool = True
					if row_1[0] == '💎' and row_2[0] == '💎' and row_3[0] == '💎':
						multiplier_amount += slots_jackpot_multiplier
						win_bool = True
					if row_1[1] == '💎' and row_2[1] == '💎' and row_3[1] == '💎':
						multiplier_amount += slots_jackpot_multiplier
						win_bool = True
					if row_1[2] == '💎' and row_2[2] == '💎' and row_3[2] == '💎':
						multiplier_amount += slots_jackpot_multiplier
						win_bool = True
					if row_1[0] == '💎' and row_2[1] == '💎' and row_3[2] == '💎':
						multiplier_amount += slots_jackpot_multiplier
						win_bool = True
					if row_1[2] == '💎' and row_2[1] == '💎' and row_3[0] == '💎':
						multiplier_amount += slots_jackpot_multiplier
					if win_bool == True:
						win_amount = amount * multiplier_amount
						display_output.append(f"**Slots:**\n{row_1[0]}{row_1[1]}{row_1[2]}\n{row_2[0]}{row_2[1]}{row_2[2]}\n{row_3[0]}{row_3[1]}{row_3[2]}")
						em = guilded.Embed(title="WIN!", description="{}\n\n<@{}> WON {}".format(" \n".join(display_output), author.id, win_amount), color=0x363942)
						await ctx.reply(embed=em)
						pocket_amount = user["pocket"] + win_amount
						cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
						conn.commit()
					elif win_bool == False:
						display_output.append(f"**Slots:**\n{row_1[0]}{row_1[1]}{row_1[2]}\n{row_2[0]}{row_2[1]}{row_2[2]}\n{row_3[0]}{row_3[1]}{row_3[2]}")
						em = guilded.Embed(title="Lose", description="{}\n\n<@{}> lost a bet of {}".format(" \n".join(display_output), author.id, amount), color=0x363942)
						await ctx.reply(embed=em)
						pocket_amount = user["pocket"] - amount
						cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
						cursor.execute(f"UPDATE users SET slots_timeout = '{curr_time}' WHERE ID = '{author.id}'")
						conn.commit()
				else:
					seconds = curr_cooldown - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot use slots yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
					await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	async def dig(self, ctx:commands.Context):
		if ctx.author.bot:
			return
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		await command_processed(message, author)

		LB_bans = fileIO("economy/bans.json", "load")

		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			economy_settings = fileIO("config/economy_settings.json", "load")
			item_drops = fileIO("economy/dig.json", "load")
			item_list = fileIO("economy/items.json", "load")

			common_min = economy_settings["common_min"]
			common_max = economy_settings["common_max"]
			common_chance = economy_settings["common_chance"]

			rare_min = economy_settings["rare_min"]
			rare_max = economy_settings["rare_max"]
			rare_chance = economy_settings["rare_chance"]

			epic_min = economy_settings["epic_min"]
			epic_max = economy_settings["epic_max"]
			epic_chance = economy_settings["epic_chance"]

			legendary_min = economy_settings["legendary_min"]
			legendary_max = economy_settings["legendary_max"]
			legendary_chance = economy_settings["legendary_chance"]

			unreal_min = economy_settings["unreal_min"]
			unreal_max = economy_settings["unreal_max"]
			unreal_chance = economy_settings["unreal_chance"]

			# Static is so you can pull the original chance range amount (So it can easily be changed)
			static_drop_slot_chance = economy_settings["dig_drop_slots_chance"]

			# Drained meaning the part that will be decreased (Pulled from Static)
			drained_drop_slot_chance = static_drop_slot_chance

			# How much the required range for a valid drop decreases by
			decrease_drop_slot_chance = economy_settings["dig_drop_slots_chance_decrease"]

			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				server = await getServer(guild.id)
				if user == None:
					await _check_values(author)
				curr_time = time.time()
				curr_cooldown = 30

				info = user["inventory"]

				delta = float(curr_time) - float(user["dig_timeout"])
				if delta >= curr_cooldown and delta>0:
					if "shovel" in info["inventory"]["items"]:
						if info["inventory"]["items"]["shovel"]["amount"] > 0:
							message_list = []
				
							drop_slots = 0
							drop_slots_fail = False
							drop_counter = 1

							def calculatedropslots():
								nonlocal drop_slots_fail
								nonlocal drop_slots
								nonlocal drained_drop_slot_chance
								nonlocal static_drop_slot_chance
								nonlocal decrease_drop_slot_chance
								if drop_slots_fail == False:
									gen_for_drop = roll_chance(1, static_drop_slot_chance, drained_drop_slot_chance)
									if gen_for_drop:
										drained_drop_slot_chance = drained_drop_slot_chance - decrease_drop_slot_chance
										drop_slots += 1
										return calculatedropslots
									else:
										drop_slots_fail = True

							while drop_slots_fail == False:
								calculatedropslots()

							drops_lines_list = []
							for i in range(drop_slots):
								common_chance_gen = roll_chance(common_min, common_max, common_chance)
								rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
								epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
								legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
								unreal_chance_gen = roll_chance(unreal_min, unreal_max, unreal_chance)
								if unreal_chance_gen:
									drop_list = []
									for i in item_drops["unreal"]:
										drop_list.append(i)
									drop = random.choice(drop_list)
									amount = random.randint(item_drops["unreal"][drop]["min_amount"], item_drops["unreal"][drop]["max_amount"])
									if not drop in info["inventory"]["items"]:
										info["inventory"]["items"][drop] = {
											"amount": amount
										}
										new_amount = amount
										drops_lines_list.append("`{}.` [UNREAL] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
									else:
										new_amount = info["inventory"]["items"][drop]["amount"] + amount
										info["inventory"]["items"][drop]["amount"] += amount
										drops_lines_list.append("`{}.` [UNREAL] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
								elif legendary_chance_gen:
									drop_list = []
									for i in item_drops["legendary"]:
										drop_list.append(i)
									drop = random.choice(drop_list)
									amount = random.randint(item_drops["legendary"][drop]["min_amount"], item_drops["legendary"][drop]["max_amount"])
									if not drop in info["inventory"]["items"]:
										info["inventory"]["items"][drop] = {
											"amount": amount
										}
										new_amount = amount
										drops_lines_list.append("`{}.` [LEGENDARY] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
									else:
										new_amount = info["inventory"]["items"][drop]["amount"] + amount
										info["inventory"]["items"][drop]["amount"] += amount
										drops_lines_list.append("`{}.` [LEGENDARY] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
								elif epic_chance_gen:
									drop_list = []
									for i in item_drops["epic"]:
										drop_list.append(i)
									drop = random.choice(drop_list)
									amount = random.randint(item_drops["epic"][drop]["min_amount"], item_drops["epic"][drop]["max_amount"])
									if not drop in info["inventory"]["items"]:
										info["inventory"]["items"][drop] = {
											"amount": amount
										}
										new_amount = amount
										drops_lines_list.append("`{}.` [Epic] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
									else:
										new_amount = info["inventory"]["items"][drop]["amount"] + amount
										info["inventory"]["items"][drop]["amount"] += amount
										drops_lines_list.append("`{}.` [Epic] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
								elif rare_chance_gen:
									drop_list = []
									for i in item_drops["rare"]:
										drop_list.append(i)
									drop = random.choice(drop_list)
									amount = random.randint(item_drops["rare"][drop]["min_amount"], item_drops["rare"][drop]["max_amount"])
									if not drop in info["inventory"]["items"]:
										info["inventory"]["items"][drop] = {
											"amount": amount
										}
										new_amount = amount
										drops_lines_list.append("`{}.` [Rare] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
									else:
										new_amount = info["inventory"]["items"][drop]["amount"] + amount
										info["inventory"]["items"][drop]["amount"] += amount
										drops_lines_list.append("`{}.` [Rare] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
								elif common_chance_gen:
									drop_list = []
									for i in item_drops["common"]:
										drop_list.append(i)
									drop = random.choice(drop_list)
									amount = random.randint(item_drops["common"][drop]["min_amount"], item_drops["common"][drop]["max_amount"])
									if not drop in info["inventory"]["items"]:
										info["inventory"]["items"][drop] = {
											"amount": amount
										}
										new_amount = amount
										drops_lines_list.append("`{}.` [Common] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
										drop_counter += 1
									else:
										new_amount = info["inventory"]["items"][drop]["amount"] + amount
										info["inventory"]["items"][drop]["amount"] += amount
										drops_lines_list.append("`{}.` [Common] +{} {}".format(drop_counter, amount,item_list["items"][drop]["display_name"]))
										drop_counter += 1
								else:
									drops_lines_list.append("`{}.` Nothing found.".format(drop_counter))
									drop_counter += 1

							if not drops_lines_list == []:
								message_list.append("__**Item drop:**__\n{}\n".format(" \n".join(drops_lines_list)))

							em = guilded.Embed(title="{} went digging.".format(author.name), description="{}".format(" \n".join(message_list)), color=0x363942)
							await ctx.reply(embed=em)
							info["inventory"]["items"]["shovel"]["amount"] = info["inventory"]["items"]["shovel"]["amount"] - 1
							infoJson = json.dumps(info)
							cursor = conn.cursor()
							cursor.execute(f"UPDATE users SET dig_timeout = '{curr_time}' WHERE ID = '{author.id}'")
							cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
							conn.commit()
							await check_leaderboard_author(author)
							connection.close()
						else:
							em = guilded.Embed(description="<@{}>, you don't have a Shovel to dig with.".format(author.id), color=0x363942)
							em.set_footer(text="Working is a good way to get items.")
							await ctx.reply(embed=em)
					else:
						em = guilded.Embed(description="<@{}>, you don't have a Shovel to dig with.".format(author.id), color=0x363942)
						em.set_footer(text="Working is a good way to get items.")
						await ctx.reply(embed=em)
				else:
					seconds = curr_cooldown - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot dig yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
					await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)


	@commands.command()
	async def work(self, ctx:commands.Context):
		if ctx.author.bot:
			return
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		await command_processed(message, author)

		LB_bans = fileIO("economy/bans.json", "load")

		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			economy_settings = fileIO("config/economy_settings.json", "load")
			item_drops = fileIO("economy/drops.json", "load")
			item_list = fileIO("economy/items.json", "load")

			support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
			members_support_guild = await support_guild.fetch_members()

			common_min = economy_settings["common_min"]
			common_max = economy_settings["common_max"]
			common_chance = economy_settings["common_chance"]

			rare_min = economy_settings["rare_min"]
			rare_max = economy_settings["rare_max"]
			rare_chance = economy_settings["rare_chance"]

			epic_min = economy_settings["epic_min"]
			epic_max = economy_settings["epic_max"]
			epic_chance = economy_settings["epic_chance"]

			legendary_min = economy_settings["legendary_min"]
			legendary_max = economy_settings["legendary_max"]
			legendary_chance = economy_settings["legendary_chance"]

			unreal_min = economy_settings["unreal_min"]
			unreal_max = economy_settings["unreal_max"]
			unreal_chance = economy_settings["unreal_chance"]

			tier_1_sub_role_id = economy_settings["tier_1_sub_role_id"]
			tier_2_sub_role_id = economy_settings["tier_2_sub_role_id"]
			tier_3_sub_role_id = economy_settings["tier_3_sub_role_id"]

			tier_1_sub_boost_amount = economy_settings["tier_1_sub_boost_amount"]
			tier_2_sub_boost_amount = economy_settings["tier_2_sub_boost_amount"]
			tier_3_sub_boost_amount = economy_settings["tier_3_sub_boost_amount"]

			# Static is so you can pull the original chance range amount (So it can easily be changed)
			static_drop_slot_chance = economy_settings["drop_slots_chance"]

			# Drained meaning the part that will be decreased (Pulled from Static)
			drained_drop_slot_chance = static_drop_slot_chance

			# How much the required range for a valid drop decreases by
			decrease_drop_slot_chance = economy_settings["drop_slots_chance_decrease"]

			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				server = await getServer(guild.id)
				if user == None:
					await _check_values(author)
				curr_time = time.time()
				if server["partner_status"] == "True":
					curr_cooldown = 20
				else:
					curr_cooldown = 60
				delta = float(curr_time) - float(user["work_timeout"])
				if delta >= curr_cooldown and delta>0:
					message_list = []
					booster_amount = 0
					if author in members_support_guild:
						author_support_guild = await support_guild.fetch_member(author.id)
						roles_list = await author_support_guild.fetch_role_ids()
						if tier_3_sub_role_id in roles_list:
							booster_amount += tier_3_sub_boost_amount
						elif tier_2_sub_role_id in roles_list:
							booster_amount += tier_2_sub_boost_amount
						elif tier_1_sub_role_id in roles_list:
							booster_amount += tier_1_sub_boost_amount


					drop_slots = 0
					drop_slots_fail = False
					drop_counter = 1

					def calculatedropslots():
						nonlocal drop_slots_fail
						nonlocal drop_slots
						nonlocal drained_drop_slot_chance
						nonlocal static_drop_slot_chance
						nonlocal decrease_drop_slot_chance
						if drop_slots_fail == False:
							gen_for_drop = roll_chance(1, static_drop_slot_chance, drained_drop_slot_chance)
							if gen_for_drop:
								drained_drop_slot_chance = drained_drop_slot_chance - decrease_drop_slot_chance
								drop_slots += 1
								return calculatedropslots
							else:
								drop_slots_fail = True

					while drop_slots_fail == False:
						calculatedropslots()

					multiplier_amount = float(server["economy_multiplier"]) + booster_amount
					gen_amount = random.randint(15, 150) * int(multiplier_amount)
					gen_amount = math.ceil(gen_amount)
					message_list.append("<@{}> gained {:,} {}!\n".format(author.id, gen_amount, economy_settings["currency_name"]))
					info = user["inventory"]
					thanksgiving_drop_lines_list = []
					if economy_settings["thanksgiving_event"] == "True":
						common_chance_gen = roll_chance(common_min, common_max, common_chance)
						rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
						epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
						legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
						unreal_chance_gen = roll_chance(unreal_min, unreal_max, unreal_chance)
						turkey_gen_amount = random.randint(1, 2)
						if legendary_chance_gen:
							if not "golden_turkey" in info["inventory"]["items"]:
								info["inventory"]["items"]["golden_turkey"] = {
									"amount": turkey_gen_amount
								}
								new_amount = turkey_gen_amount
								thanksgiving_drop_lines_list.append("`-` [LEGENDARY] +{} {}".format(amount, item_list["items"]["golden_turkey"]["display_name"]))
							else:
								new_amount = info["inventory"]["items"]["golden_turkey"]["amount"] + amount
								info["inventory"]["items"]["golden_turkey"]["amount"] += amount
								thanksgiving_drop_lines_list.append("`-` [LEGENDARY] +{} {}".format(amount, item_list["items"]["golden_turkey"]["display_name"]))
						else:
							thanksgiving_drop_lines_list.append("Nothing found.")

					if economy_settings["halloween_event"] == "True":
						common_chance_gen = roll_chance(common_min, common_max, common_chance)
						rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
						epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
						legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
						unreal_chance_gen = roll_chance(unreal_min, unreal_max, unreal_chance)
						candycorn_gen_amount = random.randint(1, 10)
						work_event_lines_list = []
						if common_chance_gen <= common_chance:
							info["inventory"]["items"]["candycorn"]["amount"] += candycorn_gen_amount
							work_event_lines_list.append(f"[Common] +{candycorn_gen_amount} Candycorn")
						if rare_chance_gen <= rare_chance:
							rare_amount = random.randint(1, 10)
							work_event_lines_list.append(f"[Rare] +{rare_amount} Jolly ranchers")
							info["inventory"]["items"]["jolly_ranchers"]["amount"] += rare_amount
						if epic_chance_gen == epic_chance:
							epic_amount = random.randint(1, 10)
							work_event_lines_list.append(f"[Epic] +{epic_amount} Nerds")
							info["inventory"]["items"]["nerds"]["amount"] += epic_amount
						if legendary_chance_gen == legendary_chance:
							legendary_amount = random.randint(1, 10)
							work_event_lines_list.append(f"[LEGENDARY] +{legendary_amount} Dots")
							info["inventory"]["items"]["dots"]["amount"] += legendary_amount
						if not work_event_lines_list == []:
							message_list.append("__**Halloween event bonus:**__\n{}\n".format(" \n".join(work_event_lines_list)))
					drops_lines_list = []
					for i in range(drop_slots):
						common_chance_gen = roll_chance(common_min, common_max, common_chance)
						rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
						epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
						legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
						unreal_chance_gen = roll_chance(unreal_min, unreal_max, unreal_chance)
						if unreal_chance_gen:
							drop_list = []
							for i in item_drops["unreal"]:
								drop_list.append(i)
							drop = random.choice(drop_list)
							amount = random.randint(item_drops["unreal"][drop]["min_amount"], item_drops["unreal"][drop]["max_amount"])
							if not drop in info["inventory"]["items"]:
								info["inventory"]["items"][drop] = {
									"amount": amount
								}
								new_amount = amount
								drops_lines_list.append("`{}.` [UNREAL] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
							else:
								new_amount = info["inventory"]["items"][drop]["amount"] + amount
								info["inventory"]["items"][drop]["amount"] += amount
								drops_lines_list.append("`{}.` [UNREAL] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
						elif legendary_chance_gen:
							drop_list = []
							for i in item_drops["legendary"]:
								drop_list.append(i)
							drop = random.choice(drop_list)
							amount = random.randint(item_drops["legendary"][drop]["min_amount"], item_drops["legendary"][drop]["max_amount"])
							if not drop in info["inventory"]["items"]:
								info["inventory"]["items"][drop] = {
									"amount": amount
								}
								new_amount = amount
								drops_lines_list.append("`{}.` [LEGENDARY] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
							else:
								new_amount = info["inventory"]["items"][drop]["amount"] + amount
								info["inventory"]["items"][drop]["amount"] += amount
								drops_lines_list.append("`{}.` [LEGENDARY] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
						elif epic_chance_gen:
							drop_list = []
							for i in item_drops["epic"]:
								drop_list.append(i)
							drop = random.choice(drop_list)
							amount = random.randint(item_drops["epic"][drop]["min_amount"], item_drops["epic"][drop]["max_amount"])
							if not drop in info["inventory"]["items"]:
								info["inventory"]["items"][drop] = {
									"amount": amount
								}
								new_amount = amount
								drops_lines_list.append("`{}.` [Epic] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
							else:
								new_amount = info["inventory"]["items"][drop]["amount"] + amount
								info["inventory"]["items"][drop]["amount"] += amount
								drops_lines_list.append("`{}.` [Epic] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
						elif rare_chance_gen:
							drop_list = []
							for i in item_drops["rare"]:
								drop_list.append(i)
							drop = random.choice(drop_list)
							amount = random.randint(item_drops["rare"][drop]["min_amount"], item_drops["rare"][drop]["max_amount"])
							if not drop in info["inventory"]["items"]:
								info["inventory"]["items"][drop] = {
									"amount": amount
								}
								new_amount = amount
								drops_lines_list.append("`{}.` [Rare] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
							else:
								new_amount = info["inventory"]["items"][drop]["amount"] + amount
								info["inventory"]["items"][drop]["amount"] += amount
								drops_lines_list.append("`{}.` [Rare] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
						elif common_chance_gen:
							drop_list = []
							for i in item_drops["common"]:
								drop_list.append(i)
							drop = random.choice(drop_list)
							amount = random.randint(item_drops["common"][drop]["min_amount"], item_drops["common"][drop]["max_amount"])
							if not drop in info["inventory"]["items"]:
								info["inventory"]["items"][drop] = {
									"amount": amount
								}
								new_amount = amount
								drops_lines_list.append("`{}.` [Common] +{} {}".format(drop_counter, amount, item_list["items"][drop]["display_name"]))
								drop_counter += 1
							else:
								new_amount = info["inventory"]["items"][drop]["amount"] + amount
								info["inventory"]["items"][drop]["amount"] += amount
								drops_lines_list.append("`{}.` [Common] +{} {}".format(drop_counter, amount,item_list["items"][drop]["display_name"]))
								drop_counter += 1
						else:
							drops_lines_list.append("`{}.` Nothing found.".format(drop_counter))
							drop_counter += 1

					if not thanksgiving_drop_lines_list == []:
						message_list.append("__**Thanksgiving event drop:**__\n`-` {}\n".format(" \n".join(thanksgiving_drop_lines_list)))

					if not drops_lines_list == []:
						message_list.append("__**Item drop:**__\n{}\n".format(" \n".join(drops_lines_list)))

					if author in members_support_guild:
						author_support_guild = await support_guild.fetch_member(author.id)
						roles_list = await author_support_guild.fetch_role_ids()
						if tier_3_sub_role_id in roles_list:
							edit_message = ":Gold_tier: Elite supporter boosted you by `x{}`".format(tier_3_sub_boost_amount)
							message_list.append(edit_message)
						elif tier_2_sub_role_id in roles_list:
							edit_message = ":Silver_tier: Epic supporter boosted you by `x{}`".format(tier_2_sub_boost_amount)
							message_list.append(edit_message)
						elif tier_1_sub_role_id in roles_list:
							edit_message = ":Copper_tier: Supporter boosted you by `x{}`".format(tier_1_sub_boost_amount)
							message_list.append(edit_message)
					if server["partner_status"] == "True":
						edit_message = ":handshake: Server partner boosted you by `x{}`".format(float(server["economy_multiplier"]))
						message_list.append(edit_message)
					em = guilded.Embed(title="{} has worked.".format(author.name), description="{}".format(" \n".join(message_list)), color=0x363942)
					em.set_footer(text="You were boosted by x{}".format(multiplier_amount))
					await ctx.reply(embed=em)
					pocket_amount = user["pocket"] + gen_amount
					infoJson = json.dumps(info)
					cursor = conn.cursor()
					cursor.execute(f"UPDATE users SET work_timeout = '{curr_time}' WHERE ID = '{author.id}'")
					cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
					cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
					conn.commit()
					await check_leaderboard_author(author)
					connection.close()
				else:
					seconds = curr_cooldown - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot work yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
					await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	#Obv know what this is
	@commands.command(aliases=["me", "bal", "balance"])
	async def profile(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				if user == None:
					await _check_values(author)
				bank_code = user["bank_access_code"]
				em = guilded.Embed(title="{}'s bank information".format(author.name), description="__**Currency**__\n`Pocket:` x{:,} {}\n`Bank:` x{:,} {}\n`Bank secure:` {}\n`Bank access code:` {}{}{}{}{}xxxxxxxxxxxxxxxxxxxxxxxxxxx".format(user["pocket"], economy_settings["currency_name"], user["bank"], economy_settings["currency_name"], user["bank_secure"], bank_code[0], bank_code[1], bank_code[2], bank_code[3], bank_code[4]), color=0x363942)
				await ctx.reply(embed=em)
				conn.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command(aliases=["inventory"])
	async def inv(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		await _check_inventory(author)
		await command_processed(message, author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.reply(embed=em)
			return
		try:
			connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
			with connection.connection() as conn:
				user = await getUser(author.id)
				server = await getServer(guild.id)
				prefix = server["server_prefix"]
				if user == None:
					await _check_values(author)
				info = user["inventory"]
				default_print_list = []
				for key, i in info["inventory"]["items"].items():
					if i["amount"] > 0:
						default_print_list.append("[{}] `{}:` {:,}".format(item_list["items"][key]["rarity"], item_list["items"][key]["display_name"], i["amount"], item_list["items"][key]["description"]))
				if default_print_list == []:
					default_print_list.append("None")
				em = guilded.Embed(title="Inventory".format(author.name), description="{}".format(" \n".join(default_print_list)), color=0x363942)
				await ctx.reply(embed=em)
				connection.close()
		except psycopg.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.reply(embed=em)

	#Get guild stats, is partner, and booster multiplier
	@commands.command()
	async def stats(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		if author.bot:
			return
		await _check_values_guild(guild)
		await command_processed(message, author)
		server = await getServer(guild.id)
		em = guilded.Embed(title="Guild stats:", description="**Partner:** {}\n**Multiplier:** x{}".format(server["partner_status"], server["economy_multiplier"]), color=0x363942)
		await ctx.reply(embed=em)

def setup(bot):
	bot.add_cog(Economy(bot))