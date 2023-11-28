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
from game.events import Boss2
from game.crewmate import CrewMate


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
        announce("You see some tridents and ruins on an island")
        num_crewmates = len(Player.get_pirates())
        announce(num_crewmates)
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
        self.item_in_sand = Trident()

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
        announce ("You arrived at an island and see pillars and tridents on the island. You anchor at the south bay")

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
            announce("You see strange writing on the side of a piller as well as hundreds of spears that seem to be burried and sticking out of the sand")
            res = input ("What would you like to inspect further\n:")
            if res == "writing":
                announce("You look at the wall and read the following.\n'zhofrph wr wkh grpdlq ri wkh jrgv'\n'welcome to the domain of the gods'")

            if res == "tridents" or res == "trident" or res == "Trident" or res == "Tridents":
                announce("you try to find all the tridents and try to count them and you find 500")
                pos = input('which trident would you like to inspect\n')
                pos = int(pos)
                if type(pos) == int:
                    if pos == 373:
                        config.the_player.add_to_inventory(Trident().as_list())
                        self.item_in_sand = None
                        announce('You pick up the rusty trident and it transforms into a sliver-blue Trident and rushes into your bag')
                    else:
                        announce('The weapons falls through you hand and reappears in the sand')
                else:
                    announce('You decide to give up')

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
        self.item_in_computer = Key3()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk into a building holding a huge pool like structure")
    
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
            announce("You see strange writing on the wall of the pool as well as a keyboard")
            res = input ("What would you like to inspect further\n:")
            if res == "writing":
                encrypted_message = self.caesar_cipher("what do i rule over", 3)
                announce("You look at the wall and read the following.\n"+ encrypted_message)
            elif res == "keyboard":
                ans = input("Please answer the text\n:")
                if ans == "sea" or ans == "ocean" or ans == "water":
                    announce("correct\nkrrr krrr")
                    i = self.item_in_computer
                    announce("You take the "+i.name + " from the computer.")
                    #config.the_player.add_to_inventory(i)
                    config.the_player.add_to_inventory(Key3().as_list())

                    self.item_in_computer = None
                    config.the_player.go = True
            elif res == "pool":
                announce("you see the water in the pool shoot out and fly through the air making many shapes and patterns")
            else:
                announce("That doesnt seem to be here")

class Puzzle2(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "puzzle2"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        

        #add some treasure!
        self.verbs["take"] = self
        self.item_in_computer = Key4()
        self.event_chance = 30
        self.events.append(guardian.Guardian_attack())
        

    def enter (self):
        announce("You walk through a portal leading you to an underwater dome")
        

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
            announce("You walk into the edge of the dome and feel stupid")

        if(verb == "inspect"):
            announce("you see a huge ancient building in pristine condition")
            res = input ("what would you like to inspect further\n")
            if res == "building":
                announce("You walk into the building and see some strange writing on the wall, a keyboard, and a pedestal with a hole in the middle of it")
                ress = input("what would you like to inspect")
                if ress == "writing":
                    encrypted_message = self.caesar_cipher("What is my roman name", 3)
                    announce("you gaze upon the writing a see\n" + encrypted_message)
                if ress == "pedestal":
                    announce("you look at the pedestal with a hole in the middle and you feel like something is supposed to go here")
                    resss = input("what would you like to put in")
                    if resss == "Trident":
                        has_tri = any(isinstance(item, Trident) for item in config.the_player.inventory)
                        if has_tri:
                            announce("you insert the trident into the hole and a secret room opens up")
                            aa = input("would you like to enter")
                            if aa == "yes":
                                announce("you anter the room and see a huge statue of a being the looks very strong")
                                aaa = input("what would you like to inspect")
                                if aaa == ("statue"):
                                    announce("you start to inspect the statue and get a strange urge to start to pray to the statue")
                                    aaaa = input("would you like to pray")
                                    if aaaa == "yes":
                                        num_crewmates = len(player.get_pirates())
                                        crewmates = [CrewMate() for _ in num_crewmates]
                                        lowest_magic_crewmate = min(crewmates, key=lambda crewmate: crewmate.skills["magic"])
                                        lowest_magic_crewmate.skills["magic"] = 100
                                        announce(lowest_magic_crewmate.name + " now has magic skill 100")
                                        #make it so the part member with the lowest magic gets 100 magic


                elif ress == "keyboard":
                    announce("You walk around the back of the pillar only to find a keyboard")
                    ans = input("answer the question\n")
                    if ans == "neptune" or ans == 'Neptune':
                        announce("correct\nkrrr krrr")
                        i = self.item_in_computer
                        announce("You take the "+ i.name + " from the computer.")
                            #config.the_player.add_to_inventory(i)
                        config.the_player.add_to_inventory(Key4().as_list())

                        self.item_in_computer = None
                        config.the_player.go = True
                else:
                    announce("That doesnt seem to be here, you exit the buiding")
            else:
                announce("That doesnt seem to be here")
    
    
        
                



class Box(items.Item):
    def __init__(self):
        super().__init__("Box", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]
    
class Key3(items.Item):
    def __init__(self):
        super().__init__("Key3", 1) #Note: price is in shillings (a silver coin, 20 per pound)

    def as_list(self):
        return [self]

class Key4(items.Item):
    def __init__(self):
        super().__init__("Key4", 1) #Note: price is in shillings (a silver coin, 20 per pound)

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
        self.verbs["back"] = self
        

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
                has_key1 = any(isinstance(item, Key3) for item in config.the_player.inventory)
                has_key2 = any(isinstance(item, Key4) for item in config.the_player.inventory)
                
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
        self.events.append(Boss2.Boss_fight2())
        self.item_in_boss = Box()
    
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
                announce("You walk up to the boss and rummage through his body only to find a box without a lid or hinge")
                aa = input('would you like to take it\n')
                if aa == 'yes':
                    announce('You take the box from the boss carcass')
                    config.the_player.add_to_inventory(Box().as_list())
                    self.item_in_computer = None
                    config.the_player.go = True
                else:
                    announce('You try to walk away but the Box forcibly enters your bag')
                    config.the_player.add_to_inventory(Box().as_list())
                    self.item_in_computer = None
                    config.the_player.go = True
            else:
                announce("That doesnt seem to be here")



class Trident(items.Item):
    def __init__(self):
        super().__init__("Trident", 99999)
        self.damage = (15)
        self.firearm = False
        self.skill = "magic"
        self.verb = "flood"
        self.verb2 = "flooded"

    def pickTargets(self, action, attacker, allies, enemies): 
        print("All enemies will be hit by the Trident.")
        selected_targets = enemies
        return selected_targets

    def as_list(self):
        return [self]
