import guilded
from guilded.ext import commands
from tools.dataIO import fileIO
from core import checks
from core.database import *
from modules.generator import command_processed
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row

class Moderation(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def setwelcomemessage(self, ctx, *, arg: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		if author == guild.owner:
			if arg == None:
				em = guilded.Embed(title="Uh oh!", description="Message cannot be blank!\n\n**Replaced methods:**\n`<server>` is replaced with the server name.\n`<user>` is replaced with the user.\n\n**Example:**\n`setwelcomemessage <user>, welcome to <server>!`", color=0x363942)
				await ctx.reply(embed=em)
				return
			try:
				with db_connection.connection() as conn:
					server = await getServer(guild.id)
					cursor = conn.cursor()
					cursor.execute(f"UPDATE servers SET welcome_message = '{arg}' WHERE ID = '{guild.id}'")
					conn.commit()
					em = guilded.Embed(title="New welcome message set", description="{}".format(arg), color=0x363942)
					await ctx.reply(embed=em)
			except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have perms to set up a welcome channel.", color=0x363942)
			em.set_image(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def settrafficlogs(self, ctx, *, arg: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		if author == guild.owner:
			try:
				with db_connection.connection() as conn:
					cursor = conn.cursor()
					server = await getServer(guild.id)
					if not arg == None:
						if arg.lower() == "none" or arg.lower() == "reset":
							cursor.execute(f"UPDATE servers SET log_traffic = 'None' WHERE ID = '{guild.id}'")
							conn.commit()
							em = guilded.Embed(title="Traffic channel reset", description="None", color=0x363942)
							await ctx.reply(embed=em)
					else:
						cursor.execute(f"UPDATE servers SET log_traffic = '{ctx.channel.id}' WHERE ID = '{guild.id}'")
						conn.commit()
						em = guilded.Embed(title="Traffic channel set", description="{}".format(ctx.channel.id), color=0x363942)
						await ctx.reply(embed=em)
			except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have perms to set up a welcome channel.", color=0x363942)
			em.set_image(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def setactionlogs(self, ctx, *, arg: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		if author == guild.owner:
			try:
				with db_connection.connection() as conn:
					cursor = conn.cursor()
					server = await getServer(guild.id)
					if not arg == None:
						if arg.lower() == "none" or arg.lower() == "reset":
							cursor.execute(f"UPDATE servers SET log_actions = 'None' WHERE ID = '{guild.id}'")
							conn.commit()
							em = guilded.Embed(title="Action channel reset", description="None", color=0x363942)
							await ctx.reply(embed=em)
					else:
						cursor.execute(f"UPDATE servers SET log_actions = '{ctx.channel.id}' WHERE ID = '{guild.id}'")
						conn.commit()
						em = guilded.Embed(title="Action channel set", description="{}".format(ctx.channel.id), color=0x363942)
						await ctx.reply(embed=em)
			except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have perms to set up a welcome channel.", color=0x363942)
			em.set_image(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def setwelcomechannel(self, ctx, *, arg: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		if author == guild.owner:
			try:
				with db_connection.connection() as conn:
					cursor = conn.cursor()
					server = await getServer(guild.id)
					if not arg == None:
						if arg.lower() == "none" or arg.lower() == "reset":
							cursor.execute(f"UPDATE servers SET welcome_channel = 'None' WHERE ID = '{guild.id}'")
							conn.commit()
							em = guilded.Embed(title="Welcome channel reset", description="None", color=0x363942)
							await ctx.reply(embed=em)
					else:
						cursor.execute(f"UPDATE servers SET welcome_channel = '{ctx.channel.id}' WHERE ID = '{guild.id}'")
						conn.commit()
						em = guilded.Embed(title="Welcome channel set", description="{}".format(ctx.channel.id), color=0x363942)
						await ctx.reply(embed=em)
			except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have perms to set up a welcome channel.", color=0x363942)
			em.set_image(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def addowner(self, ctx, *, member: guilded.Member=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="You didn't specify a user to be an owner!", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
		try:
			with db_connection.connection() as conn:
				cursor = conn.cursor()
				server = await getServer(guild.id)
				list_people = []
				list_people_display = []
				if server[9] == None:
					list_people.append(member.id)
					stmt = f"UPDATE servers SET server_owners=%s WHERE ID = '{guild.id}'"
					cursor.execute(stmt, (list_people,))
					conn.commit()
					em = guilded.Embed(title="New owner added:", description="<@{}>".format(member.id), color=0x363942)
					await ctx.reply(embed=em)
				else:
					if not server[9] == None:
						for i in server[9]:
							list_people.append(i)
							list_people_display.append("<@{}>".format(i))
					if member.id in list_people:
						em = guilded.Embed(title="Uh oh!", description="<@{}> is already an owner.".format(member.id), color=0x363942)
						await ctx.reply(embed=em)
					else:
						list_people.append(member.id)
						stmt = f"UPDATE servers SET server_owners=%s WHERE ID = '{guild.id}'"
						cursor.execute(stmt, (list_people,))
						conn.commit()
						em = guilded.Embed(title="New owner added:", description="<@{}>\n\n__**Current owners:**__\n{}\n<@{}>".format(member.id, " \n".join(list_people_display), member.id), color=0x363942)
						await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')


	@commands.command()
	async def unbanword(self, ctx, *, word: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		try:
			with db_connection.connection() as conn:
				cursor = conn.cursor()
				server = await getServer(guild.id)
				prefix = server["server_prefix"]
				channel = ctx.message.channel
				if server["moderation_module"] == "Disabled":
					em = guilded.Embed(description="The moderation module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if word == None:
					em = guilded.Embed(title="Uh oh!", description="You didn't specify a word to be an unbanned!\n\n`Ex:` {}unbanword <word>".format(prefix), color=0x363942)
					await ctx.reply(embed=em)
					return
				moderator_or_not = False
				for i in author.roles:
					if i.permissions.manage_messages == True or i.permissions.kick_members == True:
						moderator_or_not = True
				if author == guild.owner:
					moderator_or_not = True
				if moderator_or_not == True:
					if server["custom_blocked_words"] == None:
						em = guilded.Embed(title="Wew!", description="The word isn't banned.", color=0x363942)
						await ctx.reply(embed=em)
						connection.close()
						return
					else:
						list_server = []
						for i in server["custom_blocked_words"]:
							list_server.append(i)
						if str(word).lower() in list_server:
							list_server.remove(str(word).lower())
							stmt = f"UPDATE servers SET custom_blocked_words=%s WHERE ID = '{guild.id}'"
							cursor.execute(stmt, (list_server,))
							conn.commit()
							em = guilded.Embed(title="Nice!", description="The word has been unbanned.", color=0x363942)
							await ctx.reply(embed=em)
						else:
							em = guilded.Embed(title="Wew!", description="The word isn't banned.", color=0x363942)
							await ctx.reply(embed=em)
				else:
					em = guilded.Embed(title="Uh oh!", description="You don't have moderator perms.", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')

	@commands.command()
	async def banword(self, ctx, *, word: str=None):
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		try:
			with db_connection.connection() as conn:
				cursor = conn.cursor()
				server = await getServer(guild.id)
				prefix = server["server_prefix"]
				channel = ctx.message.channel
				if server["moderation_module"] == "Disabled":
					em = guilded.Embed(description="The moderation module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if word == None:
					em = guilded.Embed(title="Uh oh!", description="You didn't specify a word to be an banned!\n\n`Ex:` {}banword <word>".format(prefix), color=0x363942)
					await ctx.reply(embed=em)
					return
				moderator_or_not = False
				for i in author.roles:
					if i.permissions.manage_messages == True or i.permissions.kick_members == True:
						moderator_or_not = True
				if author == guild.owner:
					moderator_or_not = True
				if moderator_or_not == True:
					wordlist = []
					if wordlist is not None:
						if server["custom_blocked_words"] == None:
							pass
						else:
							for i in server["custom_blocked_words"]:
								wordlist.append(i)
					if str(word).lower() in wordlist:
						em = guilded.Embed(title="Wew!", description="The word argument is already banned.", color=0x363942)
						await ctx.reply(embed=em)
					else:
						if server["custom_blocked_words"] == None:
							new_value = ["{}".format(word.lower())]
							stmt = f"UPDATE servers SET custom_blocked_words=%s WHERE ID = '{guild.id}'"
							cursor.execute(stmt, (new_value,))
							conn.commit()
							em = guilded.Embed(title="Nice!", description="The word argument has been banned.", color=0x363942)
							await ctx.reply(embed=em)
						else:
							list_server = []
							for i in server["custom_blocked_words"]:
								list_server.append(i)
							list_server.append(word.lower())
							stmt = f"UPDATE servers SET custom_blocked_words=%s WHERE ID = '{guild.id}'"
							cursor.execute(stmt, (list_server,))
							conn.commit()
							em = guilded.Embed(title="Nice!", description="The word argument has been banned.", color=0x363942)
							await ctx.reply(embed=em)
				else:
					em = guilded.Embed(title="Uh oh!", description="You don't have moderator perms.", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')


	@commands.command()
	async def kick(self, ctx, *, member: guilded.Member=None):
		guild = await self.bot.fetch_server(ctx.guild.id)
		author = await guild.fetch_member(ctx.author.id)
		message = ctx.message
		info = fileIO("guilds/{}/info.json".format(guild.id), "load")
		channel = ctx.message.channel
		if info["moderation_module"] == "Disabled":
			em = guilded.Embed(description="The moderation module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		em = guilded.Embed(title="Uh oh!", description=":warning: Certain moderator commands are disabled until bots can fetch user roles/perms from the API again.", color=0x363942)
		await ctx.reply(embed=em)
		return
		moderator_or_not = False
		for i in author.roles:
			if i.permissions.manage_messages == True or i.permissions.kick_members == True:
				moderator_or_not = True
		if author == guild.owner:
			moderator_or_not = True
		if moderator_or_not == True:
			if member == None:
				em = guilded.Embed(title="Uh oh!", description="A user was not provided.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
				return
			if member == author:
				return
			await kick_check(self, ctx, member)
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have moderator perms.", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def ban(self, ctx, *, member: guilded.Member=None):
		guild = await self.bot.fetch_server(ctx.guild.id)
		author = await guild.fetch_member(ctx.message.author.id)
		channel = ctx.message.channel
		message = ctx.message
		info = fileIO("guilds/{}/info.json".format(guild.id), "load")
		if info["moderation_module"] == "Disabled":
			em = guilded.Embed(description="The moderation module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		em = guilded.Embed(title="Uh oh!", description=":warning: Certain moderator commands are disabled until bots can fetch user roles/perms from the API again.", color=0x363942)
		await ctx.reply(embed=em)
		return
		moderator_or_not = False
		for i in author.roles:
			if i.permissions.manage_messages == True or i.permissions.ban_members == True:
				moderator_or_not = True
		if author == guild.owner:
			moderator_or_not = True
		if moderator_or_not == True:
			if member == None:
				em = guilded.Embed(title="Uh oh!", description="A user was not provided.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
				return
			if member == author:
				return
			await ban_check(self, ctx, member)
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have moderator perms.", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def setlogchannel(self, ctx, *, arg: str=None):
		guild = ctx.guild
		author = ctx.author
		channel = ctx.message.channel
		message = ctx.message
		await command_processed(message, author)
		moderator_or_not = False
		for i in author.roles:
			if i.permissions.manage_messages == True or i.permissions.kick_members == True:
				moderator_or_not = True
		if author == guild.owner:
			moderator_or_not = True
		if moderator_or_not == True:
			try:
				with db_connection.connection() as conn:
					server = await getServer(guild.id)
					if not arg == None:
						if arg.lower() == "none" or arg.lower() == "reset":
							cursor = conn.cursor()
							cursor.execute(f"UPDATE servers SET logs_channel_id = 'None' WHERE ID = '{guild.id}'")
							conn.commit()
							em = guilded.Embed(title="Logs channel reset", description="None", color=0x363942)
							await ctx.reply(embed=em)
					else:
						cursor = conn.cursor()
						cursor.execute(f"UPDATE servers SET logs_channel_id = '{ctx.channel.id}' WHERE ID = '{guild.id}'")
						conn.commit()
						em = guilded.Embed(title="Logs channel set", description="{}".format(ctx.channel.id), color=0x363942)
						await ctx.reply(embed=em)
			except psycopg.DatabaseError as e:
				await ctx.reply(f'Error {e}')
		else:
			em = guilded.Embed(title="Uh oh!", description="You don't have mod perms to set a log channel.", color=0x363942)
			em.set_image(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)

	@commands.command()
	async def channelid(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		channel = await guild.fetch_channel(ctx.channel.id)
		await command_processed(message, author)
		moderator_or_not = False
		for i in author.roles:
			if i.permissions.manage_messages == True or i.permissions.kick_members == True:
				moderator_or_not = True
		if author == guild.owner:
			moderator_or_not = True
		if moderator_or_not == True:
			em = guilded.Embed(title="Channel ID retrieved.", description="{}".format(channel.id), color=0x363942)
			await ctx.reply(embed=em)

	@commands.command()
	@checks.is_dev()
	async def info(self, ctx):
		guild = ctx.guild
		author = await guild.fetch_member(ctx.message.author.id)
		channel = ctx.message.channel
		latency = str(self.bot.latency)
		member_count = 0
		for i in self.bot.guilds:
			member_count += i.member_count
		em = guilded.Embed(title="Rayz's Information", description="**Guilds:** {}\n**Ping:** {}{}ms\n**Users:** {}".format(len(self.bot.guilds), latency[2], latency[3], member_count), color=0x363942)
		em.set_footer(text="Reminder: This is only what's cached (It gets reset often). It doesn't display ALL information.")
		await ctx.reply(embed=em)

	@commands.command()
	@checks.is_dev()
	async def guildlist(self, ctx):
		author = ctx.message.author
		channel = ctx.message.channel
		guild = ctx.guild
		guild_list = []
		for i in self.bot.guilds:
			guild_list.append(i.name)
		em = guilded.Embed(title="Rayz's Guild list", description="**Guilds:**\n{}".format(" \n".join(guild_list)), color=0x363942)
		await ctx.reply(embed=em)

async def kick_check(self, ctx, member):
	author = ctx.author
	guild = ctx.guild
	baka = guild.get_member("m6oLkqLA")
	bot_has_perms = False
	bots_highest_role_num = -10000
	members_highest_role_num = -10000
	for i in baka.roles:
		if i.permissions.kick_members == True:
			bot_has_perms = True
		if i.position > bots_highest_role_num:
			bots_highest_role_num = int(i.position)
	if bot_has_perms == False:
		em = guilded.Embed(title="Uh oh!", description="I don't have the right permissions to kick members from this server.", color=0x363942)
		em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
		await ctx.reply(embed=em)
	else:
		for i in member.roles:
			if i.position > members_highest_role_num:
				members_highest_role_num = int(i.position)
		if bots_highest_role_num <= members_highest_role_num:
			em = guilded.Embed(title="Uh oh!", description="I cannot kick this user, they have a role equal to or higher than me.", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
		else:
			authors_highest_role_num = -10000
			for i in author.roles:
				if i.position > authors_highest_role_num:
					authors_highest_role_num = int(i.position)
			if authors_highest_role_num <= members_highest_role_num:
				em = guilded.Embed(title="Uh oh!", description="The user has the same, or higher role than you. I cannot kick them.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
			else:
				member_name = member.name
				if member.bot:
					em = guilded.Embed(title="Uh oh!", description="I'm programmed to not to kick bots, for crash related reasons.", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
					return
				await member.kick()
				em1 = guilded.Embed(title="User kicked.", description="**{}** was successfully kicked by <@{}>".format(member_name, author.id), color=0x363942)
				info = fileIO("guilds/{}/info.json".format(guild.id), "load")
				if info["logs_channel_id"] == "None":
					em1.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="Logs channel not set.")
				else:
					try:
						guild = await self.bot.fetch_team(ctx.guild.id)
						channel = await guild.fetch_channel(info["logs_channel_id"])
						em = guilded.Embed(title="A user was kicked.", description="**Name:** {}\n**ID:** {}".format(member.name, member.id), color=0x363942)
						em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="Kicked by {}".format(author.name))
						await channel.send(embed=em)
					except:
						em1.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						em1.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="There was an issue trying to send to the log channel. You might have to fix the ID.")
				await ctx.reply(embed=em1)

async def ban_check(self, ctx, member):
	author = ctx.author
	guild = ctx.guild
	baka = guild.get_member("m6oLkqLA")
	bot_has_perms = False
	bots_highest_role_num = -10000
	members_highest_role_num = -10000
	for i in baka.roles:
		if i.permissions.kick_members == True:
			bot_has_perms = True
		if i.position > bots_highest_role_num:
			bots_highest_role_num = int(i.position)
	if bot_has_perms == False:
		em = guilded.Embed(title="Uh oh!", description="I don't have the right permissions to ban members from the server.", color=0x363942)
		em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
		await ctx.reply(embed=em)
	else:
		for i in member.roles:
			if i.position > members_highest_role_num:
				members_highest_role_num = int(i.position)
		if bots_highest_role_num <= members_highest_role_num:
			em = guilded.Embed(title="Uh oh!", description="I cannot ban this user, they have a role equal to or higher than me.", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
		else:
			authors_highest_role_num = -10000
			for i in author.roles:
				if i.position > authors_highest_role_num:
					authors_highest_role_num = int(i.position)
			if authors_highest_role_num <= members_highest_role_num:
				em = guilded.Embed(title="Uh oh!", description="The user has the same, or higher role than you. I cannot ban them.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
			else:
				member_name = member.name
				if member.bot:
					em = guilded.Embed(title="Uh oh!", description="I'm programmed to not to kick bots, for crash related reasons.", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
					return
				await member.ban()
				em1 = guilded.Embed(title="User banned.", description="**{}** was successfully banned by <@{}>".format(member_name, author.id), color=0x363942)
				info = fileIO("guilds/{}/info.json".format(guild.id), "load")
				if info["logs_channel_id"] == "None":
					em1.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="Logs channel not set.")
				else:
					try:
						guild = await self.bot.fetch_team(ctx.guild.id)
						channel = await guild.fetch_channel(info["logs_channel_id"])
						em = guilded.Embed(title="A user was banned.", description="**Name:** {}\n**ID:** {}".format(member.name, member.id), color=0x363942)
						em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="Banned by {}".format(author.name))
						await channel.send(embed=em)
					except:
						em1.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						em1.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="There was an issue trying to send to the log channel. You might have to fix the ID.")
				await ctx.reply(embed=em1)

def setup(bot):
	bot.add_cog(Moderation(bot))
