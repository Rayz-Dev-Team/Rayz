import guilded
from guilded.ext import commands
import json
import uuid
from tools.dataIO import fileIO
import re
from core.database import *
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row

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
		server = await getServer(guild.id)
		if server["log_actions"] == None:
			return
		if banned == True:
			channel = await guild.fetch_channel(server["log_actions"])
			em = guilded.Embed(title="A member was banned:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)
		elif kicked  == True:
			channel = await guild.fetch_channel(server["log_actions"])
			em = guilded.Embed(title="A member was kicked:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)
		else:
			channel = await guild.fetch_channel(server["log_traffic"])
			em = guilded.Embed(title="A member has left:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)

	@commands.Cog.listener()
	async def on_bot_add(self, event: guilded.BotAddEvent):
		guild = event.server
		user = event.member
		author = user
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		send_channel = await guild.fetch_default_channel()
		support_guild = await self.bot.fetch_server("Mldgz04R")
		channel = await support_guild.fetch_channel("fd818fb2-c102-4ce9-b347-23d00a5649f8")
		await _check_values_guild(guild)
		em = guilded.Embed(title="Hello community!", description="`-` Thanks <@{}> for inviting me to **{}!**\n`-` My default prefix/help command is `?help`\n`-` Rayz is a multipurpose bot featuring moderation, logging, a global economy, interaction commands, and more!\n\n**Links**\n[Support server](https://www.guilded.gg/i/E6g8PZG2) • [Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)".format(user.id, guild.name), color=0x363942)
		await send_channel.send(embed=em)
		em = guilded.Embed(title="Rayz joined a Guild!", description="**__{}__**\n**Inivted by:** `{} ({})`".format(guild.name, user.name, user.id), color=0x363942)
		await channel.send(embed=em)

	@commands.Cog.listener()
	async def on_member_join(self, event: guilded.MemberJoinEvent):
		author = event.member
		guild = event.server
		if author.bot:
			return
		await _check_values_guild(guild)
		server = await getServer(guild.id)
		if server["welcome_channel"] == None:
			pass
		else:
			try:
				channel = await guild.fetch_channel(server["welcome_channel"])
				if server["welcome_message"] == None:
					welcome_message = f"Welcome <@{author.id}> to {guild.name}!"
				else:
					welcome_message = server["welcome_message"]
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
			if server["log_traffic"] == None:
				pass
			else:
				channel = await guild.fetch_channel(server["log_traffic"])
				em = guilded.Embed(title="A member has joined:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
				await channel.send(embed=em)

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

		server = await getServer(guild.id)
		prefix = server["server_prefix"]
		if server["custom_blocked_words"] == None:
			append_it = ["111111111111111111111111111111111111111111111111111111111111111111111111111111111"]
		else:
			append_it = server["custom_blocked_words"]
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
				if server["logs_channel_id"] == "None":
					em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
					em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160s", text="Make sure to set a log channel to get the full details next time.")
					await message.reply(embed=em, private=True)
					await message.delete()
				else:
					try:
						channel = await guild.fetch_channel(server["logs_channel_id"])
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

	@commands.Cog.listener()
	async def on_message_update(self, event: guilded.MessageUpdateEvent):
		guild = event.server
		author = event.before.author
		before = event.before
		after = event.after
		if before.created_by_bot:
			return

		server = await getServer(guild.id)
		if server["logs_channel_id"] is not None:
			try:
				channel = await guild.fetch_channel(server[2])
				em = guilded.Embed(title="Message edit event.", description="**User:** {}\n**ID:** {}\n\n__**EDIT EVENT**__\n`Before:`\n{}\n\n`After:`\n{}".format(author.name, author.id, before.content, after.content), color=0x363942)
				await channel.send(embed=em)
			except:
				pass
		else:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, event: guilded.MessageDeleteEvent):
		guild = event.server
		author = event.message.author
		channel = event.channel
		message = event.message
		if message.created_by_bot:
			return

		server = await getServer(guild.id)
		if server["logs_channel_id"] is not None:
			try:
				channel = await guild.fetch_channel(server["logs_channel_id"])
				em = guilded.Embed(title="Message delete event.", description="**User:** {}\n**ID:** {}\n\n__**DELETE EVENT**__\n**Deleted message:** {}".format(author.name, author.id, message.content), color=0x363942)
				await channel.send(embed=em)
			except:
				pass
		else:
			pass


async def _check_inventory(author):
	try:
		item_list = fileIO("economy/items.json", "load")
		user = await getUser(author.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			cursor = conn.cursor()
			if user["inventory"] == None or user["inventory"] == {}:
				new_account = {
					"inventory": {
						"items": {},
						"consumables": {}
					}
				}
				infoJson = json.dumps(new_account)
				cursor = conn.cursor()
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
				connection.close()
			else:
				info = user["inventory"]
				for i in item_list["items"]:
					if not i in info["inventory"]["items"]:
						info["inventory"]["items"][i] = {
							"amount": 0
						}
				infoJson = json.dumps(info)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
				connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_inventory_member(member):
	try:
		item_list = fileIO("economy/items.json", "load")
		user = await getUser(member.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			cursor = conn.cursor()
			if user["inventory"] == None:
				new_account = {
					"inventory": {
						"items": {},
						"consumables": {}
					}
				}
				infoJson = json.dumps(new_account)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
				conn.commit()
				connection.close()
			else:
				info = user["inventory"]
				for i in item_list["items"]:
					if not i in info["inventory"]["items"]:
						info["inventory"]["items"][i] = {
							"amount": 0
						}
				infoJson = json.dumps(info)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
				conn.commit()
				connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_member(member):
	try:
		user = await getUser(member.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			if user == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO users(id, daily_timeout, daily_tokens, bank, bank_access_code, bank_secure, pocket, weekly_timeout, rob_timeout, work_timeout, commands_used, dig_timeout) VALUES('{member.id}', '0', 0, 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0, 0, 0, 0, 0)")
				conn.commit()
			await _check_inventory_member(member)
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def check_leaderboard(author):
	try:
		user = await getUser(author.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			if user == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO leaderboard(id, name, currency) VALUES('{author.id}', 'None', 0)")
				conn.commit()
			await _check_inventory(author)
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def command_processed(message, author):
	try:
		user = await getUser(author.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			cursor = conn.cursor()
			total_amount = user["commands_used"] + 1
			cursor.execute(f"UPDATE users SET commands_used = {total_amount} WHERE ID = '{author.id}'")
			conn.commit()
			if total_amount == 5:
				em = guilded.Embed(title="Hello {}!".format(author.name), description="I see that you like using me! Here are some links that may be useful to you!\n\n**Links**\n[Support server](https://www.guilded.gg/i/E6g8PZG2) • [Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)", color=0x363942)
				em.set_footer(text="This message will only appear once for you.")
				await message.reply(embed=em, private=True)
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')


async def check_leaderboard_author(author):
	try:
		user = await getUser(author.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			cursor = conn.cursor()
			new_LB_bal = user["bank"] + user["pocket"]
			cursor.execute(f"UPDATE leaderboard SET currency = {new_LB_bal} WHERE ID = '{author.id}'")
			cursor.execute(f"UPDATE leaderboard SET name = '{author.name}' WHERE ID = '{author.id}'")
			conn.commit()
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values(author):
	try:
		user = await getUser(author.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			if user == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO users(id, daily_timeout, daily_tokens, bank, bank_access_code, bank_secure, pocket, weekly_timeout, rob_timeout, work_timeout, commands_used, dig_timeout) VALUES('{author.id}', '0', 0, 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0, 0, 0, 0, 0)")
				conn.commit()
			await _check_inventory(author)
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_guild(guild):
	try:
		server = await getServer(guild.id)
		connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
		with connection.connection() as conn:
			if server == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO servers(id, logs_channel_id, server_prefix, partner_status, economy_multiplier, moderation_module, fun_module, economy_module) VALUES('{guild.id}', 'None', '?', 'False', 1, 'Enabled', 'Enabled', 'Enabled')")
				conn.commit()
			connection.close()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')


def setup(bot):
	bot.add_cog(Generator(bot))