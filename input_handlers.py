import tcod as libtcod

def handle_keys(key):
    #Movement
    if key.vk==libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk==libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk==libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk==libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    #Big Screen
    if key.vk==libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    #Death to the Game Session
    elif key.vk==libtcod.KEY_ESCAPE:
        return {'exit': True}

    #Nuttin Press
    return {}