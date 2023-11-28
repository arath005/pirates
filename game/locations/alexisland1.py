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
from game.events import Boss

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
        announce("You see some ruins on an island")

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
        # self.event.appemd(drowned_pirates.DrownedPirates())
        #^can take out later justbkeeping for reference
    
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
        announce ("You arrived at a set of ruins on an island. You anchor at the south bay")

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
        self.item_in_computer = Key1()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk into a small building")
    
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
            announce("You see strange writing on the wall as well as a keyboard to the left of it")
            res = input ("What would you like to inspect further\n:")
            if res == "writing":
                encrypted_message = self.caesar_cipher("what killed the cat", 3)
                announce("You look at the wall and read the following.\n"+ encrypted_message)
            elif res == "keyboard":
                ans = input("Please answer the text\n:")
                if ans == "curiosity" or ans == "Curiosity":
                    announce("correct\nkrrr krrr")
                    i = self.item_in_computer
                    announce("You take the "+i.name + " from the computer.")
                    #config.the_player.add_to_inventory(i)
                    config.the_player.add_to_inventory(Key1().as_list())

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
        self.item_in_computer = Key2()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk through a huge tunnle coming out the other side")
        

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
            announce("You walk for hours upon hours but cant seem to get more then 30 feet away from where you started")

        if(verb == "inspect"):
            announce("you see a strange pillar in the middle of an open field with some strang writing on it")
            res = input ("what would you like to inspect further\n")
            if res == "writing":
                encrypted_message = self.caesar_cipher("curiosity is the downfall of mankind", 3)
                announce("you gaze upon the pillar and see strange writings.\n" + encrypted_message)
            elif res == "pillar":
                announce("You walk around the back of the pillar only to find a keyboard")
                ress = input('would you like to inspect the keyboard\n:')
                if ress == 'yes':
                    ans = input("true or false?\n beware the consequences if you choose incorrectly\n:")
                    if ans == "True" or ans == 'true':
                        announce("correct\nkrrr krrr")
                        i = self.item_in_computer
                        announce("You take the "+ "Key2" + " from the computer.")
                        #config.the_player.add_to_inventory(i)
                        config.the_player.add_to_inventory(Key2().as_list())

                        self.item_in_computer = None
                        config.the_player.go = True
                
            else:
                announce("That doesnt seem to be here")
    
    
        
                



class Box_lid(items.Item):
    def __init__(self):
        super().__init__("Box_lid", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]
    
class Key1(items.Item):
    def __init__(self):
        super().__init__("Key1", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]

class Key2(items.Item):
    def __init__(self):
        super().__init__("Key2", 1) #Note: price is in shillings (a silver coin, 20 per pound)

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
        self.item_hidden = Zeus_bolt()
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
                has_key1 = any(isinstance(item, Key1) for item in config.the_player.inventory)
                has_key2 = any(isinstance(item, Key2) for item in config.the_player.inventory)
                
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
                announce("You start lifting up each and every tile. You get tired about a quarter of the way done.")
                q = input('Would you like to stop?\n')
                if q == 'no':
                    announce("You continue lifting up each and every tile. You get tired again about half of the way done.")
                    w = input('Would you like to stop?\n')
                    if w == 'no':
                        announce("You continue lifting up each and every tile. You get tired once again with about a quarter left.")
                        r = input('Would you like to stop?\n')
                        if r == 'no':
                            announce("You continue lifting up each and every tile. You get tired once again with one left.")
                            s = input('Would you like to pick up the last tile?\n')
                            if s == 'yes':
                                i = self.item_hidden
                                announce("You see a glowing rod type weapon hidden under the tile.")
                                ss = input('Would you like to take it?\n')
                                if ss == 'yes':
                                    announce("You take the "+i.name + " from under the tile.")
                                    config.the_player.add_to_inventory(Zeus_bolt().as_list())
                                    self.item_hidden = None
                                else:
                                    announce("The tiles magically fly back into place")
                            else:
                                announce("The tiles magically fly back into place")
                        else:
                            announce("The tiles magically fly back into place")
                    else:
                        announce("The tiles magically fly back into place")
                else:
                    announce("The tiles magically fly back into place")
            else:
                announce("That doesnt seem to be here")



class Zeus_bolt(items.Item):
    def __init__(self, area_of_effect=2):
        super().__init__("lightningbolt", 99999)
        self.damage = (20, 30)
        self.firearm = False
        self.skill = "magic"
        self.verb = "hit"
        self.verb2 = "hits"
        self.area_of_effect = area_of_effect

    def pickTargets(self, action, attacker, allies, enemies):
        print("Available targets:")
        options = []
        for i, t in enumerate(enemies):
            options.append(f"{i + 1}. Attack {t.name}")
            print(f"{i + 1}. {t.name}")

        chosen_targets = None
        while chosen_targets is None or len(chosen_targets) != 3:
            try:
                choice_input = input("Enter your choice(s): ")
                chosen_targets = [int(index) - 1 for index in choice_input.split(",")]

                if (
                    any(index < 0 or index >= len(enemies) for index in chosen_targets)
                    or len(chosen_targets) != 3
                ):
                    raise ValueError("Please select exactly 3 valid targets.")
            except ValueError as e:
                print(f"Error: {e}")
                chosen_targets = None

        selected_targets = [enemies[i] for i in chosen_targets]
        return selected_targets

    
    
    def as_list(self):
        return [self]
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
        self.events.append(Boss.Boss_fight1())
        self.item_in_boss = Box_lid()
    
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
                announce("You walk up to the boss and rummage through his body only to find a box lid")
                aa = input('would you like to take it\n')
                if aa == 'yes':
                    announce('You take the box lid from the boss carcass')
                    config.the_player.add_to_inventory(Box_lid().as_list())
                    self.item_in_computer = None
                    config.the_player.go = True
                else:
                    announce('You try to walk away but the lid forcibly enters your bag')
                    config.the_player.add_to_inventory(Box_lid().as_list())
                    self.item_in_computer = None
                    config.the_player.go = True
            else:
                announce("That doesnt seem to be here")




