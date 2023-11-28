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
        print(f"{self.name}'s health: {self.hp}")

    def take_damage(self, damage):
        super().take_damage(damage)
        self.display_health()

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} healed for {amount} health.")
        self.display_health()


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
        attacks["slap"] = ["slaps",75, (10,20)]
        attacks["punch 1"] = ["punches",75, (10,20)]
        attacks["punch 2"] = ["punches",75, (10,20)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(100,150), attacks, 65 + random.randrange(-10,11))
class Keeper(Monster):
    def __init__ (self, name):
        attacks = self.choose_attacks()
        super().__init__(name, random.randrange(250,350), attacks, 150 + random.randrange(-10,11))

    def choose_attacks(self):
        attacks = {}
        
        if 300 >= self.hp:
            attacks["static shock"] = ["shocks", 100, (5, 10)]
        elif 75 <= self.hp < 300:
            attacks["jab"] = ["jabs", 75, (10, 20)]
        else:
            attacks["Thunderbolt"] = ["Strikes", 100, (40, 50)]

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
        if self.hp < 0.2 * self.max_hp:
            heal_amount = random.randint(10, 150)
            self.take_healing(heal_amount)
            self.consecutive_healing_turns += 1
            return superclasses.CombatAction("heal", superclasses.Attack("heal", "heals", heal_amount, (0, 0), True), self)
        else:
            self.consecutive_healing_turns = 0  
            return None  

    def pickAction(self):
        healing_action = self.healing_action()

        if self.consecutive_healing_turns == 3:
            damage_amount = 100
            opponent = self.choose_opponent()
            opponent.take_damage(damage_amount)
            print(f"{self.name} dealt {damage_amount} damage to {opponent.name} due to it exploding.")

            self.hp = 0
            print(f"{self.name} who exploded is now dead.")
            return None 

        if healing_action:
            return healing_action 
        else:
            attacks = self.getAttacks()
            return random.choice(attacks) 

    def choose_opponent(self):
        return random.choice(config.the_player.get_pirates() + self.monsters)
