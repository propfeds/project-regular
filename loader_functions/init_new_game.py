import tcod as libtcod
from components.combatant import Combatant
from components.inventory import Inventory
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder

def get_constants():
    constants={
        'window_title': 'Project Regular 2: Dance of the Bugs: The Circles of Angband: Prop\'s Awakening',
        'screen_width': 80,
        'screen_height': 50,
        'bar_width': 20,
        'panel_height': 7,
        'message_x': 22,
        'message_width': 58,
        'message_height': 6,
        'map_width': 80,
        'map_height': 43,
        'room_max_size': 8,
        'room_min_size': 6,
        'max_rooms': 40,
        'fov_algorithm': 0,
        'fov_light_walls': True,
        'fov_radius': 7,
        'max_monsters_per_room': 3,
        'max_items_per_room': 2,
        'colours':
        {
            'dark_wall': libtcod.Color(75, 105, 47),
            'dark_ground': libtcod.Color(82, 75, 36),
            'light_wall': libtcod.Color(106, 190, 48),
            'light_ground': libtcod.Color(138, 111, 48)
        }
    }
    return constants

def get_game_vars(constants):
    player=Entity(0, 0, '@', libtcod.yellow, 'Ratiel Snailface the Snek Oil Snekman (Player Character)', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=24, stamina=60, attack=8, ac=6), item=None, inventory=Inventory(26))
    entities=[player]

    game_map=GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])

    message_log=MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])
    
    game_state=GameStates.PLAYER_TURN
    return player, entities, game_map, message_log, game_state