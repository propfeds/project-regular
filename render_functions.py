import tcod as libtcod
from enum import Enum
from game_states import GameStates
from menus import inventory_menu

class RenderOrder(Enum):
    CORPSE=1
    ITEM=2
    ACTOR=3

def get_names_mouseover(mouse, entities, fov_map):
    (x, y)=(mouse.cx, mouse.cy)
    names=[entity.name for entity in entities if entity.x==x and entity.y==y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names=', '.join(names)
    return names

def render_bar(panel, x, y, width, name, value, maximum, bar_colour, back_colour):
    filled_width=int(float(value)/maximum*width)
    libtcod.console_set_default_background(panel, back_colour)
    libtcod.console_rect(panel, x, y, width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, bar_colour)
    if filled_width>0:
        libtcod.console_rect(panel, x, y, filled_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int((x+width+1)/2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, mouse, colours, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible=libtcod.map_is_in_fov(fov_map, x, y)
                wall=game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colours.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colours.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored=True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colours.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colours.get('dark_ground'), libtcod.BKGND_SET)
    render_ordered_entities=sorted(entities, key=lambda x: x.render_order.value)
    for entity in render_ordered_entities:
        draw_entity(con, entity, fov_map)
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    # HP bar
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    # Message log
    y=1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.colour)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y+=1
    render_bar(panel, 1, 1, bar_width, 'HP', player.combatant.health, player.combatant.max_hp, libtcod.light_red, libtcod.darker_red)
    # Mouseover details
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_mouseover(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, screen_height-panel_height)
    # Taking inventory
    if game_state==GameStates.INVENTORY:
        inventory_menu(con, 'Taking Inventory: Press Escape to escape.\n', player.inventory, 50, screen_width, screen_height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.colour)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)