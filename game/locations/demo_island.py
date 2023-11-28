from game import location
#there is some pretense that the game might not be played over the term
#so we use a custom function announce to ptint things instead of print
from game.display import announce
import game.config as config
import game.items as items
from game.events import *


#Demo island inherits from location (Demo island is a location)
class DemoIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        #super refers to the parent class
        #(Location in this case)
        #this runs the initializer of Location
        self.name = "island"
        self.symbol = 'I' #Symbol for map
        self.visitable = True #Marks the island as a place the pirates can visit
        self.locations = {} #Dictionary of sub-locations on the island
        self.locations["beach"] = Beach(self)
        self.locations["trees"] = Trees(self)
        #Where the pirates start. v
        self.starting_location = self.location["beach"]

    def enter(self, ship):
        #what pirates do when ship visits this loc on the map
        announce("arrived at an island")

    #Boilerplate code for starting a visit.
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.locaton.enter()
        super().visit()
        

#Sub-locations (Beach and Trees)
class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        #the verbs dict was set up by th super() init
        #'go north' has handling that causes sublocations to just get the direction.
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())


    def enter(self):
        announce ("You arrive at the beach. Your sjip anchors at the south bay")

    #one of the core functions
    #handles alot of shit
    #more complex actions should have dedications functions to handle them
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]

        if (verb=="east" or verb == "west"):
            announce("you walk all the way arround the island on the beach. It's not very dangerous.")


        
class Trees(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "trees"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self

        #add some treasure!
        self.verbs["take"] = self
        self.item_in_tree = Saber()
        self.item_in_clothes = items.Flintlock()
        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.event.appemd(drowned_pirates.DrownedPirates())


    def enter (self):
        announce("You walk into the small forest on the island.")
        if self.item_in_tree != None:
            description = description + "You see a " + self.item_in_tree.name + " stuck in a tree"
        if self.item_in_clothes != None:
            description = description + "You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor"
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["north", "south", "east", "weast"]):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if(verb == "take"):
            # the player will type something like "take saber" or "take all"
            if(self.item_in_tree == None and self.item_in_clothes == None):
                announce("you don't see anything to tske.")
            #they just typed "take"
            elif(len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                i = self.item_in_tree
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the "+i.name + " from the tree.")
                    config.the_player.add_to_inventory(i)
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_in_clothes
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the "+i.name + " out of a pile of shredded clothes")
                    config.the_player.add_to_inventory(i)
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
            if not at_least_one:
                announce("You don't see one of those around")
                



class Saber(items.Item):
    def __init__(self):
        super().__init__("saber", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"
