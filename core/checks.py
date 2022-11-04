from guilded.ext import commands
from tools.dataIO import fileIO

def is_dev_check(ctx):
	config = fileIO("config/config.json", "load")
	if str(ctx.message.author_id) in config["Developer"]:
		return True
	else:
		return False

def is_moderator_check(ctx):
	moderator_or_not = False
	for i in ctx.author.roles:
		if i.permissions.manage_messages == True or i.permissions.kick_members == True:
			moderator_or_not = True
	return moderator_or_not
		
def is_dev():
	return commands.check(is_dev_check)

def is_moderator():
	return commands.check(is_moderator_check)
