import tcod
from components.ai import ConfusedLad
from game_messages import Message

def heal(*args, **kwargs):
    entity=args[0]
    amount=kwargs.get('amount')
    results=[]
    amount=min(amount, entity.combatant.max_hp-entity.combatant.health)
    entity.combatant.take_damage(-amount)
    results.append({'consumed': True, 'message': Message('Your wounds mend! You regain {0} hit points!'.format(amount), tcod.lighter_blue)})
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
        if entity.combatant and entity!=caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance=caster.distance_to(entity) # also chebyshev lol
            if distance<closest_distance:
                target=entity
                closest_distance=distance
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A dorkbolt spawns from the veins of the earth and strikes the {0} for {1} damage!'.format(target.name, damage))})
        results.extend(target.combatant.take_damage(damage))
    else:
        results.append({'consumed': True, 'target': None, 'message': Message('A dorkbolt spawns from the veins of the earth and quickly dissipates.', tcod.red)})
    return results

def dorkblast(*args, **kwargs):
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    damage=kwargs.get('damage')
    radius=kwargs.get('radius')
    target_x=kwargs.get('target_x')
    target_y=kwargs.get('target_y')
    results=[]
    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You can\'t see where you\'re firing!', tcod.yellow)})
        return results
    results.append({'consumed': True, 'message': Message('A clump of dork dislodges from the ground!')})
    for entity in entities:
        if entity.distance_to_point(target_x, target_y)<=radius and entity.combatant:
            results.append({'message': Message('The {0} takes {1} damage from the blast.'.format(entity.name, damage))})
            results.extend(entity.combatant.take_damage(damage))
    return results

def confusodockulus(*args, **kwargs):
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    target_x=kwargs.get('target_x')
    target_y=kwargs.get('target_y')

    results=[]

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Confusodockulus whom beyond thine eyes?', tcod.yellow)})
        return results

    for entity in entities:
        if entity.x==target_x and entity.y==target_y and entity.ai:
            entity.ai=ConfusedLad(entity.ai, 23)
            entity.ai.owner=entity
            results.append({'consumed': True, 'message': Message('The eyes of the {0} turn as hollow as a Kripto.'.format(entity.name), tcod.light_green)})
            break
    else:
        results.append({'consumed': False, 'message': Message('Confusodockulus whom within thine eyes?', tcod.yellow)})
    return results