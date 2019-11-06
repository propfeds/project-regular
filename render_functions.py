import tcod
from enum import Enum
from game_states import GameStates
from menus import inventory_menu, level_up_menu, mirror_screen

class RenderOrder(Enum):
    CORPSE=1
    ITEM=2
    ACTOR=3

def get_names_mouseover(mouse, entities, fov_map):
    (x, y)=(mouse.cx, mouse.cy)
    names=[entity.name for entity in entities if entity.x==x and entity.y==y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names=', '.join(names)
    return names

def render_bar(panel, x, y, width, name, value, maximum, bar_colour, back_colour):
    filled_width=int(float(value)/maximum*width)
    tcod.console_set_default_background(panel, back_colour)
    tcod.console_rect(panel, x, y, width, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, bar_colour)
    if filled_width>0:
        tcod.console_rect(panel, x, y, filled_width, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int((x+width+1)/2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, mouse, colours, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible=tcod.map_is_in_fov(fov_map, x, y)
                wall=game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('light_ground'), tcod.BKGND_SET)
                    game_map.tiles[x][y].explored=True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_ground'), tcod.BKGND_SET)
    render_ordered_entities=sorted(entities, key=lambda x: x.render_order.value)
    for entity in render_ordered_entities:
        draw_entity(con, entity, fov_map)
    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    # HP bar
    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)
    # Message log
    y=1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.colour)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y+=1
    render_bar(panel, 1, 1, bar_width, 'HP', player.combatant.health, player.combatant.max_hp, tcod.light_red, tcod.darker_red)
    tcod.console_print_ex(panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, 'Gungeon Depth: {0}'.format(game_map.depth))
    # Mouseover details
    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, get_names_mouseover(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, screen_height-panel_height)
    # Taking inventory
    if game_state in (GameStates.INVENTORY, GameStates.DROP_INVENTORY):
        if game_state==GameStates.INVENTORY:
            title='Taking Inventory: Press Escape to escape.\n'
        else:
            title='Dropping Inventory: Press Escape to escape.\n'
        inventory_menu(con, title, player.inventory, 50, screen_width, screen_height)

    elif game_state==GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Power you:', player, 40, screen_width, screen_height)

    elif game_state==GameStates.MIRROR:
        mirror_screen(player, 30, 10, screen_width, screen_height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.colour)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)