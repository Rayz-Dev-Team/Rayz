import guilded
from guilded.ext import commands
from modules.generator import _check_values
from modules.generator import _check_inventory
from modules.generator import _check_inventory_member
from modules.generator import _check_values_member
from modules.generator import _check_values_guild
from modules.generator import check_leaderboard
from modules.generator import check_leaderboard_author
from modules.generator import command_processed
from core.database import *
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from tools.dataIO import fileIO

class Help(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, *, num: str=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await _check_values_guild(guild)
		await command_processed(message, author)
		await _check_values(author)

		economy_settings = fileIO("config/economy_settings.json", "load")
		config = fileIO("config/config.json", "load")

		support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
		members_support_guild = await support_guild.fetch_members()

		server = await getServer(guild.id)
		last_update = "{}".format(config["last_updated"])
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

		display_list = ["`1` • General `-` Enabled", "`2` • Fun `-` {}".format(fun_status), "`3` • Moderation `-` {}".format(mod_status), "`4` • Economy module `-` {}".format(economy_status)]
		if author in members_support_guild:
			author_support_guild = await support_guild.fetch_member(author.id)
			roles_list = await author_support_guild.fetch_role_ids()
			if config["staff_role_id"] in roles_list:
				display_list.append("`5` • Support staff `-` Enabled")
			if config["manager_role_id"] in roles_list:
				display_list.append("`6` • Management `-` Enabled")
			if config["developer_role_id"] in roles_list:
				display_list.append("`7` • Developer `-` Enabled")

		if num == None:
			em = guilded.Embed(title="Rayz - Help menu | Command modules", description="[optional] • <required>\n• Filter a page using `{}help 1`\n\n__**Help pages**__\n{}\n\n__**Other**__\n• `{}tos` to view our TOS.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)".format(prefix, " \n".join(display_list), prefix), color=0x363942)
			em.set_footer(text=f"{last_update}")
			await ctx.send(embed=em)
		elif num == "1" or num.lower() == "general" or num.lower() == "general module":
			em = guilded.Embed(title="General Module | Page 1", description=f"[optional] • <required>\n\n__**Main**__ [Enabled]\n{prefix}notes <user> `-` Displays your saved notes for said user.\n{prefix}addnote <user> <note> `-` Add a personal note for a user.\n{prefix}delnote <user> <NoteID> `-` Delete a personal note.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
			em.set_footer(text=f"{last_update}")
			await ctx.send(embed=em)
		elif num == "2" or num.lower() == "fun" or num.lower() == "fun module":
			em = guilded.Embed(title="Fun Module | Page 2", description=f"[optional] • <required>\n\n__**Fun module**__ [{fun_status}]\n{prefix}hug <user> `-` Hug a user.\n{prefix}cuddle <user> `-` Cuddle a user.\n{prefix}kiss <user> `-` Kiss a user.\n{prefix}feed <user> `-` Feed a user.\n{prefix}tickle <user> `-` Tickle a user.\n{prefix}pat <user> `-` Pat a user.\n{prefix}slap <user> `-` Slap a user.\n{prefix}yeet <user> `-` Yeet a user.\n{prefix}holdhand <user> `-` Hold a users hand.\n{prefix}highfive <user> `-` Highfive a user.\n{prefix}punch <user> `-` Punch a user.\n{prefix}bite <user> `-` Bite a user.\n{prefix}cry\n{prefix}bored\n{prefix}blush\n{prefix}dance\n{prefix}facepalm\n{prefix}happy\n{prefix}laugh\n{prefix}pout\n{prefix}shrug\n{prefix}sleep\n{prefix}wink\n{prefix}wave\n{prefix}urban <term>\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
			em.set_footer(text=f"{last_update}")
			await ctx.send(embed=em)
		elif num == "3" or num.lower() == "mod" or num.lower() == "moderation" or num.lower() == "moderation module":
			em = guilded.Embed(title="Moderation Module | Page 3", description=f"[optional] • <required>\n\n**Currently, only server owners can execute these commands.**\n\n__**Moderation**__ [{mod_status}]\n{prefix}changeprefix <prefix> `-` Change the prefix in this guild.\n{prefix}togglemodule `-` Toggle modules for your guild.\n{prefix}setlogchannel `-` Set the current channel to post logs in.\n{prefix}banword <word argument> `-` Bans usage of a word/phrase you don't like.\n{prefix}unbanword <word argument> `-` Unban usage of a word/phrase.\n{prefix}kick <user> `-` Kick a user from a Guild.\n{prefix}ban <user> `-` Ban a user from a Guild.\n{prefix}channelid `-` Get the channel ID in the channel you post this in.\n{prefix}settrafficlogs `-` Set the current channel to post traffic logs in.\n{prefix}setactionlogs `-` Set the current channel to post action logs in.\n{prefix}setwelcomechannel `-` Set the current channel to post welcome messages in.\n{prefix}setwelcomemessage <message> `-` Change the welcome message.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
			em.set_footer(text=f"{last_update}")
			await ctx.send(embed=em)
		elif num == "4" or num.lower() == "economy" or num.lower() == "economy module":
			em = guilded.Embed(title="Economy Module | Page 4", description=f"[optional] • <required>\n\n__**Economy**__ [{economy_status}]\n{prefix}profile `-` Display profile, and balance information.\n{prefix}work `-` Work for currency\n{prefix}weekly `-` Receive your weekly bonus.\n{prefix}gift <amount> <user> `-` Gift currency to a user.\n{prefix}withdraw <amount/all> `-` Make a withdraw from your bank.\n{prefix}deposit <amount/all> `-` Make a depsosit into your bank.\n{prefix}stats `-` View the economy settings for the guild.\n{prefix}leaderboard `-` Display the global economy leaderboard.\n{prefix}gift <amount> <user> `-` Gift others your currency.\n{prefix}give <item> <amount> <user> `-` Give others your items\nsell <item> `-` Sell your items.\n{prefix}dig `-` Dig up things!\n{prefix}prices `-` View a list of sellable item prices.\n{prefix}inventory `-` View your inventory.\n{prefix}slots <amount> `-` Bet and play some slots.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
			em.set_footer(text=f"{last_update}")
			await ctx.send(embed=em)
		elif num == "5" or num.lower() == "staff" or num.lower() == "support":
			if config["staff_role_id"] in roles_list:
				em = guilded.Embed(title="Rayz Staff Module | Page 5", description=f"[optional] • <required>\n\n`-` Rayz Staff commands are coming soon.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
		elif num == "6" or num.lower() == "manager" or num.lower() == "management":
			if config["manager_role_id"] in roles_list:
				em = guilded.Embed(title="Rayz Manager Module | Page 6", description=f"[optional] • <required>\n\n{prefix}toggle_partner `-` Enables/Disables partner status/benefits.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)
		elif num == "7" or num.lower() == "developer" or num.lower() == "dev":
			if config["developer_role_id"] in roles_list:
				em = guilded.Embed(title="Rayz Developer Module | Page 7", description=f"[optional] • <required>\n\n{prefix}load <module name> `-` Load up a module.\n{prefix}unload <module name> `-` Unload a current loaded module.\n{prefix}reload <module name> `-` Reload a currently loaded module.\n\n[Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)\n[Support Server](https://www.guilded.gg/i/E0LaMb4E)", color=0x363942)
				em.set_footer(text=f"{last_update}")
				await ctx.send(embed=em)

def setup(bot):
	bot.remove_command('help')
	bot.add_cog(Help(bot))
