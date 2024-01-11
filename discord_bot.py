import discord
from threading import Thread
from utils import await_buster
import dotenv
import os

dotenv.load_dotenv()


intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)

process_count = -1
processes = {}


@client.event
async def on_ready():
    print("Ready to roll")


@client.event
async def on_message(msg):
    global processes

    if msg.author == client.user:
        return

    if "start" in msg.content or "track" in msg.content:
        process = get_process_id()
        processes[process] = True
        print(f"starting process {process}")

        async for user_msg, verbosity in await_buster(processes, process, timeout=120):
            await msg.reply(user_msg, mention_author=verbosity)

        processes[process] = False
        print(f"stopped process {process}")
        return

    elif "stop" in msg.content:
        for x in processes:
            processes[x] = False
        await msg.reply("stopped all processes", mention_author=False)
        print("stopped all processes")


def get_process_id():
    global process_count
    process_count += 1

    return process_count


client.run(os.environ["TOKEN"])
