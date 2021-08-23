import discord
import os
#import pynacl
#import dnspython
import server

from discord.ext import commands
from random import randrange

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

TOKEN = os.environ['token']
QUOTA_CHANNEL = os.environ['quota_channel']

quotas = []

@bot.event
async def on_ready():
    # get messages from quota
    channel = bot.get_channel(int(QUOTA_CHANNEL))
    global quotas
    quotas = await channel.history().flatten()

@bot.event
async def on_message(msg):
    # add new quotable message to [quotas] if one is posted in quota channel
    if msg.channel.id == int(QUOTA_CHANNEL) and not bot.user.mentioned_in(msg) and msg.author != bot.user:
      quotas.append(msg)
    # post a message from quotas
    if bot.user.mentioned_in(msg):
        resp = quotas[randrange(len(quotas))]
        # send attachments if there is one
        if len(resp.attachments) > 0:
          embed = discord.Embed()
          embed.set_image(url=resp.attachments[0].url)
          await msg.channel.send(embed=embed, content=resp.content)
        # send vanilla text message
        else:
          await msg.channel.send(content=resp.content)
      
server.server()
bot.run(TOKEN)

