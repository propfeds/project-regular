import tcod
from random import randint
from entity import Entity
from map_objects.tile import Tile
from map_objects.rect import Rect
from components.ai import Brute
from components.combatant import Combatant
from components.item import Item
from components.stairs import Stairs
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
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
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
            
                self.spawn_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
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

    def spawn_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # spawning some baddies
        number_of_monsters=randint(0, max_monsters_per_room)
        for _ in range(number_of_monsters):
            x=randint(room.x1+1, room.x2-1)
            y=randint(room.y1+1, room.y2-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                # Ninety percent to spawn a white european, ten percent to spawn a green orck
                if randint(0, 100)<90:
                    monster=Entity(x, y, 'm', tcod.white, 'Man', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=15, stamina=40, attack=3, ac=1, xp=100), ai=Brute())
                else:
                    monster=Entity(x, y, 'o', tcod.desaturated_green, 'Orckh', block_movement=True, render_order=RenderOrder.ACTOR, combatant=Combatant(health=50, stamina=50, attack=7, ac=2, xp=150), ai=Brute())
                entities.append(monster)
        # spawning some items
        number_of_items=randint(0, max_items_per_room)
        for _ in range(number_of_items):
            x=randint(room.x1+1, room.x2-1)
            y=randint(room.y1+1, room.y2-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                item_roll=randint(0, 99)
                if item_roll<20:
                    item=Entity(x, y, '#', tcod.light_pink, 'Scroll of Confusodockulus', render_order=RenderOrder.ITEM, item=Item(use_function=confusodockulus, targeting=True, targeting_message=Message('Left-click an enemy to confuse it, or right-click to cancel.', tcod.light_cyan)))
                elif item_roll<44:
                    item=Entity(x, y, '!', tcod.violet, 'Rejujuvenation Potion', render_order=RenderOrder.ITEM, item=Item(use_function=heal, amount=7))
                elif item_roll<72:
                    item=Entity(x, y, '#', tcod.yellow, 'Scroll of Dorkbolt', render_order=RenderOrder.ITEM, item=Item(use_function=dorkbolt, damage=27, maximum_range=11))
                else:
                    item=Entity(x, y, '#', tcod.orange, 'Scroll of Dorkblast', render_order=RenderOrder.ITEM, item=Item(use_function=dorkblast, targeting=True, targeting_message=Message('Use your mouse to fire because facepalm.', tcod.lighter_blue), damage=21, radius=2))
                entities.append(item)

    def next_floor(self, player, message_log, constants):
        self.depth+=1
        entities=[player]

        self.tiles=self.init_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])

        player.combatant.take_damage(-player.combatant.health//2)
        message_log.add_message(Message('You feed on the ground.', tcod.light_violet))

        return entities