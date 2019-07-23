class Tile:
    def __init__(self, block_movement, block_sight=None):
        self.block_movement=block_movement
        if block_sight is None:
            block_sight=block_movement
        self.block_sight=block_sight
        # Independent, since I may wanna add stuff like glass walls

