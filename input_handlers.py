import tcod as libtcod
from game_states import GameStates

def handle_keys(key, game_state):
    if game_state==GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key)
    elif game_state==GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state==GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    return {}

def handle_player_turn_keys(key):
    key_char=chr(key.c)
    # Movement
    if key.vk==libtcod.KEY_KP8 or key_char=='k':
        return {'move': (0, -1)}
    elif key.vk==libtcod.KEY_KP2 or key_char=='j':
        return {'move': (0, 1)}
    elif key.vk==libtcod.KEY_KP4 or key_char=='h':
        return {'move': (-1, 0)}
    elif key.vk==libtcod.KEY_KP6 or key_char=='l':
        return {'move': (1, 0)}
    elif key.vk==libtcod.KEY_KP7 or key_char=='y':
        return {'move': (-1, -1)}
    elif key.vk==libtcod.KEY_KP9 or key_char=='u':
        return {'move': (1, -1)}
    elif key.vk==libtcod.KEY_KP1 or key_char=='b':
        return {'move': (-1, 1)}
    elif key.vk==libtcod.KEY_KP3 or key_char=='n':
        return {'move': (1, 1)}
    # Crab Grab
    if key_char=='g':
        return {'pickup': True}
    # Unto the Big Bag
    if key_char=='i':
        return {'take_inventory': True}
    elif key_char=='d':
        return {'drop_inventory': True}
    # Big Screen
    if key.vk==libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    # Death to the Game Session
    elif key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}
    # Nuttin Press
    return {}

def handle_targeting_keys(key):
    if key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

def handle_mouse(mouse):
    (x, y)=(mouse.cx, mouse.cy)
    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    return {}

def handle_player_dead_keys(key):
    key_char=chr(key.c)
    if key_char=='i':
        return {'take_inventory': True}
    elif key.vk==libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

def handle_inventory_keys(key):
    index = key.c-ord('a')
    if index>=0:
        return {'inventory_index': index}
    if key.vk==libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}