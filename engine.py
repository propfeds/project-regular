import tcod
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from game_states import GameStates
from entity import get_blocking_entities
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
from fov_functions import init_fov, recompute_fov
from random import randint
from components.combatant import Combatant
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from game_messages import Message
from loader_functions.init_new_game import get_constants, get_game_vars
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, menu

def start_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute=True
    fov_map=init_fov(game_map)
    # Any menu will return to the previous game state
    key=tcod.Key()
    mouse=tcod.Mouse()

    prev_game_state=game_state
    targeting_item=None

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
        # This is the render_all just below so I won't have to look for it again
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], mouse, constants['colours'], game_state)
        fov_recompute=False
        tcod.console_flush()
        clear_all(con, entities)

        action=handle_keys(key, game_state)
        mouse_action=handle_mouse(mouse)

        move=action.get('move')
        wait=action.get('wait')
        pickup=action.get('pickup')
        take_inventory=action.get('take_inventory')
        drop_inventory=action.get('drop_inventory')
        inventory_index=action.get('inventory_index')
        take_stairs=action.get('take_stairs')
        level_up=action.get('level_up')
        mirror=action.get('mirror')
        exit=action.get('exit')
        fullscreen=action.get('fullscreen')
        
        left_click=mouse_action.get('left_click')
        right_click=mouse_action.get('right_click')

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

        elif wait:
            game_state=GameStates.ENEMY_TURN

        elif pickup and game_state==GameStates.PLAYER_TURN:
            for entity in entities:
                if entity.item and entity.x==player.x and entity.y==player.y:
                    player_turn_results.extend(player.inventory.add_item(entity))
                    break
            else:
                message_log.add_message(Message('You grab the ground for no reason.', tcod.yellow))

        if take_inventory:
            prev_game_state=game_state
            game_state=GameStates.INVENTORY
        
        if drop_inventory:
            prev_game_state=game_state
            game_state=GameStates.DROP_INVENTORY

        if inventory_index is not None and prev_game_state!=GameStates.PLAYER_DEAD and inventory_index<len(player.inventory.contents):
            item=player.inventory.contents[inventory_index]
            if game_state==GameStates.INVENTORY:
                player_turn_results.extend(player.inventory.use_item(item, entities=entities, fov_map=fov_map))
            elif game_state==GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state==GameStates.PLAYER_TURN:
            for entity in entities:
                if entity.stairs and entity.x==player.x and entity.y==player.y:
                    entities=game_map.next_floor(player, message_log, constants)
                    fov_map=init_fov(game_map)
                    fov_recompute=True
                    tcod.console_clear(con)
                    break
            else:
                message_log.add_message(Message('Dive what?', tcod.yellow))

        if level_up:
            if level_up=='hp':
                player.combatant.max_hp+=20
                player.combatant.health+=20
            elif level_up=='atk':
                player.combatant.attack+=1
            elif level_up=='ac':
                player.combatant.ac+=1

            game_state=prev_game_state

        if mirror:
            prev_game_state=game_state
            game_state=GameStates.MIRROR

        if game_state==GameStates.TARGETING:
            if left_click:
                target_x, target_y=left_click
                item_use_results=player.inventory.use_item(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        player_turn_results.append({'targeting_cancelled': True})
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.INVENTORY, GameStates.DROP_INVENTORY, GameStates.MIRROR):
                game_state=prev_game_state
            elif game_state==GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for announcement in player_turn_results:
            message=announcement.get('message')
            dead=announcement.get('dead')
            item_added=announcement.get('item_added')
            item_consumed=announcement.get('item_consumed')
            item_dropped=announcement.get('item_dropped')
            targeting=announcement.get('targeting')
            targeting_cancelled=announcement.get('targeting_cancelled')
            xp=announcement.get('xp')
            if message:
                message_log.add_message(message)
            if dead:
                if dead==player:
                    message, game_state=kill_player(dead)
                else:
                    message=kill_monster(dead)
                message_log.add_message(message)
            if item_added:
                entities.remove(item_added)
                game_state=GameStates.ENEMY_TURN
            if item_consumed:
                game_state=GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                game_state=GameStates.ENEMY_TURN
            if targeting:
                prev_game_state=GameStates.PLAYER_TURN
                game_state=GameStates.TARGETING
                targeting_item=targeting
                message_log.add_message(targeting_item.item.targeting_message)
            if targeting_cancelled:
                game_state=prev_game_state
                message_log.add_message(Message('Targeting cancelled.'))
            if xp:
                leveled_up=player.level.add_xp(xp)
                message_log.add_message(Message('+{0} xp.'.format(xp)))
                if leveled_up:
                    message_log.add_message(Message('You strong. To level {0}!'.format(player.level.current_level), tcod.yellow))
                    prev_game_state=game_state
                    game_state=GameStates.LEVEL_UP

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

def main():
    constants=get_constants()

    tcod.console_set_custom_font('consolas12x12_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    con=tcod.console_new(constants['screen_width'], constants['screen_height'])
    panel=tcod.console_new(constants['screen_width'], constants['screen_height']-constants['panel_height'])

    player=None
    entities=[]
    game_map=None
    message_log=None
    game_state=None
    show_main_menu=True
    show_load_error_message=False
    main_menu_background_image=tcod.image_load('menu_background.png')

    key=tcod.Key()
    mouse=tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS|tcod.EVENT_MOUSE, key, mouse)
        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])
            if show_load_error_message:
                menu(con, 'Save game unfound', [], 50, constants['screen_width'], constants['screen_height'])
            tcod.console_flush()

            action=handle_main_menu(key)
            new_game=action.get('new_game')
            load_game_bool=action.get('load_game')
            exit_game=action.get('exit')

            if show_load_error_message and (new_game or load_game or exit_game):
                show_load_error_message=False
            elif new_game:
                player, entities, game_map, message_log, game_state=get_game_vars(constants)
                show_main_menu=False
            elif load_game_bool:
                try:
                    player, entities, game_map, message_log, game_state=load_game()
                    show_main_menu=False
                except FileNotFoundError:
                    show_load_error_message=True
            elif exit_game:
                break
        else:
            tcod.console_clear(con)
            start_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu=True
if __name__ == '__main__':
    main()