import guilded
from guilded.ext import commands
import asyncio
import json
import aiohttp
import random 
from tools.dataIO import fileIO
import psycopg2
from psycopg2 import Error
from core.database import *
import requests
import tools.urbandictionary as urbandict

class Fun(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def hug(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "hug"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to hug.", color=0x363942)
			await ctx.send(embed=em)
			return
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/hug")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> hugs <@{}> :hugging_face:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/hug")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> hugs <@{}> :hugging_face:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def cuddle(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "cuddle"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/cuddle")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> cuddles <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/cuddle")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> cuddles <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def kiss(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "kiss"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to kiss.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/kiss")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> kisses <@{}> :kissing_smiling_eyes:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/kiss")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> kisses <@{}> :kissing_smiling_eyes:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def feed(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "feed"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to feed.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/feed")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> feeds <@{}> :pancakes:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/feed")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> feeds <@{}> :pancakes:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def tickle(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "tickle"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to tickle.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/tickle")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> tickles <@{}> :laughing:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/tickle")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> tickles <@{}> :laughing:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def pat(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "pat"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to pat.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/pat")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> pats <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/pat")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> pats <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def slap(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "slap"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to slap.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to slap.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/slap")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> slaps <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/slap")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> slaps <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def yeet(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "yeet"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to yeet.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/yeet")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> yeets <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/yeet")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> yeets <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def holdhand(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "holdhand"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to hold hands with.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/handhold")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> holds <@{}>'s hand".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/handhold")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> holds <@{}>'s hand".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def highfive(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "highfive"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to highfive.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/highfive")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> highfives <@{}>".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/highfive")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> highfives <@{}>".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def punch(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "punch"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to punch.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/punch")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> punches <@{}>".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/punch")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title="<@{}> punches <@{}>".format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def bite(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		action = "bite"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to cuddle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			try:
				connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
				async def getServer():
					with connection:
						cursor = connection.cursor()
						cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
						content = cursor.fetchone()
					return content
				server = await getServer()
				if server[7] == "Disabled":
					em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
					await message.reply(private=True, embed=em)
					await message.delete()
					return
				if member == None:
					em = guilded.Embed(description="You didn't mention anyone to slap.", color=0x363942)
					await ctx.send(embed=em)
				else:
					try:
						await message.delete()
						resp = requests.get("https://nekos.best/api/v2/bite")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> bites <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
					except:
						resp = requests.get("https://nekos.best/api/v2/bite")
						data = resp.json()
						data = data["results"][0]["url"]
						em = guilded.Embed(title='<@{}> bites <@{}> :rage:'.format(author.id, member.id), color=0x363942)
						em.set_image(url=data)
						await ctx.send(embed=em)
				connection.close()
			except psycopg2.DatabaseError as e:
				await ctx.send(f'Error {e}')

	@commands.command()
	async def cry(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/cry")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title='<@{}> cries :sob:'.format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/cry")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title='<@{}> cries :sob:'.format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def bored(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/bored")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title='<@{}> is bored ;-;'.format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/bored")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title='<@{}> is bored ;-;'.format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def blush(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/blush")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> blushes '-'".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/blush")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> blushes '-'".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def dance(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/dance")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> dances :D".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/dance")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> dances :D".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def facepalm(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/facepalm")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> facepalms smh".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/facepalm")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> facepalms smh".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def happy(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/happy")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> is happy :3".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/happy")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> is happy :3".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def laugh(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/laugh")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> is laughing :joy:".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/laugh")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> is laughing :joy:".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def pout(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/pout")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> pouts ;-;".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/pout")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> pouts ;-;".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def shrug(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/shrug")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> shrugs".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/shrug")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> shrugs".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def sleep(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/sleep")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> sleeps".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/sleep")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> sleeps".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def wink(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/wink")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> winks".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/wink")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> winks".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

	@commands.command()
	async def wave(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					resp = requests.get("https://nekos.best/api/v2/wave")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> waves".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					resp = requests.get("https://nekos.best/api/v2/wave")
					data = resp.json()
					data = data["results"][0]["url"]
					em = guilded.Embed(title="<@{}> waves".format(author.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')
   
	@commands.command()
	async def urban(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		try:
			connection = psycopg2.connect(user=database_username, password=database_password, port=database_port, database=database_name)
			async def getServer():
				with connection:
					cursor = connection.cursor()
					cursor.execute(f"SELECT * FROM servers WHERE ID = '{guild.id}'")
					content = cursor.fetchone()
				return content
			server = await getServer()
			if server[7] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				searchwordslist = message.content.split(" ")[1::]
				searchwords = ' '.join(searchwordslist)
				try:
					await message.delete()
					definition = urbandict.define(searchwords)[0]
					gibdef = definition.definition
					if len(definition.definition) > 300:
						gibdef = definition.definition[0:297]+'...'
					em = guilded.Embed(title=f"Urban meaning of {definition.word}:",description=f"{gibdef} \n \n 👍: {definition.upvotes} \n 👎: {definition.downvotes}", color=0x363942)
					await ctx.send(embed=em)
				except:
					await message.delete()
					em = guilded.Embed(title=f"<@{author.id}> An error occurred please try again later. ", color=0x363942)
					await ctx.send(embed=em)
			connection.close()
		except psycopg2.DatabaseError as e:
			await ctx.send(f'Error {e}')

async def match_check(ctx, member, action):
	author = ctx.author
	guild = ctx.guild
	message = ctx.message
	if author.id == member.id:
		try:
			await message.delete()
			em = guilded.Embed(title="Uh oh!", description="You can't {} yourself <@{}>".format(action, author.id), color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.send(embed=em)
			return True
		except:
			em = guilded.Embed(title="Uh oh!", description="You can't {} yourself <@{}>".format(action, author.id), color=0x363942)
			em.set_thumbnail(url="https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160")
			await ctx.send(embed=em)
			return True

def setup(bot):
	bot.add_cog(Fun(bot))