import tcod
from random import randint
from random_utils import random_choice_from_dict, from_dungeon_level
from entity import Entity
from map_objects.tile import Tile
from map_objects.rect import Rect
from components.ai import Brute
from components.combatant import Combatant
from components.item import Item
from components.stairs import Stairs
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from render_functions import RenderOrder
from item_functions import heal, dorkbolt, dorkblast, confusodockulus
from game_messages import Message

class GameMap:
    def __init__(self, width, height, depth=1):
        self.width=width
        self.height=height
        self.depth=depth
        self.tiles=self.init_tiles()

    def init_tiles(self):
        # True: walls!
        tiles=[[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,):
        rooms=[]
        num_rooms=0

        last_room_c=(None, None)

        for _ in range(max_rooms):
            w= randint(room_min_size, room_max_size)
            h= randint(room_min_size, room_max_size)
            x= randint(0, map_width-w-1)
            y= randint(0, map_height-h-1)
            new_room=Rect(x, y, w, h)
            for ref_room in rooms:
                if new_room.intersect(ref_room):
                    break
            # weird python syntax stuff
            else:
                self.carve_room(new_room)
            
                (new_x, new_y)=new_room.centre()

                last_room_c=(new_x, new_y)

                if num_rooms==0:
                    player.x=new_x
                    player.y=new_y
                else:
                    # tunnel to SPECIFICALLY THE PREVIOUS ROOM, imitating the chaotic nature of dcss
                    (prev_x, prev_y)=rooms[num_rooms-1].centre()
                    if randint(0, 1)==0:
                        self.carve_tunnel_x(prev_x, new_x, prev_y)
                        self.carve_tunnel_y(prev_y, new_y, new_x)
                    else:
                        self.carve_tunnel_y(prev_y, new_y, prev_x)
                        self.carve_tunnel_x(prev_x, new_x, new_y)
            
                self.spawn_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms+=1
        stairs_x, stairs_y=last_room_c
        entities.append(Entity(stairs_x, stairs_y, '>', tcod.white, 'Stairs', render_order=RenderOrder.CORPSE, stairs=Stairs(self.depth+1)))
    def carve_room(self, room):
        for y in range(room.y1+1, room.y2):
            for x in range (room.x1+1, room.x2):
                self.tiles[x][y].block_movement=False
                self.tiles[x][y].block_sight=False
    def carve_tunnel_x(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.tiles[x][y].block_movement=False
            self.tiles[x][y].block_sight=False
    def carve_tunnel_y(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.tiles[x][y].block_movement=False
            self.tiles[x][y].block_sight=False
    def is_blocked(self, x, y):
        if self.tiles[x][y].block_movement:
            return True
        return False

    def spawn_entities(self, room, entities):
        # spawning some baddies
        max_monsters_per_room=from_dungeon_level([(2, 1), (3, 4), (5, 6)], self.depth)
        number_of_monsters=randint(0, max_monsters_per_room)
        monster_chances={
            'man': 72,
            'orckh': from_dungeon_level([(15, 3), (30, 5), (60, 7)], self.depth)
        }
        for _ in range(number_of_monsters):
            x=randint(room.x1+1, room.x2-1)
            y=randint(room.y1+1, room.y2-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                monster_choice=random_choice_from_dict(monster_chances)
                if monster_choice=='man':
                    monster=Entity(x, y, 'm', tcod.white, 'Man', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=15, stamina=40, attack=4, ac=1, xp=100), ai=Brute())
                else:
                    monster=Entity(x, y, 'o', tcod.desaturated_green, 'Orckh', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=50, stamina=50, attack=7, ac=2, xp=150), ai=Brute())
                entities.append(monster)
        # spawning some items
        max_items_per_room=from_dungeon_level([(1, 1), (2, 4)], self.depth)
        number_of_items=randint(0, max_items_per_room)
        item_chances={
            'pot_juju': 24,
            'scroll_confuse': from_dungeon_level([(24, 4)], self.depth),
            'scroll_dorkbolt': from_dungeon_level([(32, 2)], self.depth),
            'scroll_dorkblast': from_dungeon_level([(16, 5)], self.depth),
            'axe': from_dungeon_level([(15, 1)], self.depth),
            'shield': from_dungeon_level([(12, 1)], self.depth),
            'ring': from_dungeon_level([(3, 1)], self.depth)
        }
        for _ in range(number_of_items):
            x=randint(room.x1+1, room.x2-1)
            y=randint(room.y1+1, room.y2-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                item_choice=random_choice_from_dict(item_chances)
                if item_choice=='scroll_confuse':
                    item=Entity(x, y, '#', tcod.light_pink, 'Scroll of Confusodockulus', render_order=RenderOrder.ITEM, item=Item(use_function=confusodockulus, targeting=True, targeting_message=Message('Left-click an enemy to confuse it, or right-click to cancel.', tcod.light_cyan)))
                elif item_choice=='pot_juju':
                    item=Entity(x, y, '!', tcod.violet, 'Rejujuvenation Potion', render_order=RenderOrder.ITEM, item=Item(use_function=heal, amount=6))
                elif item_choice=='scroll_dorkbolt':
                    item=Entity(x, y, '#', tcod.yellow, 'Scroll of Dorkbolt', render_order=RenderOrder.ITEM, item=Item(use_function=dorkbolt, damage=23, maximum_range=11))
                elif item_choice=='scroll_dorkblast':
                    item=Entity(x, y, '#', tcod.orange, 'Scroll of Dorkblast', render_order=RenderOrder.ITEM, item=Item(use_function=dorkblast, targeting=True, targeting_message=Message('Use your mouse to fire because facepalm.', tcod.lighter_blue), damage=17, radius=2))
                elif item_choice=='axe':
                    item=Entity(x, y, '/', tcod.sky, 'Scale Axe +{0}'.format(self.depth), render_order=RenderOrder.ITEM, equippable=Equippable(EquipmentSlots.MAIN_HAND, bonus_attack=1+self.depth*2))
                elif item_choice=='shield':
                    item=Entity(x, y, '[', tcod.darker_orange, 'Scale Shield +{0}'.format(self.depth), render_order=RenderOrder.ITEM, equippable=Equippable(EquipmentSlots.OFF_HAND, bonus_ac=-1+self.depth))
                elif item_choice=='ring':
                    item=Entity(x, y, '=', tcod.amber, 'Ring of Bonding +{0}'.format(self.depth), render_order=RenderOrder.ITEM, equippable=Equippable(EquipmentSlots.FINGER, bonus_max_hp=7+self.depth*13))
                entities.append(item)

    def next_floor(self, player, message_log, constants):
        self.depth+=1
        entities=[player]

        self.tiles=self.init_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)

        player.combatant.take_damage(-player.combatant.health//2)
        message_log.add_message(Message('You feed on the ground.', tcod.light_violet))

        return entities