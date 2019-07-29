import tcod as libtcod

from game_messages import Message

def heal(*args, **kwargs):
    entity=args[0]
    amount=kwargs.get('amount')
    results=[]
    amount=min(amount, entity.combatant.max_hp-entity.combatant.health)
    entity.combatant.damage(entity, -amount)
    results.append({'used':True, 'message': Message('Your wounds mend! You regain {0} hit points!'.format(amount), libtcod.lighter_blue)})