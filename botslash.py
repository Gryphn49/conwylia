from cgi import test
from code import interact
from dis import disco
from time import time
from tkinter import N
import discord
import pickle
from discord import app_commands














# Class for all Nations

class Nation:
    """ 
to do list
- allies DONE
- trade partners -- more or less done
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
    def __init__(self, name, owner, allies=[], tps=[], union="", uP=""):
        self.name = name
        self.owner = owner
        self.allies = allies
        self.tradePart = tps
        self.union = union
        self.uP = uP # union partner

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
            return (f"{self.name} has 2 allies in the database: {allies[0]} and {allies[1]}.")
        elif len(allies) == 1:
            return (f"{self.name} has 1 ally in the database: {allies[0]}.")
        else: 
            return (f"{self.name} has no allies in the database.")
    
    def removeAlly(self, oldAlly):
            self.allies.remove(oldAlly)

    def tradePartner(self, tp):
        self.tradePart.append(tp)

    def getTradePartners(self):
        print("2")
        name = self.name
        tps = self.tradePart
        print("3")
        if len(tps) == 3:
            return (f"{name} has 3 trade partners in the database: {tps[0]} and {tps[1]} and {tps[2]}.")
        elif len(tps) == 2:
            return (f"{name} has 2 trade partners in the database: {tps[0]} and {tps[1]}.")
        elif len(tps) == 1:
            print("4")
            return (f"{name} has 1 trade partner in the database: {tps[0]}.")
        else: 
            return (f"{name} has no trade partners in the database.")

    def removeTradePartner(self, oldTp):
        self.tradePart.remove(oldTp)

    def unions(self):
        union = self.union
        if union == "False":
            return (f"{self.name} is not in a union in the database.")
        elif union == "Senior" or union == "Junior":
            return (f"{self.name} is in a union in the database with {self.uP}.")
        else: 
            return (f"{self.name} is not in a union in the database.")        


nationFile = "storedNations.pkl"
# On startup, read from pickle file of previously created nations and create nations for them.

# storage dictionary pulled from pickle file of all nations & info 
with open(nationFile, "rb") as tf:
    stored = pickle.load(tf)
    tf.close()

print(stored)

# to prevent nations from messing *everything* up
# for key in stored:    
#     stored[key]["union"] = ""





# stored layout ==      stored = {"name" : {"owner":"x", "allies":["x","y"], "tps":["x","y"], ...}, "name2" : and so on}

nations = {key: Nation(key, stored[key]["owner"], stored[key]["allies"], stored[key]["tps"]) for key in stored} # creates nation class for each nation






testServer = discord.Object(id=1010602651060277279)
class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=1010602651060277279))
            self.synced = True
        print(f'We have logged in as {self.user}')

client = aclient()
tree = app_commands.CommandTree(client)
gnq1 = 'What is the nation called?'


# creating a nation in class nation
@tree.command(name = "createnation", description="Creates a nation in the database.", guild = discord.Object(id=1010602651060277279))
async def self(interaction: discord.Interaction, name: str, owner: str):
    nations[name] = Nation(name, owner) # nation created  

    stored[nations[name].name] = {"owner" : nations[name].owner} # nation added to storage dictionary
    # storing all the nations and info
    with open(nationFile, "wb") as tf:
        pickle.dump(stored,tf)
        tf.close()
    await interaction.response.send_message(f"The nation {name} has been added to the database.")

# shows all the commands accessible
@tree.command(name = "help", description="Lists all the commands possible with Conwylia Bot.", guild = discord.Object(id=1010602651060277279))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("""
The following commands are active: 
```
/createNation (Name Of Nation) (Owner Of Nation)     -- Creates a nation in the database. 
/help                                                -- Lists all the commands possible with this bot.
/nation (Name of Nation)                             -- Looks up info on a particular nation in the database. 
/nations                                             -- Lists all the nations in the database. 
/deleteNation (Name of Nation)                       -- Deletes a nation from the database.
/ally (Name of Nation) (Name of Allied Nation)       -- Allies with another nation in the database.
/allies (Name of Nation)                             -- Lists all the allies of a nation in the database.
/removeAlly (Name of Nation) (Name of Allied Nation) -- Removes an allies between two nations.
/setowner (Name of Nation) (New Owner Name)          -- Changes the owner of a nation.
```
""")
 
# all the information about a nation
@tree.command(name = "nation", description = "Shows information about a nation.", guild = testServer)
async def self(interaction: discord.Interaction, name: str): 
    try:
        await interaction.response.send_message(f"The nation {nations[name].name} is owned by {nations[name].owner}.")
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)


# lists all the nations in the database
@tree.command(name="nations", description="Lists all the nations in the database.", guild=testServer)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("The nations currently in the database are: %s.")%", ".join(stored.keys())

# deletes a nation from the database
@tree.command(name="deletenation", description="Deletes a nation from the database.", guild=testServer)
async def self(interaction: discord.Interaction, name: str):
    try:
        del nations[name]
        del stored[name]
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"The nation {name} has been deleted from the database.")
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)

# lists the allies of a nation in the database
@tree.command(name="allies", description="Lists the allies of a nation in the database.", guild=testServer)
async def self(interaction: discord.Interaction, name: str):
    try:
        await interaction.response.send_message(nations[name].getAllies())
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)


# allies two nations both which are within the database
@tree.command(name="ally", description="Allies two nations that are within the database.", guild=testServer)
async def self(interaction: discord.Interaction, nation_name: str, allied_nation_name: str):
    if len(nations[nation_name].allies) == 2:
        await interaction.response.send_message(f"{nations[nation_name].name} cannot ally with any more nations.")
        return
    if allied_nation_name in nations:
        if len(nations[allied_nation_name].allies) == 2:
            await interaction.response.send_message(f"{nations[allied_nation_name].name} cannot ally with any more nations.")
            return
        nations[nation_name].ally(allied_nation_name)
        nations[allied_nation_name].ally(nation_name)
        stored[nations[nation_name].name]["allies"] = nations[nation_name].allies
        stored[nations[allied_nation_name].name]["allies"] = nations[allied_nation_name].allies
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is now allied with {nations[allied_nation_name].name}.")
    else:
        await interaction.response.send_message(f"The nation {allied_nation_name} doesn't exist in the database.")

# removes an alliance between two nations within the database
@tree.command(name="removeally", description="Removes an alliance between two nations within the database.", guild=testServer)
async def self(interaction: discord.Interaction, nation_name: str, allied_nation_name: str):
    if allied_nation_name in nations:
        if nations[allied_nation_name].name not in nations[nation_name].allies:
            await interaction.response.send_message(f"{nations[nation_name].name} is not allied with {nations[allied_nation_name].name}.")
            return
        nations[nation_name].removeAlly(allied_nation_name)
        nations[allied_nation_name].removeAlly(nation_name)
        stored[nations[nation_name].name]["allies"] = nations[nation_name].allies
        stored[nations[allied_nation_name].name]["allies"] = nations[allied_nation_name].allies
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is no longer allied with {allied_nation_name}.")
    else:
        await interaction.response.send_message(f"The nation {allied_nation_name} doesn't exist in the database.")

# changes a nation's owner
@tree.command(name="setowner", description="Changes a nation's owner", guild=testServer)
async def self(interaction:discord.Interaction, nation_name: str, new_owner: str):
    nations[nation_name].setOwner(new_owner)
    stored[nations[nation_name].name]["owner"] = nations[nation_name].owner
    with open(nationFile, "wb") as tf:
        pickle.dump(stored,tf)
        tf.close()
    await interaction.response.send_message(f"{nations[nation_name].owner} is the new owner of {nations[nation_name].name}.")

@tree.command(name="partner", description="Partners two nations in the database as trade partners.", guild=testServer)
async def self(interaction:discord.Interaction, nation_name: str, trade_partner_nation: str):
    if len(nations[nation_name].tradePart) == 3:
        await interaction.response.send_message(f"{nations[nation_name].name} cannot become trade partners with any more nations.")
        return
    if trade_partner_nation in nations:
        if len(nations[trade_partner_nation].tradePart) == 3:
            await interaction.response.send_message(f"{nations[trade_partner_nation].name} cannot become trade partners with any more nations.")
            return
        nations[nation_name].ally(trade_partner_nation)
        nations[trade_partner_nation].ally(nation_name)
        stored[nations[nation_name].name]["tps"] = nations[nation_name].allies
        stored[nations[trade_partner_nation].name]["tps"] = nations[trade_partner_nation].allies
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is now trade partners with {nations[trade_partner_nation].name}.")
    else:
        await interaction.response.send_message(f"The nation {trade_partner_nation} doesn't exist in the database.")

@tree.command(name="partners", description="Lists the trade partners of a nation in the database.", guild=testServer)
async def self(interaction:discord.Interaction, nation_name: str):
    try:
        print("1")
        await interaction.response.send_message(nations[nation_name].getTradePartners())
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)

@tree.command(name="removepartner", description="Removes a trade partnership between two nations in the database.", guild=testServer)
async def self(interaction:discord.Interaction, nation_name: str, trade_partner_nation: str):
    if trade_partner_nation in nations:
        if nations[trade_partner_nation].name not in nations[nation_name].tradePart:
            await interaction.response.send_message(f"{nations[nation_name].name} is not trade partners with {nations[trade_partner_nation].name}.")
            return
        nations[nation_name].removeTradePartner(trade_partner_nation)
        nations[trade_partner_nation].removeTradePartner(nation_name)
        stored[nations[nation_name].name]["tps"] = nations[nation_name].tradePart
        stored[nations[trade_partner_nation].name]["tps"] = nations[trade_partner_nation].tradePart
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is no longer trade partners with {trade_partner_nation}.")
    else:
        await interaction.response.send_message(f"The nation {trade_partner_nation} doesn't exist in the database.")

@tree.command(name=" ", description=" ", guild=testServer)
async def self(interaction:discord.Interaction):






try:
    client.run('id')
finally:
    print("Shutting down....") # eventually I'll move stored saving to here to make it simpler, but for now, it's safer for me not to.