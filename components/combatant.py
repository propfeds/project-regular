#pylint: disable=no-member
class Combatant:
    def __init__(self, health, stamina, attack, ac):
        self.max_hp=health
        self.health=health
        self.max_stam=stamina
        self.stamina=stamina
        self.attack=attack
        # AC (armour class), aka defence, aka whatever
        self.ac=ac

    def take_damage(self, damage):
        results=[]
        self.health-=damage
        if self.health<=0:
            results.append({'dead':self.owner})
        return results

    def attack_physical(self, target):
        results=[]
        damage_taken=self.attack-target.combatant.ac
        results.append({'message': '{0} attacks {1} for {2} HP.'.format(self.owner.name, target.name, str(damage_taken))})
        results.extend(target.combatant.take_damage(damage_taken))
        return results