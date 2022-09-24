import guilded
from guilded.ext import commands
import typing
import asyncio
import json
import aiohttp
import random 
import math
import time
import os
import glob
import datetime
import operator
from collections import OrderedDict
from tools.dataIO import fileIO
from modules.generator import _check_values
from modules.generator import _check_values_member
from modules.generator import _check_values_guild
from modules.generator import check_leaderboard
from modules.generator import check_leaderboard_author
import re
import psycopg2
from psycopg2 import Error
from core.database import *
from psycopg2.extras import Json
from tools.db_funcs import getUser
from tools.db_funcs import getServer
from tools.functions import paginate
from tools.functions import roll_chance

class Economy(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def tos(self, ctx):
		em = guilded.Embed(title="Rayz's ToS", description="`-` By inviting/using Rayz, you agree for it to save data using your UserID/ServerID.\n`-` By being in a mutual server with Rayz and sending a message, you agree for it to save data using your UserID.\n`-` To break down the above 2 lines, 'data' is refered to Rayz's economy system, and other misc.\n\n__**Rayz's Economy ToS**__\n`-` Any abuse/usage of loopholes will subject in a **ban** via the Economy.\n`-` By using Rayz's economy, you agree for your username, and data to be displayed in other servers.\n`-` Alt accounts to farm 'coins' is **not** allowed.\n\n__**Rayz's base ToS**__ (Relates to the entire bot.)\n`-` Repeated attempts to break/crash the bot is **not** allowed unless you are allowed by a Rayz developer.\n`-` [Guilded's ToS is our ToS](https://support.guilded.gg/hc/en-us/articles/360039728313-Terms-of-Use)", color=0x363942)
		await ctx.send(embed=em)

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
	#			if i[10] == None:
	#				new_account = {
	#					"inventory": {
	#						"items": {},
	#						"seasonal_items": {
	#							"halloween": {
	#								"candycorn": {
	#									"amount": 0,
	#									"description": "[Common] Part of the 2022 Halloween event series.",
	#									"display_name": "Candycorn"
	#								},
	#								"jolly_ranchers": {
	#									"amount": 0,
	#									"description": "[Rare] Part of the 2022 Halloween event series.",
	#									"display_name": "Jolly ranchers"
	#								},
	#								"nerds": {
	#									"amount": 0,
	#									"description": "[Epic] Part of the 2022 Halloween event series.",
	#									"display_name": "Nerds"
	#								},
	#								"dots": {
	#									"amount": 0,
	#									"description": "[LEGENDARY] Part of the 2022 Halloween event series.",
	#									"display_name": "Dots"
	#								}
	#							},
	#							"christmas": {},
	#							"easter": {},
	#							"thanksgiving": {}
	#						},
	#						"consumables": {}
	#					}
	#				}
	#				infoJson = json.dumps(new_account)
	#				cursor = connection.cursor()
	#				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{i[0]}'",  [infoJson])
	#				connection.commit()
	#				print(f"New inventory made for: {i[0]}")
	#		else:
	#			await ctx.send(user[10])
	#		connection.close()
	#	except psycopg2.DatabaseError as e:
	#		em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
	#		await ctx.send(embed=em)

	@commands.command()
	async def test2(self, ctx):
		author = ctx.author
		guild = ctx.guild
		pog = author.joined_at()
		await ctx.send(pog)

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
			await ctx.send("Has role")
		else:
			await ctx.send("Doesn't have role")

	@commands.command()
	async def test(self, ctx):
		author = ctx.author
		guild = ctx.guild
		await _check_values_guild(guild)
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			if user[10] == None:
				await ctx.send("Is None")
			else:
				await ctx.send(user[10])
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

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
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			cursor = connection.cursor()
			total_amount = user[3] + amount
			cursor.execute(f"UPDATE users SET bank = {total_amount} WHERE ID = '{member.id}'")
			connection.commit()
			connection.close()
			em = guilded.Embed(title="Woo hoo!".format(author.name), description="<@{}> has been given {:,} coins".format(member.id, amount), color=0x363942)
			await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

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
			await ctx.send(embed=em)
		elif not member.id in LB_bans["bans"]:
			LB_bans["bans"].append(member.id)
			fileIO("economy/bans.json", "save", LB_bans)
			em = guilded.Embed(title="Oh no :(", description="<@{}> has been **banned** from the Economy.".format(member.id), color=0x363942)
			await ctx.send(embed=em)

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
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			if server[4] == "False":
				cursor = connection.cursor()
				add_value = 0.25
				add_data = float(server[5]) + add_value
				cursor.execute(f"UPDATE servers SET partner_status = 'True' WHERE ID = '{guild.id}'")
				cursor.execute(f"UPDATE servers SET economy_multiplier = '{add_data}' WHERE ID = '{guild.id}'")
				connection.commit()
				em = guilded.Embed(title="Woo hoo!".format(author.name), description="`-` {} is now partnered!\n`-` All partner benefits have been activated!".format(guild.name), color=0x363942)
				em.set_footer(text="This servers currency multiplier has been set to x{}".format(add_data))
				em.set_thumbnail(url="https://cdn.discordapp.com/attachments/546687295684870145/988278191678435378/guilded_image_4bd81f3a0067c6025ab935d019169b71.png")
				await ctx.send(embed=em)
				connection.close()
			elif server[4] == "True":
				cursor = connection.cursor()
				neg_value = 0.25
				add_data = float(server[5]) - neg_value
				cursor.execute(f"UPDATE servers SET partner_status = 'False' WHERE ID = '{guild.id}'")
				cursor.execute(f"UPDATE servers SET economy_multiplier = '{add_data}' WHERE ID = '{guild.id}'")
				connection.commit()
				em = guilded.Embed(title="Uh oh!".format(author.name), description="`-` {} is now un-partnered.\n`-` All partner benefits have been revoked!".format(guild.name), color=0x363942)
				em.set_footer(text="This servers currency multiplier has been set to x{}".format(add_data))
				await ctx.send(embed=em)
				connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def prices(self, ctx):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		prices = fileIO("economy/prices.json", "load")
		item_list = fileIO("economy/items.json", "load")
		say_list = []
		for key, i in prices["items"].items():
			say_list.append("{} - {:,} {}".format(item_list["items"][key]["display_name"], i["price"], economy_settings["currency_name"]))
		em = guilded.Embed(title="Prices list", description="Item - Price\n\n{}".format(" \n".join(say_list)), color=0x363942)
		await ctx.send(embed=em)

	@commands.command()
	async def sell(self, ctx, item: str=None, amount: int=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		prices = fileIO("economy/prices.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		if item == None:
			em = guilded.Embed(title="Uh oh!", description="Item cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount == None:
			em = guilded.Embed(title="Uh oh!", description="Amount cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount < 0:
			em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			info = user[10]
			accepted_responses = ["jolly_ranchers", "candycorn", "nerds", "dots"]
			cursor = connection.cursor()
			if item.lower() in accepted_responses:
				if amount > info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"]:
					em = guilded.Embed(title="Uh oh!", description="You don't have that much!", color=0x363942)
					await ctx.send(embed=em)
				else:
					price_amount = prices["items"][item.lower()]["price"]
					total_amount = price_amount * amount
					pocket_before = user[6]
					pocket_after = pocket_before + total_amount
					loss_amount = info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"] - amount
					info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"] = loss_amount
					infoJson = json.dumps(info)
					cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
					cursor.execute(f"UPDATE users SET pocket = '{pocket_after}' WHERE ID = '{author.id}'")
					connection.commit()
					em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s inventory.\n`-` <@{}> was given {:,} {}.".format(amount, item.lower(), author.id, author.id, total_amount, economy_settings["currency_name"]), color=0x363942)
					await ctx.send(embed=em)
			else:
				em = guilded.Embed(title="Uh oh!", description="That item doesn't exist!\n\n__**Accepted items:**__\n{}".format(" \n".join(accepted_responses)), color=0x363942)
				await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def give(self, ctx, item: str=None, amount: int=None, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		if item == None:
			em = guilded.Embed(title="Uh oh!", description="Item cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount == None:
			em = guilded.Embed(title="Uh oh!", description="Amount cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount < 0:
			em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
			await ctx.send(embed=em)
			return
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="Member cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			member1 = await getUser(member.id)
			info = user[10]
			accepted_responses = ["jolly_ranchers", "candycorn", "nerds", "dots"]
			cursor = connection.cursor()
			if item.lower() in accepted_responses:
				if amount > info["inventory"]["seasonal_items"]["halloween"][item.lower()]["amount"]:
					em = guilded.Embed(title="Uh oh!", description="You don't have that much!", color=0x363942)
					await ctx.send(embed=em)
				else:
					info_member = member1[10]
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
					connection.commit()
					em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s inventory.\n`-` <@{}> was given {:,} {}.".format(amount, item.lower(), author.id, member.id, amount, item.lower()), color=0x363942)
					em.set_footer(text="All transfers are logged in order to keep track of alt account farming, which is against our Economy ToS.")
					await ctx.send(embed=em)
					guild1 = await self.bot.fetch_server("Mldgz04R")
					channel = await guild1.fetch_channel("22048e41-bcfc-49e9-a1fa-5b57171299bb")
					em = guilded.Embed(title="A transfer was made", description="{}[{}] gifted {}[{}] {:,} {}.".format(author.name, author.id, member.name, member.id, amount, item.lower()), color=0x363942)
					await channel.send(embed=em)
				connection.close()
			else:
				em = guilded.Embed(title="Uh oh!", description="That item doesn't exist!\n\n__**Accepted items:**__\n{}".format(" \n".join(accepted_responses)), color=0x363942)
				await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def gift(self, ctx, amount: int=None, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount == None:
			em = guilded.Embed(title="Uh oh!", description="Amount cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		if amount < 0:
			em = guilded.Embed(title="Nice try!", description="__**This bug was already found by:**__\n`-` Chicken [mqE6EKXm]\n`-` ItzNxthaniel [xd9ZOzpm]", color=0x363942)
			await ctx.send(embed=em)
			return
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="Member cannot be NoneType.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			member1 = await getUser(member.id)
			server = await getServer(guild.id)
			prefix = server[3]
			if amount > user[6]:
				em = guilded.Embed(title="Uh oh!", description="`You don't have {:,} in your pocket.".format(amount), color=0x363942)
				await ctx.send(embed=em)
				return
			else:
				if member1 == None:
					await _check_values_member(member)
				cursor = connection.cursor()
				reducted_amount = user[6] - amount
				new_amount = member1[6] + amount
				cursor.execute(f"UPDATE users SET pocket = {reducted_amount} WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET pocket = {new_amount} WHERE ID = '{member.id}'")
				connection.commit()
				em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s pocket.\n`-` <@{}> was given {:,} {}.".format(amount, LB["currency_name"], author.id, member.id, amount, LB["currency_name"]), color=0x363942)
				em.set_footer(text="All transfers are logged in order to keep track of alt account farming, which is against our Economy ToS.")
				await ctx.send(embed=em)
				guild1 = await self.bot.fetch_server("Mldgz04R")
				channel = await guild1.fetch_channel("82204345-aa8d-487f-8808-17afc525a735")
				em = guilded.Embed(title="A transfer was made", description="{}[{}] gifted {}[{}] {:,} {}.".format(author.name, author.id, member.name, member.id, amount, LB["currency_name"]), color=0x363942)
				await channel.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command(aliases=["with"])
	async def withdraw(self, ctx, amount: str=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			if amount.lower() == "all":
				if user[3] <= 0:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, your bank balance is 0.".format(author.id), color=0x363942)
					await ctx.send(embed=em)
					return
				bank_bal = user[3]
				bank_bal = bank_bal
				pocket_val = user[6]
				pocket_val = pocket_val
				new_pocket_val = pocket_val + bank_bal
				cursor = connection.cursor()
				cursor.execute(f"UPDATE users SET bank = 0 WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET pocket = {new_pocket_val} WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
				em = guilded.Embed(title="Bank:", description="<@{}>, you withdrew x{} {} from your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
				await ctx.send(embed=em)
			else:
				if user[3] <= 0:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, your bank balance is 0.".format(author.id), color=0x363942)
					await ctx.send(embed=em)
					return
				if int(amount) > user[3]:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you don't have x{} {} in your bank to withdraw.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
					await ctx.send(embed=em)
					return
				bank_bal = int(amount)
				pocket_val = user[6]
				pocket_val = pocket_val
				new_pocket_val = pocket_val + bank_bal
				new_bank_bal = user[3] - int(amount)
				cursor = connection.cursor()
				cursor.execute(f"UPDATE users SET bank = {new_bank_bal} WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET pocket = {new_pocket_val} WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
				em = guilded.Embed(title="Bank:", description="<@{}>, you withdrew x{} {} from your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
				await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command(aliases=["dep"])
	async def deposit(self, ctx, amount: str=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			if author.id in LB["tracker"]:
				del LB["tracker"][author.id]
				fileIO("config/economy_settings.json", "save", LB)
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			if amount.lower() == "all":
				if user[6] <= 0:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, your pocket balance is 0.".format(author.id), color=0x363942)
					await ctx.send(embed=em)
					return
				bank_bal = user[6]
				bank_new_bal = user[3] + user[6]
				cursor = connection.cursor()
				cursor.execute(f"UPDATE users SET bank = '{bank_new_bal}' WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET pocket = 0 WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
				em = guilded.Embed(title="Bank:", description="<@{}>, you deposited x{} {} into your bank.".format(author.id, bank_bal, LB["currency_name"]), color=0x363942)
				await ctx.send(embed=em)
			else:
				if user[6] <= 0:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, your pocket balance is 0.".format(author.id), color=0x363942)
					await ctx.send(embed=em)
					return
				if int(amount) > user[6]:
					em = guilded.Embed(title="Uh oh!", description="<@{}>, you don't have x{} {} in your pocket into deposit.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
					await ctx.send(embed=em)
					return
				bank_bal = user[3] + int(amount)
				pocket_val = user[6] - int(amount)
				cursor = connection.cursor()
				cursor.execute(f"UPDATE users SET bank = '{bank_bal}' WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET pocket = {pocket_val} WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
				em = guilded.Embed(title="Bank:", description="<@{}>, you deposited x{} {} into your bank.".format(author.id, int(amount), LB["currency_name"]), color=0x363942)
				await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

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
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)

			async def getUserLB():
				with connection:
					cursor = connection.cursor()
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
				await ctx.send(embed=em)
				connection.close()
				return

			# We're now importing this function
			user = await getUser(author.id)
			LB_bans = fileIO("economy/bans.json", "load")
			if author.id in LB_bans["bans"]:
				em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
				await ctx.send(embed=em)
				connection.close()
				return
			
			em = guilded.Embed(title="Global leaderboard:".format(author.name), description=description, color=0x363942)
			# Add our footer with the page we're on out of the total
			em.set_footer(text=f"Page {page}/{numOfPages}")
			await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def rob(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			economy_settings = fileIO("config/economy_settings.json", "load")
			LB_bans = fileIO("economy/bans.json", "load")
			if author.id in LB_bans["bans"]:
				em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
				await ctx.send(embed=em)
				connection.close()
				return
			prefix = server[3]
			if member == None:
				em = guilded.Embed(title="Uh oh!", description="The member argument was left empty.\n\nEx: `{}rob <member>`".format(prefix), color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.send(embed=em)
				return
			if author == member:
				em = guilded.Embed(title="Uh oh!", description="You cannot rob yourself. Smhhhhhhh", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.send(embed=em)
				return
			user = await getUser(author.id)
			member1 = await getUser(member.id)
			if member1 == None:
				await _check_values_member(member)
			if user == None:
				await _check_values(author)
			curr_time = time.time()
			delta = float(curr_time) - float(user[8])
			if delta >= 900.0 and delta>0:
				if user[6] >= 250:
					if member1[6] < 250:
						em = guilded.Embed(title="Uh oh!", description="<@{}> doesn't have x250 or more {} in their pocket.".format(member.id, economy_settings["currency_name"]), color=0x363942)
						em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						await ctx.send(embed=em)
					else:
						num = random.randint(1, 10)
						num = num
						random_rob = random.randint(1, 250)
						random_rob = random_rob
						new_member_calc = member1[6] - random_rob
						new_user_calc = user[6] + random_rob
						new_user_calc_caught = user[6] - random_rob
						if num > 6:
							cursor = connection.cursor()
							cursor.execute(f"UPDATE users SET pocket = '{new_member_calc}' WHERE ID = '{member.id}'")
							cursor.execute(f"UPDATE users SET pocket = '{new_user_calc}' WHERE ID = '{author.id}'")
							cursor.execute(f"UPDATE users SET rob_timeout = '{curr_time}' WHERE ID = '{author.id}'")
							connection.commit()
							connection.close()
							em = guilded.Embed(title="Nice!", description="<@{}> successfully robbed <@{}> for x{} {}.".format(author.id, member.id, random_rob, economy_settings["currency_name"]), color=0x363942)
							await ctx.send(embed=em)
						else:
							cursor = connection.cursor()
							cursor.execute(f"UPDATE users SET rob_timeout = '{curr_time}' WHERE ID = '{author.id}'")
							cursor.execute(f"UPDATE users SET pocket = '{new_user_calc_caught}' WHERE ID = '{author.id}'")
							connection.commit()
							connection.close()
							em = guilded.Embed(title="Oh no :(", description="<@{}> got caught robbing <@{}> and got fined for x{} {}.".format(author.id, member.id, random_rob, economy_settings["currency_name"]), color=0x363942)
							await ctx.send(embed=em)
				else:
					em = guilded.Embed(title="Uh oh!", description="You need more than x250 {} in your pocket to rob someone.".format(economy_settings["currency_name"]), color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.send(embed=em)
			else:
				seconds = 900 - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot rob someone yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
				await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def weekly(self, ctx):
		author = ctx.author
		guild = ctx.guild
		support_guild = await self.bot.fetch_server("Mldgz04R")
		members_support_guild = await support_guild.fetch_members()
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			server = await getServer(guild.id)
			if user == None:
				await _check_values(author)
			gen_amount = random.randint(5000, 12000)
			multiplier_amount = float(server[5])
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
				if server[5] > 1:
					em.set_footer(text="The multiplier in this server boosted you by x{}".format(server[5]))
				await ctx.send(embed=em)
				gen_amount = user[6] + gen_amount
				cursor = connection.cursor()
				cursor.execute(f"UPDATE users SET pocket = '{gen_amount}' WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET weekly_timeout = '{curr_time}' WHERE ID = '{author.id}'")
				connection.commit()
				await check_leaderboard_author(author)
			else:
				seconds = curr_cooldown - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				d, h = divmod(h, 24)
				em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot get your weekly bonus yet.\n`Time left:` {}d {}m {}s".format(author.id, int(d), int(m), int(s)), color=0x363942)
				await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def slots(self, ctx, *, amount: int=None):
		author = ctx.author
		guild = ctx.guild
		support_guild = await self.bot.fetch_server("Mldgz04R")
		members_support_guild = await support_guild.fetch_members()
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_drops = fileIO("economy/drops.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			server = await getServer(guild.id)
			prefix = server[3]

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

			if amount == None:
				em = guilded.Embed(title="Welcome to slots", description="**__Goal__**\n`-` Get `x3💰` to win.\n`-` Get `x3💎` to win a JACKPOT.\n\n**__Payouts__**\nWin `-` x25 bonus.\nJACKPOT `-` x450 bonus\n\nUse `{}slots <amount>` to place a bet.".format(prefix), color=0x363942)
				await ctx.send(embed=em)
				return
			if amount < slots_bet_min or amount > slots_bet_max:
				em = guilded.Embed(title="Uh oh!", description="Your bet was out of range. Acceptable range is `{:,}-{:,}`".format(slots_bet_min, slots_bet_max), color=0x363942)
				await ctx.send(embed=em)
				return
			if amount > user[6]:
				em = guilded.Embed(title="Uh oh!", description="You don't have {:,} in your pocket.".format(amount), color=0x363942)
				await ctx.send(embed=em)
				return
			cursor = connection.cursor()
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
				if row_1_chance_jackpot == slots_jackpot_chanc:
					row_1_item_list.append('💎')
				row_1_a = random.choice(row_1_item_list)
				row_1.append(row_1_a)
				#ROW 2
				row_2_item_list = ['💚', '💜', '🖤']
				row_2_chance_win = random.randint(slots_win_min, slots_win_max)
				row_2_chance_jackpot = random.randint(slots_jackpot_min, slots_jackpot_max)
				if row_2_chance_win <= slots_win_chance:
					row_2_item_list.append('💰')
				if row_2_chance_jackpot == slots_jackpot_chanc:
					row_2_item_list.append('💎')
				row_2_a = random.choice(row_2_item_list)
				row_2.append(row_2_a)
				#ROW 3
				row_3_item_list = ['💚', '💜', '🖤']
				row_3_chance_win = random.randint(slots_win_min, slots_win_max)
				row_3_chance_jackpot = random.randint(slots_jackpot_min, slots_jackpot_max)
				if row_3_chance_win <= slots_win_chance:
					row_3_item_list.append('💰')
				if row_3_chance_jackpot == slots_jackpot_chanc:
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
				await ctx.send(embed=em)
				pocket_amount = user[6] + win_amount
				cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
			elif win_bool == False:
				display_output.append(f"**Slots:**\n{row_1[0]}{row_1[1]}{row_1[2]}\n{row_2[0]}{row_2[1]}{row_2[2]}\n{row_3[0]}{row_3[1]}{row_3[2]}")
				em = guilded.Embed(title="Lose", description="{}\n\n<@{}> lost a bet of {}".format(" \n".join(display_output), author.id, amount), color=0x363942)
				await ctx.send(embed=em)
				pocket_amount = user[6] - amount
				cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def work(self, ctx):
		author = ctx.author
		guild = ctx.guild
		support_guild = await self.bot.fetch_server("Mldgz04R")
		members_support_guild = await support_guild.fetch_members()
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_drops = fileIO("economy/drops.json", "load")
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

		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			server = await getServer(guild.id)
			if user == None:
				await _check_values(author)
			curr_time = time.time()
			if server[4] == "True":
				curr_cooldown = 20
			else:
				curr_cooldown = 60
			delta = float(curr_time) - float(user[9])
			if delta >= curr_cooldown and delta>0:
				cursor = connection.cursor()
				message_list = []
				booster_amount = 0
				if author in members_support_guild:
					author_support_guild = await support_guild.fetch_member(author.id)
					roles_list = await author_support_guild.fetch_role_ids()
					if 30058586 in roles_list:
						booster_amount += 3
					elif 30058578 in roles_list:
						booster_amount += 2
					elif 30058569 in roles_list:
						booster_amount += 1.5
				multiplier_amount = float(server[5]) + booster_amount
				gen_amount = random.randint(15, 150) * int(multiplier_amount)
				gen_amount = math.ceil(gen_amount)
				message_list.append("<@{}> gained {:,} {}!\n".format(author.id, gen_amount, economy_settings["currency_name"]))
				if economy_settings["halloween_event"] == "True":
					candycorn_gen_amount = random.randint(1, 10)
					common_chance_gen = roll_chance(common_min, common_max, common_chance)
					rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
					epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
					legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
					work_event_lines_list = []
					info = user[10]
					if common_chance_gen <= common_chance:
						info["inventory"]["seasonal_items"]["halloween"]["candycorn"]["amount"] += candycorn_gen_amount
						work_event_lines_list.append(f"[Common] +{candycorn_gen_amount} Candycorn")
					if rare_chance_gen <= rare_chance:
						rare_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[Rare] +{rare_amount} Jolly ranchers")
						info["inventory"]["seasonal_items"]["halloween"]["jolly_ranchers"]["amount"] += rare_amount
					if epic_chance_gen == epic_chance:
						epic_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[Epic] +{epic_amount} Nerds")
						info["inventory"]["seasonal_items"]["halloween"]["nerds"]["amount"] += epic_amount
					if legendary_chance_gen == legendary_chance:
						legendary_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[LEGENDARY] +{legendary_amount} Dots")
						info["inventory"]["seasonal_items"]["halloween"]["dots"]["amount"] += legendary_amount
					if not work_event_lines_list == []:
						message_list.append("__**Halloween event bonus:**__\n{}\n".format(" \n".join(work_event_lines_list)))
				common_chance = roll_chance(common_min, common_max, common_chance)
				rare_chance_gen = roll_chance(rare_min, rare_max, rare_chance)
				epic_chance_gen = roll_chance(epic_min, epic_max, epic_chance)
				legendary_chance_gen = roll_chance(legendary_min, legendary_max, legendary_chance)
				unreal_chance_gen = roll_chance(unreal_min, unreal_max, unreal_chance)
				drops_lines_list = []
				if common_chance_gen:
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
						drops_lines_list.append("[Common] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
					else:
						new_amount = info["inventory"]["items"][drop]["amount"] + amount
						info["inventory"]["items"][drop]["amount"] += amount
						drops_lines_list.append("[Common] +{} {}".format(amount,item_list["items"][drop]["display_name"]))
				if rare_chance_gen:
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
						drops_lines_list.append("[Rare] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
					else:
						new_amount = info["inventory"]["items"][drop]["amount"] + amount
						info["inventory"]["items"][drop]["amount"] += amount
						drops_lines_list.append("[Rare] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
				if epic_chance_gen:
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
						drops_lines_list.append("[Epic] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
					else:
						new_amount = info["inventory"]["items"][drop]["amount"] + amount
						info["inventory"]["items"][drop]["amount"] += amount
						drops_lines_list.append("[Epic] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
				if legendary_chance_gen:
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
						drops_lines_list.append("[LEGENDARY] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
					else:
						new_amount = info["inventory"]["items"][drop]["amount"] + amount
						info["inventory"]["items"][drop]["amount"] += amount
						drops_lines_list.append("[LEGENDARY] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
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
						drops_lines_list.append("[UNREAL] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
					else:
						new_amount = info["inventory"]["items"][drop]["amount"] + amount
						info["inventory"]["items"][drop]["amount"] += amount
						drops_lines_list.append("[UNREAL] +{} {}".format(amount, item_list["items"][drop]["display_name"]))
				if not drops_lines_list == []:
					message_list.append("__**Item drop:**__\n{}\n".format(" \n".join(drops_lines_list)))

				if author in members_support_guild:
					author_support_guild = await support_guild.fetch_member(author.id)
					roles_list = await author_support_guild.fetch_role_ids()
					if 30058586 in roles_list:
						edit_message = ":Gold_tier: Elite supporter boosted you by `x3`"
						message_list.append(edit_message)
					elif 30058578 in roles_list:
						edit_message = ":Silver_tier: Epic supporter boosted you by `x2`"
						message_list.append(edit_message)
					elif 30058569 in roles_list:
						edit_message = ":Copper_tier: Supporter boosted you by `x1.5`"
						message_list.append(edit_message)
				if server[4] == "True":
					edit_message = ":handshake: Server partner boosted you by `x{}`".format(float(server[5]))
					message_list.append(edit_message)
				em = guilded.Embed(title="{} has worked.".format(author.name), description="{}".format(" \n".join(message_list)), color=0x363942)
				em.set_footer(text="You were boosted by x{}".format(multiplier_amount))
				await ctx.send(embed=em)
				pocket_amount = user[6] + gen_amount
				infoJson = json.dumps(info)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
				cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
				cursor.execute(f"UPDATE users SET work_timeout = '{curr_time}' WHERE ID = '{author.id}'")
				connection.commit()
				await check_leaderboard_author(author)
				connection.close()
			else:
				seconds = curr_cooldown - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				em = guilded.Embed(title="Uh oh!", description="<@{}>, you cannot work yet.\n`Time left:` {}m {}s".format(author.id, int(m), int(s)), color=0x363942)
				await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)
		
	#Obv know what this is
	@commands.command(aliases=["me", "bal", "balance"])
	async def profile(self, ctx):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			if user == None:
				await _check_values(author)
			bank_code = user[4]
			em = guilded.Embed(title="{}'s bank information".format(author.name), description="__**Currency**__\n`Pocket:` x{:,} {}\n`Bank:` x{:,} {}\n`Bank secure:` {}\n`Bank access code:` {}{}{}{}{}xxxxxxxxxxxxxxxxxxxxxxxxxxx".format(user[6], economy_settings["currency_name"], user[3], economy_settings["currency_name"], user[5], bank_code[0], bank_code[1], bank_code[2], bank_code[3], bank_code[4]), color=0x363942)
			await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	@commands.command(aliases=["inventory"])
	async def inv(self, ctx, *, num: str=None):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		economy_settings = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			user = await getUser(author.id)
			server = await getServer(guild.id)
			prefix = server[3]
			if user == None:
				await _check_values(author)
			info = user[10]
			bank_code = user[4]
			halloween_print_list = []
			default_print_list = []
			for key, i in info["inventory"]["seasonal_items"]["halloween"].items():
				if i["amount"] > 0:
					halloween_print_list.append("{} -\n`1.` • Amount: {}\n`2.` • Description: {}\n".format(item_list["items"][key]["display_name"], i["amount"], item_list["items"][key]["description"]))
			if halloween_print_list == []:
				halloween_print_list.append("None")
			for key, i in info["inventory"]["items"].items():
				if i["amount"] > 0:
					default_print_list.append("{} -\n`1.` • Amount: {}\n`2.` • Description: {}\n".format(item_list["items"][key]["display_name"], i["amount"], item_list["items"][key]["description"]))
			if default_print_list == []:
				default_print_list.append("None")
			if num == None:
				em = guilded.Embed(title="Inventory - Help menu".format(author.name), description="__**Inventory pages:**__\n`1` • Default\n`2` • Halloween\n\nUse `{}inv <page>`".format(prefix), color=0x363942)
				await ctx.send(embed=em)
			elif num == "1" or num.lower() == "default":
				em = guilded.Embed(title="Inventory - Page 1".format(author.name), description="__**Inventory:**__\n{}".format(" \n".join(default_print_list)), color=0x363942)
				await ctx.send(embed=em)
			elif num == "2" or num.lower() == "halloween":
				em = guilded.Embed(title="Inventory - Page 2".format(author.name), description="__**Halloween inventory:**__\n{}".format(" \n".join(halloween_print_list)), color=0x363942)
				await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	#Get guild stats, is partner, and booster multiplier
	@commands.command()
	async def stats(self, ctx):
		author = ctx.author
		guild = ctx.guild
		if author.bot:
			return
		await _check_values_guild(guild)
		server = await getServer(guild.id)
		em = guilded.Embed(title="Guild stats:", description="**Partner:** {}\n**Multiplier:** x{}".format(server[4], server[5]), color=0x363942)
		await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Economy(bot))