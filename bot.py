import discord
import time
from discord.ext import commands
from classes.ad_lib import AdLibber

bot = commands.Bot(command_prefix='?', description="A translater that tries its best")
ad_lib = AdLibber()

@bot.event
async def on_ready():
    print ("Starting up...")
    print ("I am running as: " + bot.user.name)
    print ("With the ID: " + str(bot.user.id))

    await bot.change_presence(activity = discord.Game(name="!help"))

@bot.command()
async def hello(ctx):
    embed = discord.Embed()
    gif_url = 'https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif'
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

@bot.command()
async def translate(ctx, seconds : int, languages : str):
    start_msg = await ctx.send("`Reading messages for the next {} seconds!`".format(str(seconds)))
    t_end = time.time() + seconds
    messages = []

    while time.time() < t_end:
        msg = await bot.wait_for('message')
        if msg.author.id != 645357754852048906:
            messages.append((msg.author.name, msg.content))
            emoji = '\N{THUMBS UP SIGN}'
            await start_msg.add_reaction(emoji)
    
    if len(messages) > 0:
        await ctx.send("`I read {} messages. Translating now!`".format(len(messages)))
        trans_convo = ad_lib.translate_and_format(messages, languages)
        await ctx.send(trans_convo)
    
    else:
        await ctx.send("`No input received in the past {} seconds.`".format(str(seconds)))
    
    

token = ""
with open('token.txt') as f:
    token = f.readline()

bot.run(token)

