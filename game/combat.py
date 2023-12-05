import random
import game.config as config
import game.crewmate as crew
import game.superclasses as superclasses
from game.context import Context
from game.display import announce
from game.display import menu

class Combat():

    def __init__ (self, monsters):
        self.monsters = monsters
    def get_monsters(self):
        return self.monsters

    def process_verb (self, verb, cmd_list, nouns):
        print (self.nouns + " can't " + verb)

    def crewmateAction(self, attacker, allies, enemies):
        """The player chooses an action for a crewmate to take."""
        announce(attacker.get_name() + " has seized the initiative! What should they do?",pause=False)
        actions = attacker.getAttacks()
        # actions = attacker.getMiscActions()
        if len(actions) > 0:
            choice = menu (actions)
            return actions[choice]
        #else: run in circles, scream and shout
        return None

    def combat (self):
        while len(self.monsters):
            combatants = config.the_player.get_pirates() + self.monsters
            min_t = None
            for c in combatants:
                t = (100 - c.cur_move)/c.speed
                if min_t == None:
                    min_t = t
                else:
                    min_t = min(t, min_t)
            for c in combatants:
                c.cur_move += c.speed*min_t
            speeds = [c.cur_move for c in combatants]
            max_move = max(speeds)
            ready = [c for c in combatants if c.cur_move == max_move]
            moving = random.choice(ready)
            moving.cur_move = 0
            if isinstance(moving, crew.CrewMate):
                chosen_action = self.crewmateAction(moving, config.the_player.get_pirates(), self.monsters)
                if(chosen_action != None):
                    chosen_targets = chosen_action.pickTargets(chosen_action, moving, config.the_player.get_pirates(), self.monsters)
            else:
                chosen_targets = [random.choice(config.the_player.get_pirates())]
                chosen_action = moving.pickAction()
            #Resolve
            chosen_action.resolve(chosen_action, moving, chosen_targets)
            self.monsters = [m for m in self.monsters if m.health >0]
            config.the_player.cleanup_items()

            for monster in self.monsters:
                monster.display_health()


class Monster(superclasses.CombatCritter):
    def __init__ (self, name: str, hp: int, attacks: dict[str, list], speed: float):
        super().__init__(name, hp, speed)
        self.attacks = attacks
        self.cur_move = 0

    def getAttacks(self):
        attacks = []
        for key in self.attacks.keys():
            attack = superclasses.Attack(key, self.attacks[key][0], self.attacks[key][1], self.attacks[key][2], False)
            attacks.append(superclasses.CombatAction(attack.name, attack, self))
        return attacks
    
    def display_health(self):
        print(f"{self.name}'s health: {self.health}")

    def take_damage(self, damage):
        super().take_damage(damage)
        self.display_health()

    #def heal(self, amount):
    #    self.health += amount
    #    if self.health > self.max_health:
    #        self.health = self.max_health
    #    print(f"{self.name} healed for {amount} health.")
    #    self.display_health()


    def pickAction(self):
        attacks = self.getAttacks()
        return random.choice(attacks)

class Macaque(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))

class Drowned(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (5,15)]
        attacks["punch 1"] = ["punches",random.randrange(35,51), (1,10)]
        attacks["punch 2"] = ["punches",random.randrange(35,51), (1,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))

class Guardian(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["slap"] = ["slaps",75, (5,10)]
        attacks["punch 1"] = ["punches",75, (5,10)]
        attacks["punch 2"] = ["punches",75, (5,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(50,100), attacks, 65 + random.randrange(-10,11))
class Keeper(Monster):
    def __init__(self, name):
        attacks = {}
        super().__init__(name, random.randrange(250, 350), attacks, 150 + random.randrange(-10, 11))

    def getAttacks(self):
        attacks = []

        if self.health >= 300:
            attacks.append(superclasses.CombatAction("static shock", superclasses.Attack("static shock", "shocks", 100, (5, 10), False), self))
        elif self.health < 300 and self.health >= 75:
            attacks.append(superclasses.CombatAction("jab", superclasses.Attack("jab", "jabs", 75, (10, 20), False), self))
        else:
            attacks.append(superclasses.CombatAction("Thunderbolt", superclasses.Attack("Thunderbolt", "Strikes", 100, (40, 50), False), self))

        return attacks


    
    

class Waterkeeper(Monster):
    def __init__(self, name):
        attacks = {}
        attacks["water gun"] = ["shoots", 100, (5, 10)]
        attacks["water beam"] = ["beems", 75, (10, 15)]
        attacks["waterfall"] = ["floods", 33, (15, 20)]
        attacks["heal"] = ["heals", 0, (0, 0)] 
        super().__init__(name, random.randrange(1000, 1500), attacks, 70 + random.randrange(-10, 11))
        self.consecutive_healing_turns = 0

        

    def healing_action(self):
        if self.health < 0.2 * self.max_health:
            self.consecutive_healing_turns += 1
            return superclasses.CombatAction("heal", superclasses.Heal("heal", "heals"), self)
        else:
            self.consecutive_healing_turns = 0  
            #Can return none, but you have to notice it
            return None  

    def pickAction(self):
        healing_action = self.healing_action()

        if self.consecutive_healing_turns == 3:
            #Don't do an explosion like this, use an Attack() instead... or maybe a new action type called Explode()?
            
            #Don't reurn None from pickAction probably. This would instead be the Attack() or Explode() from above
            return superclasses.CombatAction("explode", superclasses.Explode("explode", "explodes"), self)

        if healing_action:
            return healing_action 
        else:
            attacks = self.getAttacks()
            return random.choice(attacks) 


class Death(Monster):
    def __init__(self, name):
        attacks = {}
        super().__init__(name, 50, attacks, 100 + random.randrange(-10, 11))
        self.deathcount = 0
    def getAttacks(self):
        attacks = []

        if self.health <= 75:
            attacks.append(superclasses.CombatAction("Deathly Touch", superclasses.Attack("Deathly Touch", "Drains", 100, (1, 100), False), self))
        

        return attacks
    
    def inflict_damage (self, num, deathcause, combat = False):
        self.health = self.health - num
        if(self.health > 0):
            self.health = self.max_health
            return None
        else:
            if self.deathcount != 3:
                self.deathcount += 1

                announce("You have killed death " +str(self.deathcount)  + " times")
                self.health = self.max_health
                return None
            
            

        for d in self.defendees:
            d.removeDefender(self)
        self.defendees = []
        for d in self.defenders:
            d.removeDefendee(self)
        self.defenders = []
        return self
