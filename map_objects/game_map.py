from map_objects.tile import Tile

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
        # False = doesn't block (floor n stuff)
        tiles=[[Tile(False) for y in range(self.height)] for x in range(self.width)]
        tiles[0][0].block_movement=True
        tiles[0][0].block_sight=True
        tiles[1][1].block_movement=True
        tiles[1][1].block_sight=True
        tiles[2][2].block_movement=True
        tiles[2][2].block_sight=True
        tiles[2][0].block_movement=True
        tiles[2][0].block_sight=True
        tiles[0][2].block_movement=True
        tiles[0][2].block_sight=True
        # D
        tiles[4][0].block_movement=True
        tiles[4][0].block_sight=True
        tiles[5][0].block_movement=True
        tiles[5][0].block_sight=True
        tiles[4][1].block_movement=True
        tiles[4][1].block_sight=True
        tiles[6][1].block_movement=True
        tiles[6][1].block_sight=True
        tiles[4][2].block_movement=True
        tiles[4][2].block_sight=True
        tiles[5][2].block_movement=True
        tiles[5][2].block_sight=True
        tiles[6][2].block_movement=True
        tiles[6][2].block_sight=True

        return tiles
