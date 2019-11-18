import discord
import time
from discord.ext import commands
from classes.ad_lib import AdLibber
from asyncio import futures

bot = commands.Bot(command_prefix='!', description="A translater that tries its best")
bot.remove_command('help')
verbose = True
ad_lib = AdLibber(verbose)

@bot.event
async def on_ready():
    print ("Starting up...")
    print ("I am running as: " + bot.user.name)
    print ("With the ID: " + str(bot.user.id))

    await bot.change_presence(activity = discord.Game(name="!help"))

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

#region Hello
@bot.command()
async def hello(ctx):
    embed = discord.Embed()
    gif_url = 'https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif'
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)
#endregion

#region Help command
@bot.command()
async def help(ctx, *, args = None):
    help_str = ""

    if (args == None):
        help_str = '''```diff
Hello! My name is Anya. I am a terrible translator but I try my best!

The default prefix is !. To learn more about a command type !help [command].
Like this: !help translate

Commands:
> hello : Hi!
> help : Well, you got this far...
> translate : Ad-lib translation!
> language: Shows all supported languages and codes
```'''
    else:
        args = args.lower().strip()

        if args == 'translate':
            help_str = '''```!translate [number of seconds] [language1>language2>etc...]

Translate will record all messages in the channel for the given number of seconds. It then translates the messages as provided to create a fun conversation.

Ex:
    !translate 10 ko>ja>ru>en
```'''
        if args == 'languages':
            help_str = '''```!languages
Returns all language codes for use in the translate command.```'''

        else:
            help_str = "`I couldn't understand your input :(`"

    await ctx.send(help_str)
#endregion

#region Languages
@bot.command()
async def languages(ctx):
    await ctx.send(ad_lib.get_language_codes())
#endregion

#region Translate
@bot.command()
async def translate(ctx, seconds : int, languages : str):
    check_bool, check_str = ad_lib.check_languages(languages)

    if not check_bool:
        await ctx.send(check_str)
        return

    start_msg = await ctx.send("`Reading messages for the next {} seconds! #msg = {}`".format(str(seconds), str(0)))
    t_end = time.time() + seconds
    messages = []
    
    while time.time() < t_end:
        timeout = t_end - time.time()
        try:
            msg = await bot.wait_for('message', timeout=timeout)
            if msg.author.id != 645357754852048906:
                messages.append((msg.author.name, msg.content))
                await start_msg.edit(content="`Reading messages for the next {} seconds! #msg = {}`".format(str(seconds), str(len(messages))))
        except futures.TimeoutError:
            break
    
    if len(messages) > 0:
        if len(messages) != 1:
            await ctx.send("`I read {} messages. Translating now!`".format(len(messages)))
        else:
            await ctx.send("`I read {} message. Translating now!`".format(len(messages)))
        trans_convo = ad_lib.translate_and_format(messages, languages)
        await ctx.send(trans_convo)
    
    else:
        await ctx.send("`No input received in the past {} seconds.`".format(str(seconds)))
#endregion
    

token = ""
with open('token.txt') as f:
    token = f.readline()

bot.run(token)

