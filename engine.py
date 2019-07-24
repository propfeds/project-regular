import tcod as libtcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
from fov_functions import init_fov, recompute_fov

def main():
    screen_width=80
    screen_height=50
    map_width=80
    map_height=45
    room_max_size=8
    room_min_size=5
    max_rooms=40
    max_monsters_per_room=3
    fov_algorithm=0
    fov_light_walls=True
    fov_radius=7
    # Credits: DB32 Palette
    colours={
        'dark_wall': libtcod.Color(75, 105, 47),
        'dark_ground': libtcod.Color(82, 75, 36),
        'light_wall': libtcod.Color(106, 190, 48),
        'light_ground': libtcod.Color(138, 111, 48)
    }

    player=Entity(0, 0, '@', libtcod.brass)
    entities=[player]

    libtcod.console_init_root(screen_width, screen_height, 'Sneks: The Circles of Angband', False)
    con=libtcod.console_new(screen_width, screen_height)
    game_map=GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    fov_recompute=True
    fov_map=init_fov(game_map)
    key=libtcod.Key()
    mouse=libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colours)
        fov_recompute=False
        libtcod.console_flush()
        clear_all(con, entities)

        action=handle_keys(key)
        move=action.get('move')
        exit=action.get('exit')
        fullscreen=action.get('fullscreen')

        if move:
            dx, dy=move
            if not game_map.is_blocked(player.x+dx, player.y+dy):
                player.move(dx, dy)
                fov_recompute=True
        
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()