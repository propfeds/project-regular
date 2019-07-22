import tcod as libtcod
from input_handlers import handle_keys

def main():
    screen_width=80
    screen_height=50
    pos_x=int((screen_width+1)/2)
    pos_y=int((screen_height+1)/2)

    libtcod.console_init_root(screen_width, screen_height, 'Sneks: Multi-Leg Drifting', False)
    con=libtcod.console_new(screen_width, screen_height)
    key=libtcod.Key()
    mouse=libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, pos_x, pos_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()
        libtcod.console_put_char(con, pos_x, pos_y, ' ', libtcod.BKGND_NONE)

        action=handle_keys(key)
        move=action.get('move')
        exit=action.get('exit')
        fullscreen=action.get('fullscreen')

        if move:
            dx, dy=move
            pos_x+=dx
            pos_y+=dy
        
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()