#pylint: disable=no-member
import tcod
from game_messages import Message
class Combatant:
    def __init__(self, health, stamina, attack, ac, xp=0):
        self.max_hp=health
        self.health=health
        self.max_stam=stamina
        self.stamina=stamina
        self.attack=attack
        # AC (armour class), aka defence, aka whatever
        self.ac=ac
        self.xp=xp

    def take_damage(self, damage):
        results=[]
        self.health-=damage
        if self.health<=0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def attack_physical(self, target):
        results=[]
        damage_taken=max(0, self.attack-target.combatant.ac)
        if damage_taken>0:
            results.append({'message': Message('{0} attacks {1} for {2} HP.'.format(self.owner.name, target.name, str(damage_taken)), tcod.white)})
        results.extend(target.combatant.take_damage(damage_taken))
        return results