import guilded
from guilded.ext import commands
import typing
import random
import math
import traceback
import time
from tools.dataIO import fileIO
from modules.generator import _check_values
from modules.generator import _check_inventory
from modules.generator import _check_inventory_member
from modules.generator import _check_values_member
from modules.generator import _check_values_guild
from modules.generator import check_leaderboard
from modules.generator import check_leaderboard_author
from modules.generator import command_processed
import psycopg
from psycopg_pool import ConnectionPool
from core.database import *
from tools.db_funcs import getUser
from tools.db_funcs import getServer
from tools.db_funcs import getAllUsers
from psycopg.rows import dict_row
from tools.functions import paginate
from tools.functions import roll_chance
import asyncio
import datetime
import simplejson
import re

from tools.db_funcs import getAllItems
from tools.db_funcs import getItem

class EconDev(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def edit_item(self, ctx, item: str=None, item_property: str=None):
        author = ctx.author
        message = ctx.message

        economy_settings = fileIO("config/economy_settings.json", "load")
        support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
        members_support_guild = await support_guild.fetch_members()

        if author in members_support_guild:
            author_support_guild = await support_guild.fetch_member(author.id)
            roles_list = await author_support_guild.fetch_role_ids()

        if config["developer_role_id"] in roles_list:
            properties_list = ["display_name", "description", "rarity", "giftable", "event", "obtain", "type", "enabled", "enabled_sell", "enabled_buy", "can_rotate", "sell_price", "buy_price"]
            if item is None:
                em = guilded.Embed(description="An Item ID wasn't specified.", color=0x363942)
                await ctx.reply(embed=em)
                return
            if item_property is None:
                em = guilded.Embed(description="An Item property wasn't specified.", color=0x363942)
                await ctx.reply(embed=em)
                return
            items = await getAllItems()
            item_list = []
            for i in items:
                item_list.append(i["item"])
            if item in item_list:
                item_data = await getItem(item)
                if item_property in properties_list:
                    with db_connection.connection() as conn:
                        cursor = conn.cursor()
                        if item_property == "display_name":
                            em = guilded.Embed(description="What would you like to set the display name to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["display_name"] = answer.message.content
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Display name updated.", description="`Display name:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "description":
                            em = guilded.Embed(description="What would you like to set the description to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["description"] = answer.message.content
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item description updated.", description="`Description:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "rarity":
                            em = guilded.Embed(description="What would you like to set the rarity to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["rarity"] = answer.message.content
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item rarity updated.", description="`Rarity:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "giftable":
                            em = guilded.Embed(description="What would you like to set giftable to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["giftable"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item giftable updated.", description="`Giftable:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["giftable"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item giftable updated.", description="`Giftable:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                        if item_property == "event":
                            em = guilded.Embed(description="What would you like to set events to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)

                            event_list = []

                            for i in answer.message.content.split():
                                event_list.append(i.lower())

                            if "none" in event_list:
                                item_data["data"]["event"] = []
                            else:
                                item_data["data"]["event"] = event_list

                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item events updated.", description="`Events:` {}\n\n{}".format(item_data["data"]["event"], infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "obtain":
                            em = guilded.Embed(description="What would you like to set obtains to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)

                            obtain_list = []

                            for i in answer.message.content.split():
                                obtain_list.append(i.lower())

                            if "none" in obtain_list:
                                item_data["data"]["obtain"] = []
                            else:
                                item_data["data"]["obtain"] = obtain_list

                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item obtains updated.", description="`Obtains:` {}\n\n{}".format(item_data["data"]["obtain"], infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "type":
                            em = guilded.Embed(description="What would you like to set the item type to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["type"] = answer.message.content
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Display name updated.", description="`Item type:` {}\n\n{}".format(item_data["data"]["type"], infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "enabled":
                            em = guilded.Embed(description="What would you like to set enabled to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["enabled"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled updated.", description="`Enabled:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["enabled"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled updated.", description="`Enabled:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)

                        

                        if item_property == "enabled_sell":
                            em = guilded.Embed(description="What would you like to set enabled_sell to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["shop"]["enabled_sell"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled_sell updated.", description="`enabled_sell:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["shop"]["enabled_sell"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled_sell updated.", description="`enabled_sell:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                        if item_property == "enabled_buy":
                            em = guilded.Embed(description="What would you like to set enabled_buy to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["shop"]["enabled_buy"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled_buy updated.", description="`enabled_buy:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["shop"]["enabled_buy"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item enabled_buy updated.", description="`enabled_buy:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                        if item_property == "can_rotate":
                            em = guilded.Embed(description="What would you like to set can_rotate to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["shop"]["can_rotate"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item can_rotate updated.", description="`can_rotate:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["shop"]["can_rotate"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item can_rotate updated.", description="`can_rotate:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                        if item_property == "can_rotate":
                            em = guilded.Embed(description="What would you like to set can_rotate to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            if answer.message.content.lower() == "true":
                                item_data["data"]["shop"]["can_rotate"] = True
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item can_rotate updated.", description="`can_rotate:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                            elif answer.message.content.lower() == "false":
                                item_data["data"]["shop"]["can_rotate"] = False
                                infoJson = json.dumps(item_data["data"])
                                cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                                em = guilded.Embed(title="Item can_rotate updated.", description="`can_rotate:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                                await ctx.send(embed=em)
                        if item_property == "sell_price":
                            em = guilded.Embed(description="What would you like to set the sell_price to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["shop"]["sell_price"] = int(answer.message.content)
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item sell_price updated.", description="`sell_price:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "buy_price":
                            em = guilded.Embed(description="What would you like to set the buy_price to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["shop"]["buy_price"] = int(answer.message.content)
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item buy_price updated.", description="`buy_price:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "min_drop":
                            em = guilded.Embed(description="What would you like to set the min_drop to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["drop"]["min_drop"] = int(answer.message.content)
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item min_drop updated.", description="`min_drop:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        if item_property == "max_drop":
                            em = guilded.Embed(description="What would you like to set the max_drop to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)
                            item_data["data"]["drop"]["max_drop"] = int(answer.message.content)
                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item max_drop updated.", description="`max_drop:` {}\n\n{}".format(answer.message.content, infoJson), color=0x363942)
                            await ctx.send(embed=em)

                        

                        if item_property == "opens":
                            em = guilded.Embed(description="What would you like to set opens to?", color=0x363942)
                            await ctx.reply(embed=em)
                            def pred(m):
                                return m.message.author == message.author
                            answer = await self.bot.wait_for("message", check=pred)

                            opens_list = []

                            for i in answer.message.content.split():
                                opens_list.append(i.lower())

                            if "none" in opens_list:
                                item_data["data"]["opens"] = []
                            else:
                                item_data["data"]["opens"] = opens_list

                            infoJson = json.dumps(item_data["data"])
                            cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                            em = guilded.Embed(title="Item opens updated.", description="`Opens:` {}\n\n{}".format(item_data["data"]["opens"], infoJson), color=0x363942)
                            await ctx.send(embed=em)
                        
            

    @commands.command()
    async def create_item(self, ctx, item: str=None):
        author = ctx.author
        guild = ctx.guild
        message = ctx.message


        economy_settings = fileIO("config/economy_settings.json", "load")
        support_guild = await self.bot.fetch_server(economy_settings["support_server_id"])
        members_support_guild = await support_guild.fetch_members()

        if author in members_support_guild:
            author_support_guild = await support_guild.fetch_member(author.id)
            roles_list = await author_support_guild.fetch_role_ids()

        if config["developer_role_id"] in roles_list:
            if item is None:
                em = guilded.Embed(description="An Item ID wasn't specified.", color=0x363942)
                await ctx.reply(embed=em)
                return
            data = {
                "display_name": None,
                "description": None,
                "rarity": None,
                "giftable": None,
                "event": [], 
                "obtain": [], 
                "type": None, 
                "enabled": False,
                "shop": {
                    "enabled_sell": False,
                    "enabled_buy": False,
                    "can_rotate": False,
                    "sell_price": None,
                    "buy_price": None
                },
                "opens": {},
                "drop": {
                    "min_drop": None,
                    "max_drop": None
                },
                "chest": {
                    "currency": {
                        "min_currency": 0,
                        "max_currency": 0
                        },
                    "items": {},
                    "locked": False
                }
            }
            items = await getAllItems()
            if item in items:
                em = guilded.Embed(description="An item with that ID already exists.", color=0x363942)
                await ctx.reply(embed=em)
            else:
                with db_connection.connection() as conn:
                    infoJson = json.dumps(data)
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO items(item) VALUES('{item}')")
                    cursor.execute(f"UPDATE items SET data = %s WHERE item = '{item}'", [infoJson])

                    em = guilded.Embed(title="An item was created.", description="`Item ID:` {}\n\n{}".format(item, infoJson), color=0x363942)
                    await ctx.reply(embed=em)
            
                 



def setup(bot):
	bot.add_cog(EconDev(bot))