import guilded
from guilded.ext import commands
import asyncio
import json
import aiohttp
import random 
import uuid
import os
import glob
import datetime
from tools.dataIO import fileIO
import re
import psycopg2
from psycopg2 import Error
from core.database import *
from psycopg2.extras import Json
from tools.db_funcs import getUser
from tools.db_funcs import getServer

class Generator(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_remove(self, event: guilded.MemberRemoveEvent):
		author = event.member
		guild = event.server
		kicked = event.kicked
		banned = event.banned
		if author.bot:
			return
		await _check_values_guild(guild)
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			if server[15] == None:
				return
			if banned == True:
				channel = await guild.fetch_channel(server[15])
				em = guilded.Embed(title="A member was banned:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
				await channel.send(embed=em)
			elif kicked  == True:
				channel = await guild.fetch_channel(server[15])
				em = guilded.Embed(title="A member was kicked:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
				await channel.send(embed=em)
			else:
				channel = await guild.fetch_channel(server[14])
				em = guilded.Embed(title="A member has left:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
				await channel.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')

	@commands.Cog.listener()
	async def on_member_join(self, event: guilded.MemberJoinEvent):
		author = event.member
		guild = event.server
		if author.bot:
			return
		await _check_values_guild(guild)
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			if server[13] == None:
				pass
			else:
				try:
					channel = await guild.fetch_channel(server[13])
					if server[12] == None:
						welcome_message = f"Welcome <@{author.id}> to {guild.name}!"
					else:
						welcome_message = server[12]
					try:
						welcome_message = welcome_message.replace("<user>", f"<@{author.id}>")
					except:
						pass
					try:
						welcome_message = welcome_message.replace("<server>", f"{guild.name}")
					except: 
						pass
					em = guilded.Embed(title="A member has joined!", description="{}".format(welcome_message), color=0x363942)
					try:
						em.set_thumbnail(url=guild.icon)
					except:
						pass
					await channel.send(embed=em)
				except:
					pass
				if server[14] == None:
					pass
				else:
					channel = await guild.fetch_channel(server[14])
					em = guilded.Embed(title="A member has joined:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
					await channel.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')

	@commands.Cog.listener()
	async def on_message(self, event: guilded.MessageEvent):
		author = event.message.author
		guild = event.server
		message = event.message
		if event.message.created_by_bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		info = fileIO("config/banned_words.json", "load")
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			prefix = server[3]
			if server[1] == None:
				append_it = ["111111111111111111111111111111111111111111111111111111111111111111111111111111111"]
			else:
				append_it = server[1]
			swearwords = info["banned_words"] + append_it
			message_safe = True
			things_said = []
			captures = []
			if message.content.lower() == "@rayz" or message.content.lower() == "@rayz ":
				em = guilded.Embed(description="My prefix in this guild is `{}`".format(prefix), color=0x363942)
				await message.reply(embed=em)
			for word in swearwords:
				if re.search(word, message.content.lower()):
					things_said.append("{}{}-".format(word[0], word[1]))
					captures.append(word)
					message_safe = False
			if not message_safe:
				moderator_or_not = False	
				for i in author.roles:
					if i.permissions.manage_messages == True or i.permissions.kick_members == True:
						moderator_or_not = True
						await message.add_reaction(90002078)
				if moderator_or_not == False:
					if server[2] == "None":
						em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
						em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160s", text="Make sure to set a log channel to get the full details next time.")
						await message.reply(embed=em, private=True)
						await message.delete()
					else:
						try:
							channel = await guild.fetch_channel(server[2])
							em = guilded.Embed(title="A blacklisted word was used.", description="**User** {}\n**ID:** {}\n\n__**READ AT YOUR OWN RISK**__\n`Captures:`\n{}\n\n`Message content:`\n{}".format(author.name, author.id, " \n".join(captures), message.content), color=0x363942)
							await channel.send(embed=em)
							em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
							em.set_footer(text="Details sent to the logs channel.")
							await message.reply(embed=em, private=True)
							await message.delete()
						except:
							em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
							em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="The channel ID set doesn't exist. You may have to set a different ID.")
							await message.reply(embed=em, private=True)
							await message.delete()
			connection.close()
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')

	@commands.Cog.listener()
	async def on_message_update(self, event: guilded.MessageUpdateEvent):
		guild = event.server
		author = event.before.author
		before = event.before
		after = event.after
		if before.created_by_bot:
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			if server[2] is not None:
				try:
					channel = await guild.fetch_channel(server[2])
					em = guilded.Embed(title="Message edit event.", description="**User:** {}\n**ID:** {}\n\n__**EDIT EVENT**__\n`Before:`\n{}\n\n`After:`\n{}".format(author.name, author.id, before.content, after.content), color=0x363942)
					await channel.send(embed=em)
				except:
					pass
			else:
				pass
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')

	@commands.Cog.listener()
	async def on_message_delete(self, event: guilded.MessageDeleteEvent):
		guild = event.server
		author = event.message.author
		channel = event.channel
		message = event.message
		if message.created_by_bot:
			return
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			server = await getServer(guild.id)
			if server[2] is not None:
				try:
					channel = await guild.fetch_channel(server[2])
					em = guilded.Embed(title="Message delete event.", description="**User:** {}\n**ID:** {}\n\n__**DELETE EVENT**__\n**Deleted message:** {}".format(author.name, author.id, message.content), color=0x363942)
					await channel.send(embed=em)
				except:
					pass
			else:
				pass
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')


async def _check_inventory(author):
	try:
		item_list = fileIO("economy/items.json", "load")
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(author.id)
		if user[10] == None:
			new_account = {
				"inventory": {
					"items": {},
					"consumables": {}
				}
			}
			infoJson = json.dumps(new_account)
			cursor = connection.cursor()
			cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
			connection.commit()
			connection.close()
			return
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(author.id)
		info = user[10]
		for i in item_list["items"]:
			if not i in info["inventory"]["items"]:
				info["inventory"]["items"][i] = {
					"amount": 0
				}
		infoJson = json.dumps(info)
		cursor = connection.cursor()
		cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
		connection.commit()
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def _check_inventory_member(member):
	try:
		item_list = fileIO("economy/items.json", "load")
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(member.id)
		if user[10] == None:
			new_account = {
				"inventory": {
					"items": {},
					"consumables": {}
				}
			}
			infoJson = json.dumps(new_account)
			cursor = connection.cursor()
			cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
			connection.commit()
			connection.close()
			return
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(member.id)
		info = user[10]
		for i in item_list["items"]:
			if not i in info["inventory"]["items"]:
				info["inventory"]["items"][i] = {
					"amount": 0
				}
		infoJson = json.dumps(info)
		cursor = connection.cursor()
		cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
		connection.commit()
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_member(member):
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(member.id)
		if user == None:
			cursor = connection.cursor()
			cursor.execute(f"INSERT INTO users(id, daily_timeout, daily_tokens, bank, bank_access_code, bank_secure, pocket, weekly_timeout, rob_timeout, work_timeout) VALUES('{member.id}', '0', 0, 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0, 0, 0)")
			connection.commit()
		await _check_inventory_member(member)
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def check_leaderboard(author):
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		async def getUser():
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT * FROM leaderboard WHERE ID = '{author.id}'")
				content = cursor.fetchone()
			return content
		user = await getUser()
		if user == None:
			cursor = connection.cursor()
			cursor.execute(f"INSERT INTO leaderboard(id, name, currency) VALUES('{author.id}', 'None', 0)")
			connection.commit()
		await _check_inventory(author)
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def check_leaderboard_author(author):
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		cursor = connection.cursor()
		user = await getUser(author.id)
		new_LB_bal = user[3] + user[6]
		cursor.execute(f"UPDATE leaderboard SET currency = {new_LB_bal} WHERE ID = '{author.id}'")
		cursor.execute(f"UPDATE leaderboard SET name = '{author.name}' WHERE ID = '{author.id}'")
		connection.commit()
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def _check_values(author):
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		user = await getUser(author.id)
		if user == None:
			cursor = connection.cursor()
			cursor.execute(f"INSERT INTO users(id, daily_timeout, daily_tokens, bank, bank_access_code, bank_secure, pocket, weekly_timeout, rob_timeout, work_timeout) VALUES('{author.id}', '0', 0, 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0, 0, 0)")
			connection.commit()
		await _check_inventory(author)
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_guild(guild):
	try:
		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
		server = await getServer(guild.id)
		if server == None:
			cursor = connection.cursor()
			cursor.execute(f"INSERT INTO servers(id, logs_channel_id, server_prefix, partner_status, economy_multiplier, moderation_module, fun_module, economy_module) VALUES('{guild.id}', 'None', '?', 'False', 1, 'Enabled', 'Enabled', 'Enabled')")
			connection.commit()
		connection.close()
	except psycopg2.DatabaseError as e:
		print(f'Error {e}')


def setup(bot):
	bot.add_cog(Generator(bot))