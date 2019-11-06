import tcod
from game_states import GameStates
from render_functions import RenderOrder
from components.item import Item
from game_messages import Message

def kill_player(player):
    player.char='%'
    player.colour=tcod.dark_red
    return Message('You have departed.', tcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message=Message('The {0} has departed.'.format(monster.name), tcod.orange)
    monster.char='%'
    monster.colour=tcod.dark_red
    monster.ai=None
    monster.combatant=None
    monster.block_movement=False
    monster.render_order=RenderOrder.CORPSE
    monster.item=Item()
    monster.name='A {0} corpse'.format(monster.name)
    return death_message