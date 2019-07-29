import tcod as libtcod
from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
    player.char='%'
    player.colour=libtcod.dark_red
    return Message('You have departed.', libtcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message=Message('The {0} has departed.'.format(monster.name), libtcod.orange)
    monster.char='%'
    monster.colour=libtcod.dark_red
    monster.ai=None
    monster.combatant=None
    monster.block_movement=False
    monster.render_order=RenderOrder.CORPSE
    monster.name='A {0} corpse'.format(monster.name)
    return death_message