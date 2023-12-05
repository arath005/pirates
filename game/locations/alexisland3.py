from game import location
#there is some pretense that the game might not be played over the term
#so we use a custom function announce to ptint things instead of print
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
from game.player import Player
from game.combat import *
from game.events import guardian
from game.events import Boss3

class Alex(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        #super refers to the parent class
        #(Location in this case)
        #this runs the initializer of Location
        self.name = "island"
        self.symbol = 'I' #Symbol for map
        self.visitable = True #Marks the island as a place the pirates can visit
        self.locations = {} #Dictionary of sub-locations on the island
        self.locations["ruins"] = Ruins(self)
        self.locations["puzzle"] = Puzzle(self)
        self.locations["puzzle2"] = Puzzle2(self)
        self.locations["doorway"] = doorway(self)
        self.locations["boss"] = boss(self)

        #Where the pirates start. v
        self.starting_location = self.locations["ruins"]

    def enter(self, ship):
        #what pirates do when ship visits this loc on the map
        announce("You see some ruins on an island in the shape of a skull")
        

    #Boilerplate code for starting a visit.
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        

#Sub-locations (Beach and Trees)
class Ruins(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "ruins"
        #the verbs dict was set up by th super() init
        #'go north' has handling that causes sublocations to just get the direction.
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.event_chance = 10
        self.events.append(guardian.Guardian_attack())
    
    def caesar_cipher(text, shift):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
        
                is_upper = char.isupper()

        
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))

                encrypted_text += shifted_char
            else:
        
                encrypted_text += char
        
            return encrypted_text




    def enter(self):
        announce ("You arrived at a set of ruins on an island that look like they are in the shape of a sckull. You anchor at the south bay")

    #one of the core functions
    #handles alot of shit
    #more complex actions should have dedications functions to handle them
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["doorway"]
        if (verb=="east"):
            config.the_player.next_loc = self.main_location.locations["puzzle2"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["puzzle"]
        if(verb == "inspect"):
            announce("You see strange writing on the side of a piller as well as some english below it")
            res = input ("What would you like to inspect further\n:")
            if res == "writing":
                announce("You look at the wall and read the following.\n'zhofrph wr wkh grpdlq ri wkh jrgv'\n'welcome to the domain of the gods'")
            else:
                announce("That doesnt seem to be here")

class Puzzle(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "puzzle"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        

        #add some treasure!
        self.verbs["take"] = self
        self.item_in_computer = Key5()
        self.item_in_grave = Demonsword()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk into a graveyard")
    
    def caesar_cipher(self, text, shift):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
        
                is_upper = char.isupper()

        
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))

                encrypted_text += shifted_char
            else:
        
                encrypted_text += char
        
        return encrypted_text

    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["east"]):
            config.the_player.next_loc = self.main_location.locations["ruins"]

        if(verb in ["north", "south", "west"]):
            announce("You run into a wall. You feel pretty stupid")

        if(verb == "inspect"):
            announce("you see a graveyard that seems to go on forever with tombstones as well as a sign and a keyboard under it")
            res = input ("What would you like to inspect further\n:")
            if res == "graves" or res == "Tombstones" or res == "tombstones" or res == "Graves":
                announce('you see hundreds of graves each with a different tombstone some more complex then others')
                ress = input('Which grave would you like to visit\n')
                if ress == "Persephone" or ress == "persephone":
                    if self.item_in_grave == None:
                        announce('there is nothing here')
                    else:
                        announce('you find a black and red sword stuck into this grave')
                        resss = input('Would you like to take it\n')
                        if resss == 'yes':
                            e = self.item_in_grave
                            announce("You take the "+e.name + " from the grave.")
                            config.the_player.add_to_inventory(Demonsword().as_list())
                            self.item_in_grave = None
                            config.the_player.go = True
                        else:
                            e = self.item_in_grave
                            announce("The "+ e.name + " flies out of the grave and into you bag")
                            config.the_player.add_to_inventory(Demonsword().as_list())
                            self.item_in_grave = None
                            config.the_player.go = True
                else:
                    announce('You visit their grave and pay your respects')
                
            elif res == "sign":
                encrypted_message = self.caesar_cipher("What realm do I rule over", 3)
                announce("You look at the sign and read the following.\n"+ encrypted_message)
            elif res == "keyboard":
                ans = input("Please answer the text\n:")
                if ans == "Underworld" or ans == "underworld":
                    announce("correct\nkrrr krrr")
                    if self.item_in_computer == None:
                        announce('you already took it')
                    else:
                        i = self.item_in_computer
                        announce("You take the "+i.name + " from the computer.")
                        #config.the_player.add_to_inventory(i)
                        config.the_player.add_to_inventory(Key5().as_list())

                        self.item_in_computer = None
                        config.the_player.go = True
            else:
                announce("That doesnt seem to be here")
    
        
        if(verb == "take"):
            # the player will type something like "take saber" or "take all"
            if(self.item_in_tree == None and self.item_in_clothes == None):
                announce("you don't see anything to take.")
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


