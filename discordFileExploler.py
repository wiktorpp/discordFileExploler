import discord
from TOKEN import TOKEN
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")

async def pager(string, function):
    stringWrapped = textwrap.wrap(str(string), 2000, replace_whitespace=False)
    for line in stringWrapped:
        await function(line)

@client.event
async def on_message(message):
    if message.content.startswith("$pwd"):
        await message.channel.send(os.getcwd())

    if message.content.startswith("$cd "):
        try:
            os.chdir(message.content[4:])
        except FileNotFoundError:
            await message.channel.send("ERROR: invalid directory name")

    if message.content.startswith("$ls"):
        await message.channel.send("\n".join(os.listdir()))

    if message.content.startswith("$open "):
        try:
            file = open(message.content[6:], "rb")
        except FileNotFoundError:
            await message.channel.send("ERROR: invalid file name")
        await message.channel.send(
            file = discord.File(file, file.name.split("/")[-1])
        )

    if message.content.startswith("$cat"):
        try:
            text = open(message.content[5:], "r").read()
        except FileNotFoundError:
            await message.channel.send("ERROR: invalid file name")
        await pager(text, message.channel.send)

client.run(TOKEN)

