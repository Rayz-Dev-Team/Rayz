import os
import re
import discord
from discord.ext import commands
from tools.dataIO import fileIO

def is_dm_check(ctx):
	guild = ctx.guild
	if guild:
		return False
	else:
		return True
		
def is_dev_check(ctx):
	config = fileIO("config/config.json", "load")
	if str(ctx.message.author.id) in config["Dev"]:
		return True
	else:
		return False
 
def is_dm():
	return commands.check(is_dm_check)
	
def is_dev():
	return commands.check(is_dev_check)