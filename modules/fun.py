import guilded
from guilded.ext import commands
import aiohttp
from core.database import *
import tools.urbandictionary as urbandict
from modules.generator import command_processed
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row
import sys

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def hug(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "hug"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to hug.", color=0x363942)
			await ctx.send(embed=em)
			return
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/hug") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> hugs <@{}> :hugging_face:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/hug") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> hugs <@{}> :hugging_face:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def kiss(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "kiss"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to kiss.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/kiss") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> kisses <@{}> :kissing_smiling_eyes:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/kiss") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> kisses <@{}> :kissing_smiling_eyes:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def feed(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "feed"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to feed.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/feed") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> feeds <@{}> :pancakes:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/feed") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> feeds <@{}> :pancakes:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def tickle(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "tickle"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to tickle.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/tickle") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> tickles <@{}> :laughing:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/tickle") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> tickles <@{}> :laughing:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def pat(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "pat"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to pat.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/pat") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> pats <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/pat") as r:
							data = await r.json()
							await cs.close()
					print(data)
					data = data["file"]
					em = guilded.Embed(title='<@{}> pats <@{}> :flushed:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def slap(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "slap"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to slap.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/slap") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> slaps <@{}> :rage:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/slap") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> slaps <@{}> :rage:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def holdhand(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "holdhand"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to hold hands with.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/handhold") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> holds <@{}>'s hand".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/handhold") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> holds <@{}>'s hand".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def highfive(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "highfive"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to highfive.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/highfive") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> highfives <@{}>".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/highfive") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> highfives <@{}>".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def punch(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "punch"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to punch.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/punch") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> punches <@{}>".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/punch") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title="<@{}> punches <@{}>".format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def bite(self, ctx, *, member: guilded.Member=None):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		action = "bite"
		if member == None:
			em = guilded.Embed(description="You didn't mention anyone to bite.", color=0x363942)
			await ctx.send(embed=em)
		matching = await match_check(ctx, member, action)
		if not matching:
			server = await getServer(guild.id)
			if server["fun_module"] == "Disabled":
				em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
				await message.reply(private=True, embed=em)
				await message.delete()
				return
			else:
				try:
					await message.delete()
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/bite") as r:
							data = await r.json()
							await cs.close()
					data = data["file"]
					em = guilded.Embed(title='<@{}> bites <@{}> :rage:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)
				except:
					headers = {
						"Authorization": api_token
					}
					async with aiohttp.ClientSession(headers=headers) as cs:
						async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/bite") as r:
							data = await r.json()
							await cs.close()
					data = data["results"][0]["url"]
					em = guilded.Embed(title='<@{}> bites <@{}> :rage:'.format(author.id, member.id), color=0x363942)
					em.set_image(url=data)
					await ctx.send(embed=em)

	@commands.command()
	async def cry(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/cry") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title='<@{}> cries :sob:'.format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/cry") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title='<@{}> cries :sob:'.format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def blush(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/blush") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> blushes '-'".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/blush") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> blushes '-'".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def dance(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/dance") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> dances :D".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/dance") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> dances :D".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def shrug(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/shrug") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> shrugs".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/shrug") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> shrugs".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def wink(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/wink") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> winks".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/wink") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> winks".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def wave(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
			em = guilded.Embed(description="The fun module is disabled in this server.", color=0x363942)
			await message.reply(private=True, embed=em)
			await message.delete()
			return
		else:
			try:
				await message.delete()
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/wave") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> waves".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)
			except:
				headers = {
					"Authorization": api_token
				}
				async with aiohttp.ClientSession(headers=headers) as cs:
					async with cs.get("https://gallery.fluxpoint.dev/api/sfw/gif/wave") as r:
						data = await r.json()
						await cs.close()
				data = data["file"]
				em = guilded.Embed(title="<@{}> waves".format(author.id), color=0x363942)
				em.set_image(url=data)
				await ctx.send(embed=em)

	@commands.command()
	async def urban(self, ctx):
		author = ctx.author
		guild = ctx.guild
		message = ctx.message
		await command_processed(message, author)
		server = await getServer(guild.id)
		if server["fun_module"] == "Disabled":
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
