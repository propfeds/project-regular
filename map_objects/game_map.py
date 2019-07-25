import tcod as libtcod
from random import randint
from entity import Entity
from map_objects.tile import Tile
from map_objects.rect import Rect
from components.ai import Brute
from components.combatant import Combatant

class GameMap:
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.tiles=self.init_tiles()
    def init_tiles(self):
        # True: walls!
        tiles=[[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):
        rooms=[]
        num_rooms=0
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
            
                self.spawn_entities(new_room, entities, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms+=1
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

    def spawn_entities(self, room, entities, max_monsters_per_room):
        number_of_monsters=randint(0, max_monsters_per_room)
        for _ in range(number_of_monsters):
            x=randint(room.x1+1, room.x2-1)
            y=randint(room.y1+1, room.y2-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                # Ninety percent to spawn a white european, ten percent to spawn a green orck
                if randint(0, 100)<90:
                    monster=Entity(x, y, 'm', libtcod.white, 'Man', block_movement=True, combatant=Combatant(health=15, stamina=40, attack=3, ac=1), ai=Brute())
                else:
                    monster=Entity(x, y, 'o', libtcod.desaturated_green, 'Orck', block_movement=True, combatant=Combatant(health=50, stamina=50, attack=7, ac=3), ai=Brute())
                entities.append(monster)