import guilded
from guilded.ext import commands
from tools.dataIO import fileIO
from modules.generator import _check_values
from modules.generator import _check_values_guild
from core.database import *
from modules.generator import command_processed
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row

class General(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def changeprefix(self, ctx, pref: str=None):
		channel = ctx.channel
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await command_processed(message, author)
		await _check_values_guild(guild)
		try:
			server = await getServer(guild.id)
			if author == guild.owner:
				if pref == None:
					em = guilded.Embed(title="Uh oh!", description="You didn't define a prefix.\n\n`Ex: ?changeprefix ;`", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
				else:
					try:
						with db_connection.connection() as conn:
							cursor = conn.cursor()
							cursor.execute(f"UPDATE servers SET server_prefix = '{pref}' WHERE ID = '{guild.id}'")
							conn.commit()
						em = guilded.Embed(title="Success!", description="My prefix in this guild was changed to `{}`".format(str(pref)), color=0x363942)
						await ctx.reply(embed=em)
					except:
						em = guilded.Embed(title="Uh oh!", description="Unknown error, please contact the Developer.", color=0x363942)
						em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						await ctx.reply(embed=em)
			else:
				em = guilded.Embed(title="Uh oh!", description="You're not the server owner. Only the server owner can use this command.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			await ctx.reply(f'Error {e}')


	@commands.command(pass_context=True)
	async def togglemodule(self, ctx):
		channel = ctx.channel
		guild = ctx.guild
		author = ctx.author
		message = ctx.message
		await _check_values_guild(guild)
		await command_processed(message, author)
		try:
			with db_connection.connection() as conn:
				server = await getServer(guild.id)
				cursor = conn.cursor()
				if author == guild.owner:
					fun_status = server["fun_module"]
					mod_status = server["moderation_module"]
					if fun_status == "Enabled":
						fun_status = ":Rayz_Enabled:"
					elif fun_status == "Disabled":
						fun_status = ":Rayz_Disabled:"
					if mod_status == "Enabled":
						mod_status = ":Rayz_Enabled:"
					elif mod_status == "Disabled":
						mod_status = ":Rayz_Disabled:"
					em = guilded.Embed(title="Module config", description="__**Modules status**__\nFun module `-` {}\nModeration module `-` {}\n\n`-` What would you like to do?".format(fun_status, mod_status), color=0x363942)
					em.set_footer(icon_url = "https://cdn.discordapp.com/attachments/546687295684870145/969368622885662770/Rayz.png", text="Accepted responses: e, enable, d, disable")
					await ctx.reply(embed=em)
					def pred(m):
						return m.message.author == message.author
					answer1 = await self.bot.wait_for("message", check=pred)
					if answer1.message.content.lower() == "d" or answer1.message.content.lower() == "disable":
						if server["fun_module"] == "Disabled" and server["moderation_module"] == "Disabled":
							em = guilded.Embed(title="Uh oh!", description="There are no modules to disable. All modules are already disabled.", color=0x363942)
							em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
							await ctx.reply(embed=em)
						else:
							modules = []
							if server["fun_module"] == "Enabled":
								modules.append("fun")
							if server["moderation_module"] == "Enabled":
								modules.append("moderation")
							em = guilded.Embed(title="Module config", description="Which module would you like to disable?\n{}".format(" \n".join(modules)), color=0x363942)
							await ctx.reply(embed=em)
							def pred(m):
								return m.message.author == message.author
							answer1 = await self.bot.wait_for("message", check=pred)
							if answer1.message.content.lower() in modules:
								if answer1.message.content.lower() == "fun":
									if server["fun_module"] == "Enabled":
										cursor.execute(f"UPDATE servers SET fun_module = 'Disabled' WHERE ID = '{guild.id}'")
										conn.commit()
										em = guilded.Embed(title="Success!", description="The Fun module has been disabled.", color=0x363942)
										await ctx.reply(embed=em)
								elif answer1.message.content.lower() == "moderation":
									if server["moderation_module"] == "Enabled":
										cursor.execute(f"UPDATE servers SET moderation_module = 'Disabled' WHERE ID = '{guild.id}'")
										conn.commit()
										em = guilded.Embed(title="Success!", description="The Moderation module has been disabled.", color=0x363942)
										await ctx.reply(embed=em)
									else:
										em = guilded.Embed(title="Uh oh!", description="That module is already disabled.", color=0x363942)
										em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
										await ctx.reply(embed=em)
								else:
									em = guilded.Embed(title="Uh oh!", description="Invalid response.", color=0x363942)
									em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
									await ctx.reply(embed=em)
							else:
								em = guilded.Embed(title="Uh oh!", description="Invalid response.", color=0x363942)
								em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
								await ctx.reply(embed=em)
					elif answer1.message.content.lower() == "e" or answer1.message.content.lower() == "enable":
						if server["fun_module"] == "Enabled" and server["moderation_module"] == "Enabled":
							em = guilded.Embed(title="Uh oh!", description="There are no modules to enable. All modules are already enabled.", color=0x363942)
							em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
							await ctx.reply(embed=em)
						else:
							modules = []
							if server["fun_module"] == "Disabled":
								modules.append("fun")
							if server["moderation_module"] == "Disabled":
								modules.append("moderation")
							em = guilded.Embed(title="Module config", description="Which module would you like to enable?\n{}".format(" \n".join(modules)), color=0x363942)
							await ctx.reply(embed=em)
							def pred(m):
								return m.message.author == message.author
							answer1 = await self.bot.wait_for("message", check=pred)
							if answer1.message.content.lower() in modules:
								if answer1.message.content.lower() == "fun":
									if server["fun_module"] == "Disabled":
										cursor.execute(f"UPDATE servers SET fun_module = 'Enabled' WHERE ID = '{guild.id}'")
										conn.commit()
										em = guilded.Embed(title="Success!", description="The Fun module has been enabled.", color=0x363942)
										await ctx.reply(embed=em)
								elif answer1.message.content.lower() == "moderation":
									if server["moderation_module"] == "Disabled":
										cursor.execute(f"UPDATE servers SET moderation_module = 'Enabled' WHERE ID = '{guild.id}'")
										conn.commit()
										em = guilded.Embed(title="Success!", description="The Moderation module has been enabled.", color=0x363942)
										await ctx.reply(embed=em)
									else:
										em = guilded.Embed(title="Uh oh!", description="That module is already enabled.", color=0x363942)
										em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
										await ctx.reply(embed=em)
								else:
									em = guilded.Embed(title="Uh oh!", description="Invalid response.", color=0x363942)
									em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
									await ctx.reply(embed=em)
							else:
								em = guilded.Embed(title="Uh oh!", description="Invalid response.", color=0x363942)
								em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
								await ctx.reply(embed=em)
					else:
						em = guilded.Embed(title="Uh oh!", description="Invalid response.", color=0x363942)
						em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
						await ctx.reply(embed=em)
				else:
					em = guilded.Embed(title="Uh oh!", description="You're not the server owner. Only the server owner can use this command.", color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
		except psycopg.DatabaseError as e:
			await ctx.reply(f'Error {e}')


	@commands.command(pass_context=True)
	async def addnote(self, ctx, member: guilded.Member=None, *, note: str=None):
		author = ctx.message.author
		channel = ctx.message.channel
		guild = ctx.guild
		message = ctx.message
		await _check_values(author)
		await command_processed(message, author)
		em = guilded.Embed(title="Uh oh!", description="This command has been disabled by the Developer.", color=0x363942)
		em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
		return
		if member == None:
			return
		if note == None:
			em = guilded.Embed(title="Uh oh!", description="You didn't give me a note to add :(", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
			return
		else:
			info = fileIO("users/{}/info.json".format(author.id), "load")
			if member.id not in info["notes"]:
				info["notes"][str(member.id)] = {
					"counter": 1,
					"notes_list": {
						"1": {
							"content": "{}".format(str(note))
						}
					}
				}
				fileIO("users/{}/info.json".format(author.id), "save", info)
				em = guilded.Embed(title="Note added!", description="Note: `{}`".format(note), color=0x363942)
				await ctx.reply(embed=em)
			elif member.id in info["notes"]:
				baka = info["notes"][str(member.id)]["counter"] + 1
				info["notes"][str(member.id)]["notes_list"][str(baka)] = {
					"content": "{}".format(str(note))
				}
				info["notes"][str(member.id)]["counter"] += 1
				fileIO("users/{}/info.json".format(author.id), "save", info)
				em = guilded.Embed(title="Note added!", description="Note: `{}`".format(note), color=0x363942)
				await ctx.reply(embed=em)

	@commands.command(pass_context=True)
	async def delnote(self, ctx, member: guilded.Member=None, *, note: str=None):
		author = ctx.message.author
		channel = ctx.message.channel
		guild = ctx.guild
		message = ctx.message
		await _check_values(author)
		await command_processed(message, author)
		em = guilded.Embed(title="Uh oh!", description="This command has been disabled by the Developer.", color=0x363942)
		em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
		return
		if member == None:
			em = guilded.Embed(title="Uh oh!", description="You didn't give me a correct user argument :(", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
			return
		if note == None:
			em = guilded.Embed(title="Uh oh!", description="You didn't give me a note ID to delete :(", color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.reply(embed=em)
			return
		else:
			info = fileIO("users/{}/info.json".format(author.id), "load")
			if str(member.id) in info["notes"]:
				if str(note) in info["notes"][str(member.id)]["notes_list"]:
					info["notes"][str(member.id)]["notes_list"].pop(str(note))
					fileIO("users/{}/info.json".format(author.id), "save", info)
					em = guilded.Embed(title="Success!", description="The note by the ID of {} has been removed.".format(note), color=0x363942)
					await ctx.reply(embed=em)
				else:
					if info["notes"][str(member.id)]["notes_list"] == {}:
						baka = ["None"]
					else:
						baka = []
						for i in info["notes"][str(member.id)]["notes_list"]:
							baka.append(i)
					em = guilded.Embed(title="Uh oh!", description="That ID doesn't exist. `{}` :(\n\n**List of available ID's:**\n {}".format(note, " \n".join(baka)), color=0x363942)
					em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
					await ctx.reply(embed=em)
			else:
				em = guilded.Embed(title="Uh oh!", description="You don't have any notes for this user :(", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)

	@commands.command(pass_context=True)
	async def notes(self, ctx, *, member: guilded.Member=None):
		author = ctx.message.author
		channel = ctx.message.channel
		guild = ctx.guild
		message = ctx.message
		await _check_values(author)
		await command_processed(message, author)
		em = guilded.Embed(title="Uh oh!", description="This command has been disabled by the Developer.", color=0x363942)
		em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
		return
		if member == None:
			return
		else:
			info = fileIO("users/{}/info.json".format(author.id), "load")
			if member.id in info["notes"]:
				note_list = []
				for i in info["notes"][str(member.id)]["notes_list"]:
					note_list.append("{} `-` {}".format(i, info["notes"][str(member.id)]["notes_list"][i]["content"]))
				em = guilded.Embed(title="Here are the notes you have saved for this user!", description="**ID** `-` **Note**\n\n{}".format(" \n".join(note_list)), color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/d4ff26d3888068415e7f00af2442f471-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)
			else:
				em = guilded.Embed(title="Uh oh!", description="You've made 0 notes for this user.", color=0x363942)
				em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
				await ctx.reply(embed=em)

def setup(bot):
	bot.add_cog(General(bot))
