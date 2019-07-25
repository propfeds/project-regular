import tcod as libtcod
from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.char='%'
    player.colour=libtcod.dark_red
    return 'You have departed.', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message='The {0} has departed.'.format(monster.name)
    monster.char='%'
    monster.colour=libtcod.dark_red
    monster.ai=None
    monster.combatant=None
    monster.block_movement=False
    monster.render_order=RenderOrder.CORPSE
    monster.name='A {0} corpse'.format(monster.name)
    return death_message