from equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, main_hand=None, off_hand=None, finger=None):
        self.main_hand=main_hand
        self.off_hand=off_hand
        self.finger=finger
    
    @property
    def bonus_max_hp(self):
        total=0
        if self.main_hand and self.main_hand.equippable:
            total+=self.main_hand.equippable.bonus_max_hp
        if self.off_hand and self.off_hand.equippable:
            total+=self.off_hand.equippable.bonus_max_hp
        if self.finger and self.finger.equippable:
            total+=self.finger.equippable.bonus_max_hp
        
        return total

    @property
    def bonus_attack(self):
        total=0
        if self.main_hand and self.main_hand.equippable:
            total+=self.main_hand.equippable.bonus_attack
        if self.off_hand and self.off_hand.equippable:
            total+=self.off_hand.equippable.bonus_attack
        if self.finger and self.finger.equippable:
            total+=self.finger.equippable.bonus_attack
        
        return total

    @property
    def bonus_ac(self):
        total=0
        if self.main_hand and self.main_hand.equippable:
            total+=self.main_hand.equippable.bonus_ac
        if self.off_hand and self.off_hand.equippable:
            total+=self.off_hand.equippable.bonus_ac
        if self.finger and self.finger.equippable:
            total+=self.finger.equippable.bonus_ac
        
        return total

    def toggle_equip(self, equippable_entity):
        results=[]

        slot=equippable_entity.equippable.slot
        if slot==EquipmentSlots.MAIN_HAND:
            if self.main_hand==equippable_entity:
                self.main_hand=None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})
                self.main_hand=equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot==EquipmentSlots.OFF_HAND:
            if self.off_hand==equippable_entity:
                self.off_hand=None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})
                self.off_hand=equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot==EquipmentSlots.FINGER:
            if self.finger==equippable_entity:
                self.finger=None
                results.append({'dequipped': equippable_entity})
            else:
                if self.finger:
                    results.append({'dequipped': self.finger})
                self.finger=equippable_entity
                results.append({'equipped': equippable_entity})
        
        return results