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
        self.health-=damage

    def attack_physical(self, target):
        damage_taken=self.attack-target.combatant.ac
        target.combatant.take_damage(damage_taken)
        # pylint: disable=no-member
        # Fuck off seriously
        print('{0} attacks {1} for {2} HP.'.format(self.owner.name, target.owner.name, str(damage_taken)))