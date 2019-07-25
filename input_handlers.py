import tcod as libtcod

def handle_keys(key):
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

    # Big Screen
    if key.vk==libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    # Death to the Game Session
    elif key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Nuttin Press
    return {}