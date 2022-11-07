import guilded
from guilded.ext import commands
import json
import glob
import sys
import os
from core import checks
from core import prefix
import traceback
from tools.dataIO import fileIO
import logging

logger = logging.getLogger('guilded')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='guilded.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('config/config.json') as f:
    config = json.load(f)

token = config["Token"]
cogs = [os.path.basename(f) for f in glob.glob("modules/*.py")]
startup = ["modules." + os.path.splitext(f)[0] for f in cogs]
bot = commands.Bot(bot_id="acd5fc8c-4272-48d0-b78b-da1fecb1bab5", command_prefix=prefix.prefix, experimental_event_style=True)

@bot.event
async def on_ready():
    print(f"[ Online and connected to Guilded. User: {bot.user}]")
    print('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound)):
        return
    else:
        try:
            em = guilded.Embed(title="An error occured while trying to process your command.", description="`-` Screenshot this, and [send it to the developer](https://www.guilded.gg/i/E0LaMb4E)\n\n{}".format(error), color=0x363942)
            await ctx.reply(private=True, embed=em)
        except:
            print(error)

@bot.command()
@checks.is_dev()
async def load(ctx, *, cog_name: str):
    if not cog_name.startswith("modules."):
        cog_name = "modules." + cog_name
    try:
        bot.load_extension(cog_name)
    except Exception as e:
        em = guilded.Embed(description="Failed to load the module.", color=0x363942)
        await ctx.reply(embed=em)
        print('{}: {}'.format(type(e), e))
    else:
        em = guilded.Embed(description="**Module loaded.** :)", color=0x363942)
        await ctx.reply(embed=em)

@bot.command()
@checks.is_dev()
async def unload(ctx, *, cog_name: str):
    if not cog_name.startswith("modules."):
        cog_name = "modules." + cog_name

    if cog_name in bot.extensions:
        bot.unload_extension(cog_name)
        em = guilded.Embed(description="**Module unloaded.** :)", color=0x363942)
        await ctx.reply(embed=em)
    else:
        em = guilded.Embed(description="That module isn't loaded.", color=0x363942)
        await ctx.reply(embed=em)

@bot.command()
@checks.is_dev()
async def reload(ctx, *, cog_name: str = None):
    if cog_name == None:
        embed = guilded.Embed(description="Reloading... ('thank you not here, you are amazing, I love you' - Beezo)",colour=0x363942)
        await ctx.reply(embed = embed)
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        if not cog_name.startswith("modules."):
            cog_name = "modules." + cog_name
        try:
            bot.unload_extension(cog_name)
            bot.load_extension(cog_name)
        except Exception as e:
            em = guilded.Embed(description="Failed to reload the module.", color=0x363942)
            await ctx.reply(embed=em)
            print('{}: {}'.format(type(e), e))
        else:
            em = guilded.Embed(description="**Module reloaded.** :)", color=0x363942)
            await ctx.reply(embed=em)

@bot.event
async def on_message(message:guilded.Message):
    async def aexec(code, message:guilded.Message):
        exec(f'async def __ex(message):\n    '+(''.join(f'\n    {l}'for l in code.split('\n'))).strip())
        return (await locals()['__ex'](message))
    def evalcheck(message:guilded.Message):
        config = fileIO("config/config.json", "load")
        if str(message.author_id) in config["Developer"]:
            return True
        else:
            return False
    if evalcheck(message):
        if ((message.content).lower()).startswith('r-eval\n') or ((message.content).lower()).startswith('r-exec\n'):
            cmd = (((message.content)[7:])[:len(((message.content)[7:]))-0]).strip()
            try:
                await aexec(cmd, message)
            except Warning as e:
                result = ("".join(traceback.format_exception(e, e, e.__traceback__))).replace('`', '\`')
                await message.reply(f'**Eval ran with an warning:**\n\n```python\n{result}\n```')
                await message.add_reaction('⚠️')
            except Exception as e:
                result = ("".join(traceback.format_exception(e, e, e.__traceback__))).replace('`', '\`')
                await message.reply(f'**Eval failed with Exception:**\n\n```python\n{result}\n```')
                await message.add_reaction('❌')
            else:
                await message.add_reaction('✅')
    try:
        await bot.process_commands(message)
    except commands.CommandNotFound:
        pass


if __name__ == '__main__':
    for thing in startup:
        bot.load_extension(thing)
    bot.run(token)
