import tcod as libtcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap

def main():
    screen_width=80
    screen_height=50
    map_width=80
    map_height=45
    colours={
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    player=Entity(int((screen_width+1)/2), int((screen_height+1)/2), '@', libtcod.yellow)
    man=Entity(int((screen_width+1)/2), int((screen_height+1)/2)-2, 'm', libtcod.white)
    entities=[player, man]

    libtcod.console_init_root(screen_width, screen_height, 'Sneks: Multi-Leg Drifting', False)
    con=libtcod.console_new(screen_width, screen_height)
    game_map=GameMap(map_width, map_height)
    key=libtcod.Key()
    mouse=libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, game_map, screen_width, screen_height, colours)
        libtcod.console_flush()
        clear_all(con, entities)

        action=handle_keys(key)
        move=action.get('move')
        exit=action.get('exit')
        fullscreen=action.get('fullscreen')

        if move:
            dx, dy=move
            player.move(dx, dy)
        
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()