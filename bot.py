from time import time
import discord
import pickle

# Class for all Nations

class Nation:
    """ 
to do list
- allies
- trade partners
- population ?
- army size ? 
- is in union? junior or senior?
- treaties 
- war
- income
    - separated into different types via taxes, trade, and so on
- resources
- buildings
- expenses
- just kinda overall the time in the play world lol
- worked tiles

War based work:
- Naval Combat
- Land Combat

"""
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def getName(self):
        return self.name
    
    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner


# On startup, read from pickle file of previously created nations and create nations for them.

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
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("Who is the owner?")
        Nowner = await client.wait_for("message", timeout=60.0)
        nations[Nname.content] = Nation(Nname.content, Nowner.content) # nation created  

        stored[nations[Nname.content].getName()] = {"owner" : nations[Nname.content].getOwner()} # nation added to storage dictionary
        # storing all the nations and info
        with open("storedNations.pkl", "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await message.channel.send("The nation " + Nname.conent + " has been added to the database.")

# all the information about a nation
    if message.content == "&nation": 
        await message.channel.send('What is the nation called?')
        Nname = await client.wait_for("message", timeout=60.0)
        try:
            await message.channel.send("The nation " + nations[Nname.content].getName() + " is owned by " + nations[Nname.content].getOwner())
        except KeyError:
            await message.channel.send("That nation doesn't exist in the database.")

    if message.content == "&nations":
        nationsList = ""
        for key in stored:
            nationsList += (key + ", ")
        nationsList = nationsList[:-2]
        nationsList += "."
        await message.channel.send("The nations currently in the database are: " + nationsList)

    if message.content == "&deleteNation":
        await message.channel.send('What is the nation called?')
        Nname = await client.wait_for("message", timeout=60.0)
        try:
            del nations[Nname.content]
            del stored[Nname.content]
            with open("storedNations.pkl", "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send("The nation " + Nname.conent + " has been deleted from the database.")
        except KeyError:
            await message.channel.send("That nation doesn't exist in the database.")





client.run('id')