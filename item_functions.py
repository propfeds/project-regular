import tcod as libtcod

from game_messages import Message

def heal(*args, **kwargs):
    entity=args[0]
    amount=kwargs.get('amount')
    results=[]
    amount=min(amount, entity.combatant.max_hp-entity.combatant.health)
    entity.combatant.take_damage(-amount)
    results.append({'used':True, 'message': Message('Your wounds mend! You regain {0} hit points!'.format(amount), libtcod.lighter_blue)})
    return results

def dorkbolt(*args, **kwargs):
    # seeks the nearest foe
    caster=args[0]
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    damage=kwargs.get('damage')
    maximum_range=kwargs.get('maximum_range')
    results=[]
    target=None
    closest_distance=maximum_range+1
    for entity in entities:
        if entity.combatant and entity!=caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance=caster.distance_to(entity) # also chebyshev lol
            if distance<closest_distance:
                target=entity
                closest_distance=distance
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A dorkbolt spawns from the veins of the earth and strikes the {0} for {1} damage!'.format(target.name, damage))})
        results.extend(target.combatant.take_damage(damage))
    else:
        results.append({'consumed': True, 'target': None, 'message': Message('A dorkbolt spawns from the veins of the earth and quickly dissipates.', libtcod.red)})
    return results