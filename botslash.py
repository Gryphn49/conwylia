import discord
import pickle
from discord import app_commands
from typing import List
from discord import ui














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
        self.name = name # name of nation
        self.owner = owner # name of owner (of nation)
        self.allies = allies # list of allies
        self.tradePart = tps # list  of trade partners
        self.unionStatus = union # is union -- Options: blank (not set), False, Senior, Junior
        self.uP = uP # union partner

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


nationFile = "storedNations.pkl" # this is the local pickle file that stores the information when the code is shut down.
# On startup, read from pickle file of previously created nations and create nations for them.

# storage dictionary pulled from pickle file of all nations & info 
with open(nationFile, "rb") as tf:
    stored = pickle.load(tf) # labels stored as the dictionary with all the information.
    tf.close()

print(stored) # prints stored -- honestly as more or less a check for me to see that everything looks fine. This can be removed later.

# to prevent nations from messing *everything* up -- this is just here for whenever I add a new attribute to the nation class, because then some nations might have the new thing, and others won't. nations then freaks out when it has something different.
for key in stored:  
    stored[key]["tps"] = []
    stored[key]["allies"] = [] 
    stored[key]["un"] = ""
    stored[key]["uP"] = ""





# stored layout ==      stored = {"name" : {"owner":"x", "allies":["x","y"], "tps":["x","y"], "un":"Senior", "uP":"x", ...}, "name2" : and so on}

nations = {key: Nation(key, stored[key]["owner"], stored[key]["allies"], stored[key]["tps"], stored[key]["un"], stored[key]["uP"]) for key in stored} # creates nation class for each nation from the information provided in stored.
# as it was described to me after I did it and it looked confusing, stored is the layout that the pickle file needs to not lose information, and nations is the layout I need/like to make use of the class so that I can do stuff.
# in an ideal world, stored would only be opened once, and saved/closed once, but given how I'm shutting the code without it being able to do finally code, I need to have it save after each update to it. This can probably be changed at a later point, but it works currently.





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






# modal ui and creation of nation on submit
class CreateNation(ui.Modal, title="Nation Information"):
    name = ui.TextInput(label="Name")
    owner = ui.TextInput(label="Owner")

    async def on_submit(self, interaction: discord.Interaction):
        nations[self.name.value] = Nation(self.name.value, self.owner.value)     # nation created 
        stored[nations[self.name.value].name] = {"owner" : self.owner.value, "allies":[],"tps":[],"un":"","uP":""}     # nation added to storage dictionary
        with open(nationFile, "wb") as tf:    # storing all the nations and info
            pickle.dump(stored,tf)
            tf.close() 
        
        await interaction.response.send_message(f"The nation {self.name.value} has been added to the database.") # response to user 


# creating a nation in class nation
@tree.command(name = "createnation", description="Creates a nation in the database.", guild = testServer)
async def self(interaction: discord.Interaction):
    newNation = CreateNation()
    await interaction.response.send_modal(newNation)
 




# shows all the commands accessible
@tree.command(name = "help", description="Lists all the commands possible with Conwylia Bot.", guild = discord.Object(id=1010602651060277279))
async def self(interaction: discord.Interaction):
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
            nations[nation_name].unionize(union_nation, "Senior")
            nations[union_nation].unionize(nation_name, "Junior")

            nations[union_nation].tradePart = nations[nation_name].tradePart
            nations[union_nation].allies = nations[nation_name].allies
            stored[nations[union_nation].name]["tps"] = nations[union_nation].tradePart
            stored[nations[union_nation].name]["allies"] = nations[union_nation].allies

        else:
            nations[nation_name].unionize(union_nation, "Junior")
            nations[union_nation].unionize(nation_name, "Senior")

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





# @testing.autocomplete("nation_name")
# async def testing_autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
#     nationNames = stored.keys()
#     return [app_commands.Choice(name=nation_name, value=nation_name) for nation_name in nationNames if current.lower() in nation_name.lower()]


@tree.command(name="deunionize", description="Allows a nation to deunionize with another nation.", guild=testServer) # I acknowledge that this requires war on the part of the junior partner. I've coded it so that it can be translated easily to that system, but since war isn't up yet, it's not set up.
async def self(interaction:discord.Interaction):
    return

# @tree.command(name="blank", description="blank", guild=testServer)
# async def self(interaction:discord.Interaction):
#     return



try:
    client.run('id') # this is the discord bot id. Ideally, I don't commit the actual id to github because then anyone can run any code on the bot. I'd have to reset the id then. 
finally:
    print("Shutting down....") # eventually I'll move stored saving to here to make it simpler, but for now, it's safer for me not to.