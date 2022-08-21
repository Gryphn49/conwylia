from time import time
from tkinter import N
import discord
import pickle

# Class for all Nations

class Nation:
    """ 
to do list
- allies DONE
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
    def __init__(self, name, owner, allies=[], tps=[]):
        self.name = name
        self.owner = owner
        self.allies = allies
        self.tradePart = tps

    def getName(self):
        return self.name
    
    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner

    def ally(self, ally):
        self.allies.append(ally)

    def getAllies(self):
        allies = self.allies
        if len(allies) == 2:
            return (self.name + " has 2 allies in the database: " + allies[0] + " and " + allies[1])
        elif len(allies) == 1:
            return (self.name + " has 1 ally in the database: " + allies[0])
        else: 
            return (self.name + " has no allies in the database.")
    
    def removeAlly(self, oldAlly):
            self.allies.remove(oldAlly)

    def tradePartner(self, tp):
        self.tradePart.append(tp)

    def getTradePartners(self):
        name = self.name
        tps = self.tradePart()
        if len(tps) == 3:
            return (name + " has 3 trade partners in the database: " + tps[0] + " and " + tps[1] + " and " + tps[2])
        elif len(tps) == 2:
            return (name + " has 2 trade partners in the database: " + tps[0] + " and " + tps[1])
        elif len(tps) == 1:
            return (name + " has 1 trade partner in the database: " + tps[0])
        else: 
            return (name + " has no trade partners in the database.")


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

        stored[nations[Nname.content].name] = {"owner" : nations[Nname.content].owner} # nation added to storage dictionary
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
            await message.channel.send("The nation " + nations[Nname.content].name + " is owned by " + nations[Nname.content].owner + ".")
        except KeyError:
            await message.channel.send("That nation doesn't exist in the database.")

# lists all the nations in the database
    if mg == "&nations":
        await message.channel.send("The nations currently in the database are: " + ", ".join(stored.keys) + ".")

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
        await message.channel.send(nations[Nname.content].getAllies())
    
# allies two nations both which are within the database
    if mg == "&ally":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("What nation are they allied with?")
        Nally = await client.wait_for("message", timeout=60.0)
        if len(nations[Nname.content].getAllies()) == 2:
            await message.channel.send(nations[Nname.content].name + " cannot ally with any more nations.")
            return
        if Nally.content in nations:
            if len(nations[Nally.content].getAllies()) == 2:
                await message.channel.send(nations[Nally.content].name + " cannot ally with any more nations.")
                return
            if nations[Nally.content] not in nations[Nname.content].allies:
                await message.channel.send(nations[Nname.content].name + " is not allied with " + nations[Nally.content].name)
            nations[Nname.content].ally(Nally.content)
            nations[Nally.content].ally(Nname.content)
            stored[nations[Nname.content].name]["allies"] = nations[Nname.content].getAllies()
            stored[nations[Nally.content].name]["allies"] = nations[Nally.content].getAllies()
            with open(nationFile, "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send(nations[Nname.content].name +  " is now allied with " + Nally.content)
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
            stored[nations[Nname.content].name]["allies"] = nations[Nname.content].getAllies()
            stored[nations[Nally.content].name]["allies"] = nations[Nally.content].getAllies()
            with open(nationFile, "wb") as tf:
                pickle.dump(stored,tf)
                tf.close()
            await message.channel.send(nations[Nname.content].name +  " is no longer allied with " + Nally.content)
        else:
            await message.channel.send("The nation " + Nally.content + " doesn't exist in the database.")

# changes a nation's owner
    if mg == "&setOwner":
        await message.channel.send(gnq1)
        Nname = await client.wait_for("message", timeout=60.0)
        await message.channel.send("Who is the new owner?")
        NNowner = await client.wait_for("message", timeout=60.0)
        nations[Nname.content].setOwner(NNowner.content)
        stored[nations[Nname.content].name]["owner"] = nations[Nname.content].owner
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()


client.run('id')