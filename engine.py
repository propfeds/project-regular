import tcod as libtcod
from input_handlers import handle_keys
from game_states import GameStates
from entity import Entity, get_blocking_entities
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_functions import init_fov, recompute_fov
from random import randint
from components.combatant import Combatant
from death_functions import kill_monster, kill_player
from game_messages import MessageLog

def main():
    screen_width=80
    screen_height=50
    map_width=80
    map_height=43
    bar_width=20
    panel_height=7
    message_x=bar_width+2
    message_width=screen_width-bar_width-2
    message_height=panel_height-1

    room_max_size=8
    room_min_size=6
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

    player=Entity(0, 0, '@', libtcod.yellow, 'Ratiel Snailface the Snek Oil Snekman (Player Character)', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=24, stamina=60, attack=8, ac=6))
    entities=[player]

    libtcod.console_set_custom_font('consolas12x12_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'Sneks: The Circles of Angband', False)
    con=libtcod.console_new(screen_width, screen_height)
    panel=libtcod.console_new(screen_width, screen_height-panel_height)
    game_map=GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    fov_recompute=True
    fov_map=init_fov(game_map)
    message_log=MessageLog(message_x, message_width, message_height)

    key=libtcod.Key()
    mouse=libtcod.Mouse()
    game_state=GameStates.PLAYER_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        # This is the render_all just below so I won't have to look for it again
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, mouse, colours)
        fov_recompute=False
        libtcod.console_flush()
        clear_all(con, entities)

        action=handle_keys(key)
        move=action.get('move')
        exit=action.get('exit')
        fullscreen=action.get('fullscreen')

        player_turn_results=[]
        if move and game_state==GameStates.PLAYER_TURN:
            dx, dy=move
            if not game_map.is_blocked(player.x+dx, player.y+dy):
                target=get_blocking_entities(entities, player.x+dx, player.y+dy)
                if target:
                    player_turn_results.extend(player.combatant.attack_physical(target))
                else:
                    player.move(dx, dy)
                    fov_recompute=True
                game_state=GameStates.ENEMY_TURN
        
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for announcement in player_turn_results:
            message=announcement.get('message')
            dead=announcement.get('dead')
            if message:
                message_log.add_message(message)
            if dead:
                if dead==player:
                    message, game_state=kill_player(dead)
                else:
                    message=kill_monster(dead)
                message_log.add_message(message)

        if game_state==GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results=entity.ai.take_turn(player, fov_map, game_map, entities)
                    for announcement in enemy_turn_results:
                        message=announcement.get('message')
                        dead=announcement.get('dead')
                        if message:
                            message_log.add_message(message)
                        if dead:
                            if dead==player:
                                message, game_state=kill_player(dead)
                            else:
                                message=kill_monster(dead)
                            message_log.add_message(message)
                            if game_state==GameStates.PLAYER_DEAD:
                                break
                    if game_state==GameStates.PLAYER_DEAD:
                        break
            else:
                game_state=GameStates.PLAYER_TURN

if __name__ == '__main__':
    main()