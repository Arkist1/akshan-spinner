import discord
from threading import Thread
from utils import await_buster

intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Ready to roll")


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if "start" or "track" in msg.content:
        async for user_msg in await_buster():
            await msg.reply(user_msg)


TOKEN = "MTE3OTcwNTA4NjI4OTY0OTcwNA.GvredA.BI4i4MrwHGk2J_3FmeIxsmgQZ2TO0UfeCfcGk8"
client.run(TOKEN)
