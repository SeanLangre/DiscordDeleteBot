import os
import discord
import enum
import subprocess
from dotenv import load_dotenv


class ExtendedEnum(enum.Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Commands(ExtendedEnum):
    HELP = "$help"
    HELLO = "$hello"
    DELETE_ALL = "$delete-all"
    RUN_STOCK_SEARCH = "$start-search"


load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(Commands.HELP.value):
        await message.channel.send("{} ".format(Commands.list()))
    if message.content.startswith(Commands.HELLO.value):
        await message.channel.send("Hello! Type $help for help.")
    if message.content.startswith(Commands.DELETE_ALL.value):
        await DeleteAllMessages(message)
    if message.content.startswith(Commands.RUN_STOCK_SEARCH.value):
        await RunStockSearch(message)


async def RunStockSearch(message):
    await message.channel.send("Start Search")
    await DeleteAllMessages(message)
    subprocess.call([r"" + os.getenv("STONK_BOT_PATH")])


async def DeleteAllMessages(message):
    deleted = await message.channel.purge(limit=100)
    await message.channel.send("Deleted {} message(s)".format(len(deleted)))


client.run(os.getenv("DISCORD_TOKEN"))
