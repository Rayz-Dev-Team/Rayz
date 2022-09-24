import guilded
from guilded.ext import commands
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
		if 30058569 in roles_list:
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{member.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
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
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		prices = fileIO("economy/prices.json", "load")
		item_list = fileIO("economy/items.json", "load")
		say_list = []
		for key, i in prices["items"].items():
			say_list.append("{} - {:,}".format(item_list["items"][i]["display_name"], i["price"]))
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
		LB = fileIO("config/economy_settings.json", "load")
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
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
					em = guilded.Embed(title="Transfer complete", description="`-` {:,} {} removed from <@{}>'s inventory.\n`-` <@{}> was given {:,} {}.".format(amount, item.lower(), author.id, author.id, total_amount, LB["currency_name"]), color=0x363942)
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getMember():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{member.id}'")
					content = cursor.fetchone()
				return content
			member1 = await getMember()
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getMember():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{member.id}'")
					content = cursor.fetchone()
				return content
			member1 = await getMember()
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
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

	@commands.command(aliases=["lb"])
	async def leaderboard(self, ctx):
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
					cursor.execute(f"SELECT * FROM leaderboard")
					result = cursor.fetchall()
				return result
			LB = await getUserLB()
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			LB_bans = fileIO("economy/bans.json", "load")
			if author.id in LB_bans["bans"]:
				em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
				await ctx.send(embed=em)
				connection.close()
				return
			LB_list = {}
			for i in LB:
				LB_list[i[1]] = "{}".format(i[2])
			sort_orders = sorted(LB_list.items(), key=lambda x: int(x[1]), reverse=True)
			sort_list = []
			for i in sort_orders:
				sort_list.append("{}: {:,}".format(i[0], int(i[1])))
			em = guilded.Embed(title="Global leaderboard:".format(author.name), description="`1.` {}\n`2.` {}\n`3.` {}\n`4.` {}\n`5.` {}\n`6.` {}\n`7.` {}\n`8.` {}\n`9.` {}\n`10.` {}".format(sort_list[0], sort_list[1], sort_list[2], sort_list[3], sort_list[4], sort_list[5], sort_list[6], sort_list[7], sort_list[8], sort_list[9]), color=0x363942)
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
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			LB = fileIO("config/economy_settings.json", "load")
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
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getMember():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{member.id}'")
					content = cursor.fetchone()
				return content
			member1 = await getMember()
			if member1 == None:
				await _check_values_member(member)
			if user == None:
				await _check_values(author)
			curr_time = time.time()
			delta = float(curr_time) - float(user[8])
			if delta >= 900.0 and delta>0:
				if user[6] >= 250:
					if member1[6] < 250:
						em = guilded.Embed(title="Uh oh!", description="<@{}> doesn't have x250 or more {} in their pocket.".format(member.id, LB["currency_name"]), color=0x363942)
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
							em = guilded.Embed(title="Nice!", description="<@{}> successfully robbed <@{}> for x{} {}.".format(author.id, member.id, random_rob, LB["currency_name"]), color=0x363942)
							await ctx.send(embed=em)
						else:
							cursor = connection.cursor()
							cursor.execute(f"UPDATE users SET rob_timeout = '{curr_time}' WHERE ID = '{author.id}'")
							cursor.execute(f"UPDATE users SET pocket = '{new_user_calc_caught}' WHERE ID = '{author.id}'")
							connection.commit()
							connection.close()
							em = guilded.Embed(title="Oh no :(", description="<@{}> got caught robbing <@{}> and got fined for x{} {}.".format(author.id, member.id, random_rob, LB["currency_name"]), color=0x363942)
							await ctx.send(embed=em)
				else:
					em = guilded.Embed(title="Uh oh!", description="You need more than x250 {} in your pocket to rob someone.".format(LB["currency_name"]), color=0x363942)
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if user == None:
				await _check_values(author)
			gen_amount = random.randint(5000, 12000)
			multiplier_amount = float(server[5])
			edit_message = None
			if author in members_support_guild:
				author_support_guild = await support_guild.fetch_member(author.id)
				roles_list = await author_support_guild.fetch_role_ids()
				if 30058586 in roles_list:
					edit_message = ":Gold_tier: Elite supporter boosted you by `x3`"
					multiplier_amount += 3
				elif 30058578 in roles_list:
					edit_message = ":Silver_tier: Epic supporter boosted you by `x2`"
					multiplier_amount += 2
				elif 30058569 in roles_list:
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
					if 30058586 in roles_list or 30058578 in roles_list or 30058569 in roles_list:
						em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!\n\n{}".format(author.id, gen_amount, LB["currency_name"], edit_message), color=0x363942)
					else:
						em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!".format(author.id, gen_amount, LB["currency_name"]), color=0x363942)
				else:
					em = guilded.Embed(title="{} has obtained their weekly bonus.".format(author.name), description="<@{}> gained x{:,} {}!".format(author.id, gen_amount, LB["currency_name"]), color=0x363942)
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_drops = fileIO("economy/drops.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			prefix = server[3]
			if amount == None:
				em = guilded.Embed(title="Welcome to slots", description="**__Goal__**\n`-` Get `x3💰` to win.\n`-` Get `x3💎` to win a JACKPOT.\n\n**__Payouts__**\nWin `-` x30 bonus.\nJACKPOT `-` x140 bonus\n\nUse `{}slots <amount>` to place a bet.".format(prefix), color=0x363942)
				await ctx.send(embed=em)
				return
			if amount < 2500 or amount > 15000:
				em = guilded.Embed(title="Uh oh!", description="Your bet was out of range. Acceptable range is `2,500-15,000`", color=0x363942)
				await ctx.send(embed=em)
				return
			if amount > user[6]:
				em = guilded.Embed(title="Uh oh!", description="You don't have {:,} in your pocket.".format(amount), color=0x363942)
				await ctx.send(embed=em)
				return
			cursor = connection.cursor()
			final = []
			display_output = []
			for i in range(3):
				item_list = ['🧡', '💛', '💚', '💙', '💜', '🖤']
				chance_win = random.randint(1, 100)
				chance_jackpot = random.randint(1, 1000)
				if chance_win <= 75:
					item_list.append('💰')
				if chance_jackpot == 1:
					item_list.append('💎')
				a = random.choice(item_list)
				final.append(a)
			if final.count('💰') == 3:
				display_output.append(f"**Slots:**:\n{final[0]}{final[1]}{final[2]}")
				em = guilded.Embed(title="WIN!", description="{}\n\nYour bet of x has been multiplied by x".format(" \n".join(display_output)), color=0x363942)
				await ctx.send(embed=em)
				win_amount = amount * 30
				pocket_amount = user[6] + win_amount
				cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
			elif final.count('💎') ==3:
				display_output.append(f"**Slots:**:\n{final[0]}{final[1]}{final[2]}")
				em = guilded.Embed(title="JACKPOT!", description="{}\n\nYour bet of x has been multiplied by x".format(" \n".join(display_output)), color=0x363942)
				await ctx.send(embed=em)
				win_amount = amount * 140
				pocket_amount = user[6] + win_amount
				cursor.execute(f"UPDATE users SET pocket = '{pocket_amount}' WHERE ID = '{author.id}'")
				connection.commit()
				connection.close()
			else:
				display_output.append(f"**Slots:**\n{final[0]}{final[1]}{final[2]}")
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_drops = fileIO("economy/drops.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
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
				message_list.append("<@{}> gained {:,} coins!\n".format(author.id, gen_amount))
				if LB["halloween_event"] == "True":
					candycorn_gen_amount = random.randint(1, 10)
					common_chance = random.randint(1, 100)
					rare_chance = random.randint(1, 100)
					epic_chance = random.randint(1, 100)
					legendary_chance = random.randint(1, 1000)
					work_event_lines_list = []
					info = user[10]
					if common_chance <= 50:
						info["inventory"]["seasonal_items"]["halloween"]["candycorn"]["amount"] += candycorn_gen_amount
						work_event_lines_list.append(f"[Common] +{candycorn_gen_amount} Candycorn")
					if rare_chance <= 15:
						rare_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[Rare] +{rare_amount} Jolly ranchers")
						info["inventory"]["seasonal_items"]["halloween"]["jolly_ranchers"]["amount"] += rare_amount
					if epic_chance == 1:
						epic_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[Epic] +{epic_amount} Nerds")
						info["inventory"]["seasonal_items"]["halloween"]["nerds"]["amount"] += epic_amount
					if legendary_chance == 1:
						legendary_amount = random.randint(1, 10)
						work_event_lines_list.append(f"[LEGENDARY] +{legendary_amount} Dots")
						info["inventory"]["seasonal_items"]["halloween"]["dots"]["amount"] += legendary_amount
					if not work_event_lines_list == []:
						message_list.append("__**Halloween event bonus:**__\n{}\n".format(" \n".join(work_event_lines_list)))
				common_chance = random.randint(1, 100)
				rare_chance = random.randint(1, 100)
				epic_chance = random.randint(1, 100)
				legendary_chance = random.randint(1, 1000)
				unreal_chance = random.randint(1, 10000)
				drops_lines_list = []
				if common_chance <= 50:
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
				if rare_chance <= 15:
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
				if epic_chance == 1:
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
				if legendary_chance == 1:
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
				if unreal_chance == 1:
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			if user == None:
				await _check_values(author)
			bank_code = user[4]
			em = guilded.Embed(title="{}'s bank information".format(author.name), description="__**Currency**__\n`Pocket:` x{:,} {}\n`Bank:` x{:,} {}\n`Bank secure:` {}\n`Bank access code:` {}{}{}{}{}xxxxxxxxxxxxxxxxxxxxxxxxxxx".format(user[6], LB["currency_name"], user[3], LB["currency_name"], user[5], bank_code[0], bank_code[1], bank_code[2], bank_code[3], bank_code[4]), color=0x363942)
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
		LB = fileIO("config/economy_settings.json", "load")
		LB_bans = fileIO("economy/bans.json", "load")
		item_list = fileIO("economy/items.json", "load")
		if author.id in LB_bans["bans"]:
			em = guilded.Embed(title="Uh oh!", description="You were banned from Rayz's Economy for violating our ToS.", color=0x363942)
			await ctx.send(embed=em)
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getUser():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM users WHERE ID = '{author.id}'")
					content = cursor.fetchone()
				return content
			user = await getUser()
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
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
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			em = guilded.Embed(title="Guild stats:", description="**Partner:** {}\n**Multiplier:** x{}".format(server[4], server[5]), color=0x363942)
			await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Economy(bot))