class Puzzle2(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "puzzle2"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.verbs["back"] = self
        

        #add some treasure!
        self.verbs["take"] = self
        self.item_in_computer = Key6()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk across a bridge")

        

    def caesar_cipher(self, text, shift):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
        
                is_upper = char.isupper()

        
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))

                encrypted_text += shifted_char
            else:
        
                encrypted_text += char
        
        return encrypted_text
    
    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["west"]):
            config.the_player.next_loc = self.main_location.locations["ruins"]

        if(verb in ["north", "south", "east"]):
            announce("You try to move but the huge dog growls so you stay still")

        if(verb == "inspect"):
            announce("You find a three headed dog guarding a door")
            res = input ("what would you like to inspect further\n")
            if res == "dog" or res == "Dog":
                announce("You try to communicate with the dog and it asks you a question")
                ress = input('What is my name\n')
                if ress == "Cerberus" or ress == "cerberus":
                    if self.item_in_computer == None:
                        announce('you already took it')
                    else:
                        i = self.item_in_computer
                        announce("Cerberus gives you "+ i.name)
                        config.the_player.add_to_inventory(Key6().as_list())
                        self.item_in_computer = None
                        config.the_player.go = True
                else:
                    announce("wrong")
            else:
                announce("That doesnt seem to be here")
    
    
        
                



class Hinges(items.Item):
    def __init__(self):
        super().__init__("Hindges", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]
    
class Key5(items.Item):
    def __init__(self):
        super().__init__("Key5", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]

class Key6(items.Item):
    def __init__(self):
        super().__init__("Key6", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]

class Demonsword(items.Item):
    def __init__(self):
        super().__init__("Demonsword", 99999)
        self.damage = (99,101)
        self.firearm = False
        self.skill = "magic"
        self.verb = "slash"
        self.verb2 = "slashes"

    def as_list(self):
        return [self]


class doorway(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "doorway"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        

        #add some treasure!
        self.verbs["take"] = self
        self.event_chance = 50
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk into a huge building")
        

    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["south"]):
            config.the_player.next_loc = self.main_location.locations["ruins"]

        if(verb in ["west", "east"]):
            announce("You hit a wall.")

        if(verb == "inspect"):
            announce("You see a huge door, columns and tiles adorning the floor")
            res = input ("what would you like to inspect further\n")
            if res == "door":
                announce("you walk up to the door and see 2 key holes.")
                has_key1 = any(isinstance(item, Key5) for item in config.the_player.inventory)
                has_key2 = any(isinstance(item, Key6) for item in config.the_player.inventory)
                
                if has_key1 and has_key2:


                    aa = input('would you like to insert your keys?\n')
                    if aa == 'yes':
                        announce("The door has opened")
                        aaa = input('would you like to enter?\n')
                        if aaa == 'yes':
                            config.the_player.go = True
                            config.the_player.next_loc = self.main_location.locations["boss"]
                            
                    else:
                        announce('You feel a greater power laughing at your lack of courage')
                else:
                    announce('You hear a voice saying you are not ready yet')
            elif res == "columns":
                announce("You walk around every single column in there and find nothing")
                
            elif res == "tiles":
                announce("The tiles are too heavy to be lifted")
            else:
                announce("That doesnt seem to be here")



class boss(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "boss"
        #the verbs dict was set up by th super() init
        #'go north' has handling that causes sublocations to just get the direction.
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.event_chance = 100
        self.events.append(Boss3.Boss_fight3())
        self.item_in_boss = Hinges()
    
    def enter(self):
        announce ("You see a huge boss running at you")

    #one of the core functions
    #handles alot of shit
    #more complex actions should have dedications functions to handle them
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return through the doorway")
            config.the_player.next_loc = self.main_location.locations["doorway"]
        if (verb == "north"):
            announce('You run into a wall')
        if (verb=="east"):
            announce('You run into a wall')
        if (verb == "west"):
            announce('You run into a wall')
        if(verb == "inspect"):
            announce("You see a giant boss carcass.")
            res = input ("What would you like to inspect further\n")
            if res == "boss":
                if self.item_in_boss == None:
                    announce('you already took it')
                else:
                    announce("You walk up to the boss and rummage through his body only to find some hindges to a box")
                    aa = input('would you like to take it\n')
                    if aa == 'yes':
                        announce('You take the hindges from the boss carcass')
                        config.the_player.add_to_inventory(Hinges().as_list())
                        self.item_in_boss = None
                        config.the_player.go = True
                    else:
                        announce('You try to walk away but the hindges forcibly enters your bag')
                        config.the_player.add_to_inventory(Hinges().as_list())
                        self.item_in_boss = None
                        config.the_player.go = True
            else:
                announce("That doesnt seem to be here")



