class Equippable:
    def __init__(self, slot, bonus_attack=0, bonus_ac=0, bonus_max_hp=0):
        self.slot=slot
        self.bonus_attack=bonus_attack
        self.bonus_ac=bonus_ac
        self.bonus_max_hp=bonus_max_hp