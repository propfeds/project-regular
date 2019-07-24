from map_objects.tile import Tile
from map_objects.rect import Rect

class GameMap:
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.tiles=self.init_tiles()

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_movement:
            return True
        return False

    def init_tiles(self):
        # True: walls!
        tiles=[[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

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