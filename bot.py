from time import time
import discord

# Class for all Nations

class Nation:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def getName(self):
        return self.name
    
    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner


# On startup, read from JSON file of previously created nations and create nations for them.

# lst = [] # from json file list of nations


# nations = {k: Nation(lst[k], "Unknown") for k in lst}


stored = {"A":"1#100","B":"2#400","C":"3#34"}
owners = []
for key in stored:
    owner = ""
    for i in stored[key]:
        if i != "#":
            owner += i
        else:
            owners.append(owner)
            break

useful = []
for key in stored:
    useful.append(key) # this is really really poorly coded, but works so :shrug:
nations = {key: Nation(key, owners[useful.index(key)]) for key in stored}

print(nations["A"].getName())
print(nations["A"].getOwner())


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# creating a nation in class nation
    if message.content == "&createNation":
        await message.channel.send('What is the nation called?')
        msg = await client.wait_for("message", timeout=60.0)
        NName = msg.content
        await message.channel.send("Who is the owner?")
        msg = await client.wait_for("message", timeout=60.0)
        n1 = Nation(NName, msg.content)
        stored[n1.getName()] = n1.getName() + "#" + n1.getOwner()

    if message.content == "&nation":
        await message.channel.send('What is the nation called?')
        msg = await client.wait_for("message", timeout=60.0)
        msge = msg.content





client.run('id')