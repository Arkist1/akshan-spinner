import discord
from threading import Thread
from utils import await_buster
import dotenv
import os

dotenv.load_dotenv()


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


client.run(os.environ["TOKEN"])
