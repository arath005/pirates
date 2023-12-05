import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Boss_fight3 (event.Event):
    '''
    A combat encounter with a guardian of a distant past.
    When the event is drawn, creates a combat encounter with 2 to 3 drowned pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " Keeper of Death"

    def process (self, world):
        '''Process the event. Populates a combat with monsters. The first Drowned may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the Keeper of Death is defeated!"
        monsters = []
        if random.randrange(10) == 0:
            monsters.append(combat.Death("Ultra Keeper of Death"))
            monsters[0].speed = 1.2*monsters[0].speed
        else:
            monsters.append(combat.Death("Keeper of Death "))
        announce ("You are attacked by a Keeper of Death!")
        combat.Combat(monsters).combat()
        result["newevents"] = []
        return result
