import discord
import pickle
from discord import app_commands
from typing import List
from discord import ui






""" 
to do list
- allies DONE
- trade partners -- more or less done
- population DONE -- I don't like it, but it's done.
- army size ? 
- is in union? junior or senior?  -- more or less done (until war is done)
- treaties 
- war
- income
    - separated into different types via taxes, trade, and so on
- resources -- partially done
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

# class Resource():

#     def __init__(self):
#         return

# calling a nation's resource 
resIron = dict(name="Iron", type="Mil", desc="Used to equip armies with weapons.")
resHorse = dict(name="Horse", type="Mil", desc="Horses are used by the cavalry units of a nation.")
resWood = dict(name="Wood", type="Mil", desc="Wood is used to make ships.")

resGold = dict(name="Gold", type="Lux", desc="Gold has always been very rare and an expensive luxury item.")
resGem = dict(name="Gems", type="Lux", desc="Jewels have always been very rare and expensive luxury items.")
resSpice = dict(name="Spices", type="Lux", desc="Spices are a very good way to preserve and season foods, and are a hot commodity among people who can get their hands on them.")
resFur = dict(name="Furs", type="Lux", desc="Furs are an essential luxury item to those living in cold climates, or just want to look fancy.")

# this is the tile class for all nation's tiles
# class Tile:

#      def __init__(self, name, pop, res, rt):
#          self.name = name # type of tile
#          self.pop = pop # population of said tile in thousands
#          self.res = res # resources of tile in a list displaying the Resource instance of the resources given by the tile.
#          self.rt = rt # rough terrain y/n

tileMountain = dict(name="Mountain", pop=5, res=[resIron], rt=True, workedNum=3)         # sometimes gold/gems
tileHills = dict(name="Hills", pop=15, res=[], rt=True, workedNum=8)                     # sometimes iron
tilePlains = dict(name="Plains", pop=20, res=[], rt=False, workedNum=10)                  # sometimes horse
tileSavannah = dict(name="Savannah", pop=15, res=[], rt=False, workedNum=8)              # sometimes horse or iron
tileTundra = dict(name="Tundra", pop=10, res=[], rt=False, workedNum=5)                  # sometimes fur
tileForest = dict(name="Forest", pop=15, res=[resWood, resWood], rt=True, workedNum=8)   # no sometimes :)
tileTaiga = dict(name="Taiga", pop=10, res=[resWood, resWood], rt=True, workedNum=5)     # sometimes fur
tileMarsh = dict(name="Marsh", pop=10, res=[resWood], rt=True, workedNum=5)              # no sometimes :)
tileJungle = dict(name="Jungle", pop=5, res=[resWood, resWood], rt=True, workedNum=3)    # sometimes spice
tileDesert = dict(name="Desert", pop=0, res=[], rt=False, workedNum=0)                   # 
tileIce = dict(name="Ice", pop=0, res=[], rt=False, workedNum=0)                         # sometimes gold or iron
tileLake = dict(name="Lake", pop=0, res=[], rt=False, workedNum=0)                       #
tileRiver = dict(name="River", pop=0, res=[], rt=False, workedNum=0)                     #
tileOcean = dict(name="Ocean", pop=0, res=[], rt=False, workedNum=0)                     #

tileTypes = [tileMountain,tileHills,tilePlains,tileSavannah,tileTundra,tileForest]
tileNametoClass = {"Mountain":tileMountain,"Hills":tileHills,"Plains":tilePlains,"Savannah":tileSavannah,"Tundra":tileTundra,"Forest":tileForest} # etc.



# Class for all Nations


# so when you want to access a nation's resource, you want to see what resources they have access to through which tiles they have, which gives the resource instance of whatever resource
# the number of resource calculation is done IN Nation, based purely on Tile. 

class Nation:

    def __init__(self, name, owner, allies=[], tps=[], union="", uP="", tiles=[]): # these things are necessary to be stored to memory.
        # base information
        self.name = name # name of nation
        self.owner = owner # name of owner (of nation)
        self.tiles = tiles # list of Tile instances that the nation has

        # diplomacy
        self.allies = allies # list of allies
        self.tradePart = tps # list  of trade partners
        self.unionStatus = union # is union -- Options: blank (not set), False, Senior, Junior
        self.uP = uP # union partner

        # resources 
        self.resources = [] # a list of resource dictionary instances
        for tile in self.tiles: # for each individual tile, find the resources
            self.resources += tile["res"] # this defines the resources of the nation
        
        # population
        self.pop = 0 # population of nation IN THOUSANDS
        # population due to tiles
        for tile in self.tiles: # for each individual tile, find the population due to tiles
            self.pop += tile["pop"] # this defines the population of the nation (based on the tiles)
        #worked tiles
        self.wtNumMax = (6 if len(self.tiles) < 11 else 5 if len(self.tiles) < 16 else 4 if len(self.tiles) < 21 else 2 if len(self.tiles) < 26 else 0)  # max worked tiles number
        self.wtList = [] # list of all worked tiles
        for tile in self.wtList: # for each worked tile
            self.pop += tile["workedNum"] # this defines the population added by worked tiles
        # communities
        self.villages = [] # total list of villages
        self.pop += len(self.villages)*5 # adding population due to villages
        self.towns = [] # total list of towns
        self.pop += len(self.towns)*10 # adding population due to towns
        self.cities = [] # total list of cities
        self.pop += len(self.cities)*20 # adding population due to cities
        self.capital = "" # there can only be one capital, so name of capital
        self.capital += (30 if self.capital != "" else 0) # adding population due to capital
        self.communitiesNum = len(self.villages)+len(self.towns)+len(self.cities)+(1 if self.capital != "" else 0) # total number of commuinities -- on second though, this will not be overly useful :)
        # water access
        self.wA = 0 # water access
        

        # income
        self.income = 0 # overall income of a nation
        self.taxes = 0 # overall income due to taxes
        self.idk = 0

    def setOwner(self, newOwner): # sets a new owner
        self.owner = newOwner

    def ally(self, ally): # allies with another nation (adds an ally to the allies list) -- does not check to see if it's an actual nation here. That's done a bit more frontly.
        self.allies.append(ally)

    def getAllies(self): # returns a response of how many allies.
        allies = self.allies
        if len(allies) == 2: # max is 2 allies, so it increments down. Probably a neater way to do this, but this is fairly simple and works so eh...
            return (f"{self.name} has 2 allies in the database: {allies[0]} and {allies[1]}.")
        elif len(allies) == 1:
            return (f"{self.name} has 1 ally in the database: {allies[0]}.")
        else: 
            return (f"{self.name} has no allies in the database.")
    
    def removeAlly(self, oldAlly): # removes an ally from the allies list.
            self.allies.remove(oldAlly)

    def tradePartner(self, tp): # adds a trade partner to the tradePart list -- check is done frontly again
        self.tradePart.append(tp)

    def getTradePartners(self): # returns a response of how many trade partners
        name = self.name
        tps = self.tradePart
        if len(tps) == 3: # max is 3 trade partners, so it increments down. getAllies is done the same way, so there's probably a better way but it works....
            return (f"{name} has 3 trade partners in the database: {tps[0]} and {tps[1]} and {tps[2]}.")
        elif len(tps) == 2:
            return (f"{name} has 2 trade partners in the database: {tps[0]} and {tps[1]}.")
        elif len(tps) == 1:
            print("4")
            return (f"{name} has 1 trade partner in the database: {tps[0]}.")
        else: 
            return (f"{name} has no trade partners in the database.")

    def removeTradePartner(self, oldTp): # removes a trade partner from the tradePart list
        self.tradePart.remove(oldTp)

    def unions(self): # returns whether the nation is in a union or not.
        if self.uP != "": # this does not say whether they are a senior or junior nation cuz imo doesn't really matter outside of rp rules. I could add it, but I could also just add another command to check that.
            return (f"{self.name} is in a union in the database with {self.uP}.")
        else: 
            return (f"{self.name} is not in a union in the database.")

    def unionize(self, union_Nation, seniority): # allows a nation to unionize with another nation
        self.uP = union_Nation # sets the other nation as said union partner (uP)
        if seniority == True: # sets senior nation vs junior nation
            self.unionStatus = "Senior"
        else: 
            self.unionStatus = "Junior"

    def deUnionize(self): # removes a union, just sets everything to a blank/false status -- IK this needs some war stuff to actually happen, but since I don't have information on war yet, I can't do that.
        self.uP = ""
        self.unionStatus = "False"

    def tileList(self):
        tileNames = [tile["name"] for tile in self.tiles]  
        return(f"{self.name} has the following tiles: " + ", ".join(tileNames) +".")

    def resourceList(self):
        resourceNames = [resource["name"] for resource in self.resources]
        numeratedResources = []
        for i in resourceNames:
            resourceNum = resourceNames.count(i)
            if resourceNum == 0:
                continue
            resourceName = str(resourceNum) + "x " + i
            numeratedResources.append(resourceName)
            resourceNames = list(filter((i).__ne__,resourceNames))
        return(f"{self.name} has the following resources: " + ", ".join(numeratedResources) +".")



nationFile = "storedNations.pkl" # this is the local pickle file that stores the information when the code is shut down.
# On startup, read from pickle file of previously created nations and create nations for them.

# storage dictionary pulled from pickle file of all nations & info 
with open(nationFile, "rb") as tf:
    stored = pickle.load(tf) # labels stored as the dictionary with all the information.
    tf.close()

print(stored) # prints stored -- honestly as more or less a check for me to see that everything looks fine. This can be removed later.

# to prevent nations from messing *everything* up -- this is just here for whenever I add a new attribute to the nation class, because then some nations might have the new thing, and others won't. nations then freaks out when it has something different.
# for key in stored:  
#     stored[key]["tps"] = []
#     stored[key]["allies"] = [] 
#     stored[key]["un"] = ""
#     stored[key]["uP"] = ""
    # stored[key]["tiles"] = []

# stored layout ==      stored = {"name" : {"owner":"x", "allies":["x","y"], "tps":["x","y"], "un":"Senior", "uP":"x", ...}, "name2" : and so on}

nations = {key: Nation(key, stored[key]["owner"], stored[key]["allies"], stored[key]["tps"], stored[key]["un"], stored[key]["uP"], stored[key]["tiles"]) for key in stored} # creates nation class for each nation from the information provided in stored.
# as it was described to me after I did it and it looked confusing, stored is the layout that the pickle file needs to not lose information, and nations is the layout I need/like to make use of the class so that I can do stuff.
# in an ideal world, stored would only be opened once, and saved/closed once, but given how I'm shutting the code without it being able to do finally code, I need to have it save after each update to it. This can probably be changed at a later point, but it works currently.

# This is a testing area that I've been using for Nation work that I've found problematic.
# idk = Nation("idk", "wat", [], [], "", "", [tileMountain, tileForest, tileForest])
# nations["test"].tileList()
# nations["test"].resourceList()

testServer = discord.Object(id=1010602651060277279) # this is our bot testing server -- I can probably change this to the main Conwylia server when we get to that point.
class aclient(discord.Client): # this entire class sets up the commands to work more or less, I don't want to mess with it because I don't fully understand what it's doing because the discord.py documentation hurts my head to deal with.
    def __init__(self):
        super().__init__(intents = discord.Intents.default()) 
        self.synced = False # you have to sync the commands to the server so it sets sync to false at start up

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: # when the bot is ready for use, it syncs up to the server's command list
            await tree.sync(guild = discord.Object(id=1010602651060277279))
            self.synced = True
        print(f'We have logged in as {self.user}') # this tells the person running the code that all is good, and the bot is ready for use.

client = aclient() # calling the code to create the client
tree = app_commands.CommandTree(client) # setting up the command tree through discord.


# The following is all commands for the discord bot.

# modal ui and creation of nation on submit
class CreateNation(ui.Modal, title="Nation Information"):
    name = ui.TextInput(label="Name")
    owner = ui.TextInput(label="Owner")
    tiles = ui.TextInput(label="List of Tiles")
    

    async def on_submit(self, interaction: discord.Interaction):
        try:
            strTileList = self.tiles.value.split()
            tileList = []
            for i in strTileList:
                tileList.append(tileNametoClass[i])
        except:
            await interaction.response.send_message(f"The layout of the tile list was incorrect.", ephemeral=True)
        nations[self.name.value] = Nation(self.name.value, self.owner.value)     # nation created 
        stored[nations[self.name.value].name] = {"owner" : self.owner.value, "allies":[],"tps":[],"un":"","uP":"","tiles":tileList}     # nation added to storage dictionary
        with open(nationFile, "wb") as tf:    # storing all the nations and info
            pickle.dump(stored,tf)
            tf.close() 
        await interaction.response.send_message(f"The nation {self.name.value} has been added to the database.") # response to user 


    async def on_timeout(self, interaction) -> None:
        await interaction.response.send_message(f"Nation creation timed out.", ephemeral=True) 

# creating a nation in class nation
@tree.command(name = "createnation", description="Creates a nation in the database.", guild = testServer)
async def createNation(interaction: discord.Interaction):
    newNation = CreateNation()
    await interaction.response.send_modal(newNation)
 




# shows all the commands accessible
@tree.command(name = "help", description="Lists all the commands possible with Conwylia Bot.", guild = discord.Object(id=1010602651060277279))
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("""
The following commands are active: 
```
/createnation                                                       -- Creates a nation in the database. 
/help                                                               -- Lists all the commands possible with this bot.
/nation (Name of Nation)                                            -- Looks up info on a particular nation in the database. 
/nations                                                            -- Lists all the nations in the database. 
/deletenation (Name of Nation)                                      -- Deletes a nation from the database.
/ally (Name of Nation) (Name of Allied Nation)                      -- Allies with another nation in the database.
/allies (Name of Nation)                                            -- Lists all the allies of a nation in the database.
/removeally (Name of Nation) (Name of Allied Nation)                -- Removes an alliance between two nations in the database.
/setowner (Name of Nation) (New Owner Name)                         -- Changes the owner of a nation in the database.
/partner (Name of Nation) (Name of Trade Partner)                   -- Makes two nations trade partners in the database.
/partners (Name of Nation)                                          -- Lists all the trade partners of a nation in the database.
/removepartner (Name of Nation) (Name of Trade Partner)             -- Removes a trade partnership between two nations in the database.
/union (Name of Nation)                                             -- Says whether a nation is in a union and with whom in the database.
/unionize (Name of Nation) (Name of Union Nation) (Seniority)       -- Enters into a union with another nation in the database.
/deunionize (Name of Nation) (Name of Union Nation)                 -- Breaks a union with another nation in the database.
```
""") # all possible commands. Honestly I think I read that there was a better way to do this, but I can't find it, so I have to update it manually, therefore I forget about it until I'm reminded.
 


# all the information about a nation
@tree.command(name = "nation", description = "Shows information about a nation.", guild = testServer)
async def nationInfo(interaction: discord.Interaction, nation_name: str): 
    try:    # the bot trys to show the basic information -- this probably either needs an update or removal as it's quite outdated. If I can make a dropdown of options after name of nation that allows me to select a particular feature of the nation and call that, I would go for that.
        await interaction.response.send_message(f"The nation {nations[nation_name].name} is owned by {nations[nation_name].owner}.") 
    except KeyError: # this gets thrown when the bot can't find the nation in nations.
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True) # whenever the bot sends a message ephemerally, it sends it as a hidden message, so it only gets sent to the user who sent the command. This allows for you to easily remedy the mistake and doesn't call attention to the mistake.
# I'm trying to make all error messages happen this way, in assumption that the user didn't mean to mess up, so it makes it easier to fix it quietly. It might be reasonable to supply the user with the exact information they gave the bot, but eh
# Looking forward, whenever I talk about a quiet response or something, this is what I mean. It responds personally to the user only.
@nationInfo.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



# lists all the nations in the database
@tree.command(name="nations", description="Lists all the nations in the database.", guild=testServer)
async def nationsList(interaction: discord.Interaction):
    await interaction.response.send_message("The nations currently in the database are: " + ", ".join(stored.keys()) +".") # this grabs all of the nations names which are in stored as the keys and joins them together with a comma. Better than the multi-line for loop I used to have do it...



# deletes a nation from the database
@tree.command(name="deletenation", description="Deletes a nation from the database.", guild=testServer)
async def dnation(interaction: discord.Interaction, nation_name: str):
    try: # this tries to delete the nation 
        del nations[nation_name]
        del stored[nation_name]
        # saving the new list of nations without the deleted nation
        with open(nationFile, "wb") as tf:
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"The nation {nation_name} has been deleted from the database.") # response
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True) # if the bot can't find said nation, it responses quietly

@dnation.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



# lists the allies of a nation in the database
@tree.command(name="allies", description="Lists the allies of a nation in the database.", guild=testServer)
async def allies(interaction: discord.Interaction, nation_name: str):
    try: # the bot tries to call getAllies
        await interaction.response.send_message(nations[nation_name].getAllies())
    except KeyError: # if the nation can't be found, it response quietly.
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)

@allies.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



# allies two nations both which are within the database
@tree.command(name="ally", description="Allies two nations that are within the database.", guild=testServer)
async def nally(interaction: discord.Interaction, nation_name: str, allied_nation_name: str): # nation name = "asking nation", whichever nation is initiating the alliance (ik its mutual but eh),   allied nation name = "to be allied nation", the other nation :)
    if len(nations[nation_name].allies) == 2: # maximum number of allies is 2, so if the asking nation attempting to ally with the to be allied nation already has 2 allies, the bot realises and says no. Unsure whether this should be a "quiet" response or not.
        await interaction.response.send_message(f"{nations[nation_name].name} cannot ally with any more nations.")
        return
    if allied_nation_name in nations: # checks to see if the to be allied nation is actually a known nation
        if len(nations[allied_nation_name].allies) == 2: # if it is, gotta check to make sure that it can ally with the asking nation.
            await interaction.response.send_message(f"{nations[allied_nation_name].name} cannot ally with any more nations.") # again, not quiet response, but probably could be argued that it should be.
            return
        nations[nation_name].ally(allied_nation_name) # successfully allies in BOTH nation instances.
        nations[allied_nation_name].ally(nation_name)
        stored[nations[nation_name].name]["allies"] = nations[nation_name].allies
        stored[nations[allied_nation_name].name]["allies"] = nations[allied_nation_name].allies
        with open(nationFile, "wb") as tf: # storing the new allies information
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is now allied with {nations[allied_nation_name].name}.") # response
    else:
        await interaction.response.send_message(f"The nation {allied_nation_name} doesn't exist in the database.") # ultimately if the to be allied nation was not in nations, runs this. Although, I think I'm missing a check to see if the asking nation is in nations. This might be the response to that too.

@nally.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@nally.autocomplete("allied_nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=allied_nation_name, value=allied_nation_name) for allied_nation_name in stored.keys() if current.lower() in allied_nation_name.lower()]



# removes an alliance between two nations within the database
@tree.command(name="removeally", description="Removes an alliance between two nations within the database.", guild=testServer)
async def rally(interaction: discord.Interaction, nation_name: str, allied_nation_name: str):
    if allied_nation_name in nations: # this is basically the same crap as the ally command, so comments are gonna be sparse.
        if nations[allied_nation_name].name not in nations[nation_name].allies: # gotta make sure they are actually allied
            await interaction.response.send_message(f"{nations[nation_name].name} is not allied with {nations[allied_nation_name].name}.")
            return
        nations[nation_name].removeAlly(allied_nation_name)
        nations[allied_nation_name].removeAlly(nation_name)
        stored[nations[nation_name].name]["allies"] = nations[nation_name].allies
        stored[nations[allied_nation_name].name]["allies"] = nations[allied_nation_name].allies
        with open(nationFile, "wb") as tf: # storing new info
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is no longer allied with {allied_nation_name}.") # response
    else:
        await interaction.response.send_message(f"The nation {allied_nation_name} doesn't exist in the database.")

@rally.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@rally.autocomplete("allied_nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=allied_nation_name, value=allied_nation_name) for allied_nation_name in stored.keys() if current.lower() in allied_nation_name.lower()]



# changes a nation's owner
@tree.command(name="setowner", description="Changes a nation's owner", guild=testServer) # this command is more or less just to fix stuff when I accidentally remove an owner through a mess up. IDK how it would be useful in reality.
async def nown(interaction:discord.Interaction, nation_name: str, new_owner: str):
    nations[nation_name].setOwner(new_owner)
    stored[nations[nation_name].name]["owner"] = nations[nation_name].owner
    with open(nationFile, "wb") as tf: # storing new info
        pickle.dump(stored,tf)
        tf.close()
    await interaction.response.send_message(f"{nations[nation_name].owner} is the new owner of {nations[nation_name].name}.") # of course if the nation doesn't actually exist it's just going to run an error and not respond, so... I'll add that type of check in mass later.

@nown.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



@tree.command(name="partner", description="Partners two nations in the database as trade partners.", guild=testServer) # so this whole trade partner section of code is almost identical to the ally code section. I used it as a base to create this code, so sparse comments :)
async def npart(interaction:discord.Interaction, nation_name: str, trade_partner_nation: str):
    if len(nations[nation_name].tradePart) == 3: # max is 3
        await interaction.response.send_message(f"{nations[nation_name].name} cannot become trade partners with any more nations.")
        return
    if trade_partner_nation in nations:
        if len(nations[trade_partner_nation].tradePart) == 3: # max
            await interaction.response.send_message(f"{nations[trade_partner_nation].name} cannot become trade partners with any more nations.")
            return
        nations[nation_name].ally(trade_partner_nation)
        nations[trade_partner_nation].ally(nation_name)
        stored[nations[nation_name].name]["tps"] = nations[nation_name].tradePart
        stored[nations[trade_partner_nation].name]["tps"] = nations[trade_partner_nation].tradePart
        with open(nationFile, "wb") as tf: # storing new data
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is now trade partners with {nations[trade_partner_nation].name}.") # response
    else:
        await interaction.response.send_message(f"The nation {trade_partner_nation} doesn't exist in the database.") 

@npart.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@npart.autocomplete("trade_partner_nation")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=trade_partner_nation, value=trade_partner_nation) for trade_partner_nation in stored.keys() if current.lower() in trade_partner_nation.lower()]



@tree.command(name="partners", description="Lists the trade partners of a nation in the database.", guild=testServer) 
async def parts(interaction:discord.Interaction, nation_name: str):
    try:
        await interaction.response.send_message(nations[nation_name].getTradePartners()) # returns trade partner info
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)

@parts.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



@tree.command(name="removepartner", description="Removes a trade partnership between two nations in the database.", guild=testServer)
async def rpart(interaction:discord.Interaction, nation_name: str, trade_partner_nation: str):
    if trade_partner_nation in nations: 
        if nations[trade_partner_nation].name not in nations[nation_name].tradePart: # gotta make sure that they are trade partners
            await interaction.response.send_message(f"{nations[nation_name].name} is not trade partners with {nations[trade_partner_nation].name}.")
            return
        nations[nation_name].removeTradePartner(trade_partner_nation)
        nations[trade_partner_nation].removeTradePartner(nation_name)
        stored[nations[nation_name].name]["tps"] = nations[nation_name].tradePart
        stored[nations[trade_partner_nation].name]["tps"] = nations[trade_partner_nation].tradePart
        with open(nationFile, "wb") as tf: # storing new data
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is no longer trade partners with {trade_partner_nation}.") # response
    else:
        await interaction.response.send_message(f"The nation {trade_partner_nation} doesn't exist in the database.")

@rpart.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@rpart.autocomplete("trade_partner_nation")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=trade_partner_nation, value=trade_partner_nation) for trade_partner_nation in stored.keys() if current.lower() in trade_partner_nation.lower()]



@tree.command(name="union", description="Shows whether a nation is in a union or not.", guild=testServer)
async def union(interaction:discord.Interaction, nation_name: str):
    try:
        await interaction.response.send_message(nations[nation_name].unions()) # returns trade partner info
    except KeyError:
        await interaction.response.send_message("That nation doesn't exist in the database.", ephemeral=True)

@union.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]



@tree.command(name="unionize", description="Allows a nation to unionize with another nation.", guild=testServer)
async def unionize(interaction:discord.Interaction, nation_name: str, union_nation: str, seniority: bool):
    if nations[nation_name].uP != "": # if asking nation has a union already
        await interaction.response.send_message(f"{nations[nation_name].name} cannot be in a union with any more nations.")
        return
    if union_nation in nations:
        if nations[union_nation].uP != "": # if unioned nation has one already  -- HONESTLY this might not be an issue, it would just lead to some complicated stuff. So like if unioned nation is a junior nation, means war between the two seniors. If unioned nation is senior, what happens to junior nation?
            await interaction.response.send_message(f"{nations[union_nation].name} cannot be in a union with any more nations.")
            return
        if seniority: # all allies and trade partners stick with the senior nation.
            nations[nation_name].unionize(union_nation, True)
            nations[union_nation].unionize(nation_name, False)

            nations[union_nation].tradePart = nations[nation_name].tradePart
            nations[union_nation].allies = nations[nation_name].allies
            stored[nations[union_nation].name]["tps"] = nations[union_nation].tradePart
            stored[nations[union_nation].name]["allies"] = nations[union_nation].allies

        else:
            nations[nation_name].unionize(union_nation, False)
            nations[union_nation].unionize(nation_name, True)

            nations[nation_name].tradePart = nations[union_nation].tradePart
            nations[nation_name].allies = nations[union_nation].allies
            stored[nations[nation_name].name]["tps"] = nations[nation_name].tradePart
            stored[nations[nation_name].name]["allies"] = nations[nation_name].allies


        stored[nations[nation_name].name]["un"] = nations[nation_name].unionStatus
        stored[nations[union_nation].name]["un"] = nations[union_nation].unionStatus
        stored[nations[nation_name].name]["uP"] = nations[nation_name].uP
        stored[nations[union_nation].name]["uP"] = nations[union_nation].uP

        
        with open(nationFile, "wb") as tf: # storing new data
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is now in a union with {nations[union_nation].name}.") # response
    else:
        await interaction.response.send_message(f"The nation {union_nation} doesn't exist in the database.") 

@unionize.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@unionize.autocomplete("union_nation")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=union_nation, value=union_nation) for union_nation in stored.keys() if current.lower() in union_nation.lower()]



@tree.command(name="deunionize", description="Allows a nation to deunionize with another nation.", guild=testServer) # I acknowledge that this requires war on the part of the junior partner. I've coded it so that it can be translated easily to that system, but since war isn't up yet, it's not set up.
async def deunion(interaction:discord.Interaction, nation_name: str, union_nation: str):
    if nations[nation_name].uP == "": # if asking nation has a union already
        await interaction.response.send_message(f"{nations[nation_name].name} is not in a union.")
        return
    if union_nation in nations:
        if nations[union_nation].uP == "": # 
            await interaction.response.send_message(f"{nations[union_nation].name} is not in a union.")
            return
        if nations[nation_name].unionStatus == "Senior": # all allies and trade partners stick with the senior nation, while the junior loses all allies and trade partners.
                                                         # If the main nation is the senior nation, the other goes blank.
            nations[nation_name].deUnionize()
            nations[union_nation].deUnionize()

            nations[union_nation].tradePart = []
            nations[union_nation].allies = []
            stored[nations[union_nation].name]["tps"] = nations[union_nation].tradePart
            stored[nations[union_nation].name]["allies"] = nations[union_nation].allies

        else: # or the unioned nation is senior, and the main nation goes blank instead. 
              # It's here that there would be war stuff.

            nations[nation_name].deUnionize()
            nations[union_nation].deUnionize()

            nations[nation_name].tradePart = []
            nations[nation_name].allies = []
            stored[nations[nation_name].name]["tps"] = nations[nation_name].tradePart
            stored[nations[nation_name].name]["allies"] = nations[nation_name].allies


        stored[nations[nation_name].name]["un"] = nations[nation_name].unionStatus
        stored[nations[union_nation].name]["un"] = nations[union_nation].unionStatus
        stored[nations[nation_name].name]["uP"] = nations[nation_name].uP
        stored[nations[union_nation].name]["uP"] = nations[union_nation].uP

        
        with open(nationFile, "wb") as tf: # storing new data
            pickle.dump(stored,tf)
            tf.close()
        await interaction.response.send_message(f"{nations[nation_name].name} is no longer in a union with {nations[union_nation].name}.") # response
    else:
        await interaction.response.send_message(f"The nation {union_nation} doesn't exist in the database.") 

@deunion.autocomplete("nation_name")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]
@deunion.autocomplete("union_nation")
async def autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=union_nation, value=union_nation) for union_nation in stored.keys() if current.lower() in union_nation.lower()]


@tree.command(name="population", description="Shows a nation's population.", guild=testServer)
async def population(interaction:discord.Interaction, nation_name: str):
    await interaction.response.send_message(f"%s has a population of %dk." % (nation_name, nations[nation_name].pop))

@population.autocomplete("nation_name")
async def autocomplete(interaction:discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in stored.keys() if current.lower() in nation_name.lower()]


@tree.command(name="tiles", description="Shows all the tiles of a nation.", guild=testServer)
async def self(interaction:discord.Interaction):
    return

# @tree.command(name="blank", description="blank", guild=testServer)
# async def self(interaction:discord.Interaction):
#     return



try:
    client.run('id') # this is the discord bot id. Ideally, I don't commit the actual id to github because then anyone can run any code on the bot. I'd have to reset the id then. 
finally:
    print("Shutting down....") # eventually I'll move stored saving to here to make it simpler, but for now, it's safer for me not to.