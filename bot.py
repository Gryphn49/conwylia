from time import time
from tkinter import N
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
- cities
- forts
- capital
- villages
- notable places

War based work:
- Naval Combat
- Land Combat

"""
    def __init__(self, name, owner, allies=[]):
        self.name = name
        self.owner = owner
        self.allies = allies

    def getName(self):
        return self.name
    
    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner

    def ally(self, ally):
        self.allies.append(ally)

    def getAllies(self):
        return self.allies
    
    def removeAlly(self, oldAlly):
        self.allies.remove(oldAlly)


nationFile = "storedNations.pkl"
# On startup, read from pickle file of previously created nations and create nations for them.

# storage dictionary pulled from pickle file of all nations & info 
with open(nationFile, "rb") as tf:
    stored = pickle.load(tf)
    tf.close()

print(stored)

# stored layout ==      stored = {"name" : {"owner":"x", "allies":["x","y"], ...}, "name2" : and so on}

nations = {key: Nation(key, stored[key]["owner"], stored[key]["allies"]) for key in stored} # creates nation class for each nation

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
gnq1 = 'What is the nation called?'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    mg = message.content
    if message.author == client.user:
        return

# shows all the commands accessable
    if mg == "&help":
        await message.channel.send("""
                                    The following commands are active: 
                                    \n &createNation -- Creates a nation in the database. 
                                    \n &nation -- Looks up info on a particular nation in the database. 
                                    \n &nations -- Lists all the nations in the database. 
                                    \n &deleteNation -- Deletes a nation from the database.
                                    \n &ally -- Allies with another nation in the database.
                                    \n &allies -- Lists all the allies of a nation in the database.
                                    \n &removeAlly -- Removes an allies between two nations.
                                    """)

# creating a nation in class nation
    if mg == "&createNation":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("Who is the owner?")
        Nowner = await client.wait_for("message", timeout=60.0)
        nations[Nname.content] = Nation(Nname.content, Nowner.content) # nation created  

        stored[nations[Nname.content].getName()] = {"owner" : nations[Nname.content].getOwner()} # nation added to storage dictionary
        # storing all the nations and info
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await message.channel.send("The nation " + Nname.content + " has been added to the database.")

# all the information about a nation
    if mg == "&nation": 
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        try:
            await message.channel.send("The nation " + nations[Nname.content].getName() + " is owned by " + nations[Nname.content].getOwner() + ".")
        except KeyError:
            await message.channel.send("That nation doesn't exist in the database.")

# lists all the nations in the database
    if mg == "&nations":
        nationsList = ""
        for key in stored:
            nationsList += (key + ", ")
        await message.channel.send("The nations currently in the database are: " + nationsList[:-2] + ".")

# deletes a nation from the database
    if mg == "&deleteNation":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        try:
            del nations[Nname.content]
            del stored[Nname.content]
            with open(nationFile, "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send("The nation " + Nname.content + " has been deleted from the database.")
        except KeyError:
            await message.channel.send("That nation doesn't exist in the database.")

# lists the allies of a nation in the database
    if mg == "&allies":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        if len(nations[Nname.content].getAllies()) == 2:
            await message.channel.send(nations[Nname.content].getName() + " has 2 allies in the database: " + nations[Nname.content].getAllies()[0] + " and " + nations[Nname.content].getAllies()[1])
        elif len(nations[Nname.content].getAllies()) == 1:
            await message.channel.send(nations[Nname.content].getName() + " has 1 ally in the database: " + nations[Nname.content].getAllies()[0])
        else: 
            await message.channel.send(nations[Nname.content].getName() + " has no allies in the database.")
    
# allies two nations both which are within the database
    if mg == "&ally":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("What nation are they allied with?")
        Nally = await client.wait_for("message", timeout=60.0)
        if len(nations[Nname.content].getAllies()) == 2:
            await message.channel.send(nations[Nname.content].getName() + " cannot ally with any more nations.")
            return
        if Nally.content in nations:
            if len(nations[Nally.content].getAllies()) == 2:
                await message.channel.send(nations[Nally.content].getName() + " cannot ally with any more nations.")
            nations[Nname.content].ally(Nally.content)
            nations[Nally.content].ally(Nname.content)
            stored[nations[Nname.content].getName()]["allies"] = nations[Nname.content].getAllies()
            stored[nations[Nally.content].getName()]["allies"] = nations[Nally.content].getAllies()
            with open(nationFile, "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send(nations[Nname.content].getName() +  " is now allied with " + Nally.content)
        else:
            await message.channel.send("The nation " + Nally.content + " doesn't exist in the database.")

# removes an alliance between two nations within the database
    if mg == "&removeAlly":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("What nation were they allied with?")
        Nally = await client.wait_for("message", timeout=60.0)
        if Nally.content in nations:
            nations[Nname.content].removeAlly(Nally.content)
            nations[Nally.content].removeAlly(Nname.content)
            stored[nations[Nname.content].getName()]["allies"] = nations[Nname.content].getAllies()
            stored[nations[Nally.content].getName()]["allies"] = nations[Nally.content].getAllies()
            with open(nationFile, "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send(nations[Nname.content].getName() +  " is no longer allied with " + Nally.content)
        else:
            await message.channel.send("The nation " + Nally.content + " doesn't exist in the database.")

# changes a nation's owner
    if mg == "&setOwner":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("Who is the new owner?")
        NNowner = await client.wait_for("message", timeout=60.0)
        nations[Nname.content].setOwner(NNowner.content)
        stored[nations[Nname.content].getName()]["owner"] = nations[Nname.content].getOwner()
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()


client.run('id')