import guilded
from guilded.ext import commands
from modules.generator import _check_values_guild
import psycopg2
from core.database import *
from tools.db_funcs import getServer

class Help(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, *, num: str=None):
		guild = ctx.guild
		await _check_values_guild(guild)
		try:
			# connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			# unused connection removed to save bandwidth and resources and speed up
			server = await getServer(guild.id)
			last_update = "Last updated on 09/26/2022 at 10:15AM PST."
			prefix = server[3]
			if server[7] == "Enabled":
				fun_status = "Enabled"
			elif server[7] == "Disabled":
				fun_status = "Disabled"
			if server[6] == "Enabled":
				mod_status = "Enabled"
			elif server[6] == "Disabled":
				mod_status = ":Disabled"
			if server[8] == "Enabled":
				economy_status = "Enabled"
			elif server[8] == "Disabled":
				economy_status = "Disabled"
			if num == None:
				em = guilded.Embed(title="Rayz - Help menu | Command modules", description=f"[optional] • <required>\n• Filter a page using `{prefix}help 1`\n\n__**Help pages**__\n`1` • General `-` Enabled\n`2` • Fun `-` {fun_status}\n`3` • Moderation `-` {mod_status}\n`4` • Economy module `-` {economy_status}\n\n__**Other**__\n• `{prefix}tos` to view our TOS.\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
			elif num == "1" or num.lower() == "general" or num.lower() == "general module":
				em = guilded.Embed(title="General Module | Page 1", description=f"[optional] • <required>\n\n__**Main**__ [Enabled]\n{prefix}notes <user> `-` Displays your saved notes for said user.\n{prefix}addnote <user> <note> `-` Add a personal note for a user.\n{prefix}delnote <user> <NoteID> `-` Delete a personal note.\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
			elif num == "2" or num.lower() == "fun" or num.lower() == "fun module":
				em = guilded.Embed(title="Fun Module | Page 2", description=f"[optional] • <required>\n\n__**Fun module**__ [{fun_status}]\n{prefix}hug <user> `-` Hug a user.\n{prefix}cuddle <user> `-` Cuddle a user.\n{prefix}kiss <user> `-` Kiss a user.\n{prefix}feed <user> `-` Feed a user.\n{prefix}tickle <user> `-` Tickle a user.\n{prefix}pat <user> `-` Pat a user.\n{prefix}slap <user> `-` Slap a user.\n{prefix}yeet <user> `-` Yeet a user.\n{prefix}holdhand <user> `-` Hold a users hand.\n{prefix}highfive <user> `-` Highfive a user.\n{prefix}punch <user> `-` Punch a user.\n{prefix}bite <user> `-` Bite a user.\n{prefix}cry\n{prefix}bored\n{prefix}blush\n{prefix}dance\n{prefix}facepalm\n{prefix}happy\n{prefix}laugh\n{prefix}pout\n{prefix}shrug\n{prefix}sleep\n{prefix}wink\n{prefix}wave\n{prefix}urban <term>\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
			elif num == "3" or num.lower() == "mod" or num.lower() == "moderation" or num.lower() == "moderation module":
				em = guilded.Embed(title="Moderation Module | Page 3", description=f"[optional] • <required>\n\n**Currently, only server owners can execute these commands.**\n\n__**Moderation**__ [{mod_status}]\n{prefix}changeprefix <prefix> `-` Change the prefix in this guild.\n{prefix}togglemodule `-` Toggle modules for your guild.\n{prefix}setlogchannel `-` Set the current channel to post logs in.\n{prefix}banword <word argument> `-` Bans usage of a word/phrase you don't like.\n{prefix}unbanword <word argument> `-` Unban usage of a word/phrase.\n{prefix}kick <user> `-` Kick a user from a Guild.\n{prefix}ban <user> `-` Ban a user from a Guild.\n{prefix}channelid `-` Get the channel ID in the channel you post this in.\n{prefix}settrafficlogs `-` Set the current channel to post traffic logs in.\n{prefix}setactionlogs `-` Set the current channel to post action logs in.\n{prefix}setwelcomechannel `-` Set the current channel to post welcome messages in.\n{prefix}setwelcomemessage <message> `-` Change the welcome message.\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
			elif num == "4" or num.lower() == "economy" or num.lower() == "economy module":
				em = guilded.Embed(title="Economy Module | Page 4", description=f"[optional] • <required>\n\n__**Economy**__ [{economy_status}]\n{prefix}profile `-` Display profile, and balance information.\n{prefix}work `-` Work for currency\n{prefix}weekly `-` Receive your weekly bonus.\n{prefix}gift <amount> <user> `-` Gift currency to a user.\n{prefix}withdraw <amount/all> `-` Make a withdraw from your bank.\n{prefix}deposit <amount/all> `-` Make a depsosit into your bank.\n{prefix}stats `-` View the economy settings for the guild.\n{prefix}leaderboard `-` Display the global economy leaderboard.\n{prefix}gift <amount> <user> `-` Gift others your currency.\n{prefix}give <item> <amount> <user> `-` Give others your items\nsell <item> <amount> `-` Sell your items.\nprices `-` View a list of sellable item prices.\ninventory `-` View your inventory.\nslots <amount> `-` Bet and play some slots.\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
		except psycopg2.DatabaseError as e:
			em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
			await ctx.send(embed=em)

	# removed because not halloween
	# @commands.command()
	# async def halloween(self, ctx):
	# 	guild = ctx.guild
	# 	await _check_values_guild(guild)
	# 	try:
	# 		connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
	# 		server = await getServer(guild.id)
	# 		footer = "The halloween event is now live!"
	# 		prefix = server[3]
	# 		em = guilded.Embed(title="Halloween information", description=f"[optional] • <required>\n-------------------------------------------------\nIt's almost October and Halloween's approaching fast! We have a ton of cool new seasonal features for you to discover. Have a spooktacular day!\n\n🎃 __**Information**__\nCandies have been added, along with rarities in `{prefix}work`. It's probably best you collect these, and trade people for a price!\n\n__**New commands!**__\n{prefix}prices `-` View candy sell prices\n{prefix}sell <item> <amount> `-` Sell your candy\n{prefix}give <item> <amount> <user> `-` Give others your candy!\n{prefix}inv `-` View your inventory.\n{prefix}gift <amount> <user> `-` Gift your currency to others. Trading?\n\n👻 __**Other**__\n• `{prefix}tos` to view our TOS.\n\n[Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
	# 		em.set_footer(text=f"{footer}")
	# 		await ctx.send(embed=em)
	# 	except psycopg2.DatabaseError as e:
	# 		em = guilded.Embed(title="Uh oh!", description="Error. {}".format(e), color=0x363942)
	# 		await ctx.send(embed=em)

def setup(bot):
	bot.remove_command('help')
	bot.add_cog(Help(bot))
