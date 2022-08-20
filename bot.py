from time import time
import discord
import pickle

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

# storage dictionary pulled from pickle file of all nations & info 
with open("storedNations.pkl", "rb") as tf:
    stored = pickle.load(tf)
    tf.close()

print(stored)


nations = {key: Nation(key, stored[key]["owner"]) for key in stored} # creates nation class for each nation

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
        n1 = Nation(NName, msg.content) # nation created  
        stored[n1.getName()] = {"owner" : n1.getOwner()} # nation added to storage dictionary
        # storing all the nations and info
        with open("storedNations.pkl", "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()

    if message.content == "&nation":
        await message.channel.send('What is the nation called?')
        msg = await client.wait_for("message", timeout=60.0)
        msge = msg.content





client.run('id')