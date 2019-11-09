import tcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options)>26:
        raise ValueError('Cannot have a menu bigger than the English alphabet.')
    # Calculate height after word wrap
    header_height=tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height=len(options)+header_height
    window=tcod.console_new(width, height)
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)
    # Print
    y=header_height
    letter_index=ord('a')
    for option_text in options:
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, '('+chr(letter_index)+') '+option_text)
        y+=1
        letter_index+=1
    x=int(screen_width/2-width/2)
    y=int(screen_height/2-height/2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1, 0.7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    if len(player.inventory.contents)==0:
        options=['More weight is required.']
    else:
        options=[('{0} ({1})'.format(item.name, item.equippable.slot.name) if (item==player.equipment.main_hand or item==player.equipment.off_hand or item==player.equipment.finger) else item.name) for item in player.inventory.contents]
    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, bg_image, screen_width, screen_height):
    tcod.image_blit_2x(bg_image, 0, 0, 0)
    tcod.console_set_default_foreground(0, tcod.light_yellow)
    tcod.console_print_ex(0, int(screen_width/2), int(screen_height/2)-4, tcod.BKGND_NONE, tcod.CENTER, 'REGULAR AWAKENING')
    tcod.console_print_ex(0, int(screen_width/2), int(screen_height/2), tcod.BKGND_NONE, tcod.CENTER, 'By Porp yours truely <3')

    menu(con, '', ['New Game', 'Load Game', 'Bye Mates'], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options=['Helth (+13 HP)', 'Stremf (+2 Attack)', 'Doge (+1 AC)']

    menu(con, header, options, menu_width, screen_width, screen_height)

def mirror_screen(player, mirror_width, mirror_height, screen_width, screen_height):
    window=tcod.console_new(mirror_width, mirror_height)
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 1, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'In the Mirror you see yourself:')
    tcod.console_print_rect_ex(window, 0, 2, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    tcod.console_print_rect_ex(window, 0, 3, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    tcod.console_print_rect_ex(window, 0, 4, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Experience until next level: {0}'.format(player.level.experience_to_next_level))
    tcod.console_print_rect_ex(window, 0, 6, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Maximum HP: {0}'.format(player.combatant.max_hp))
    tcod.console_print_rect_ex(window, 0, 7, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Attack: {0}'.format(player.combatant.attack))
    tcod.console_print_rect_ex(window, 0, 8, mirror_width, mirror_height, tcod.BKGND_NONE,
                                  tcod.LEFT, 'Armour Class: {0}'.format(player.combatant.ac))
    x=screen_width//2-mirror_width//2
    y=screen_height//2-mirror_height//2
    tcod.console_blit(window, 0, 0, mirror_width, mirror_height, 0, x, y, 1.0, 0.7)