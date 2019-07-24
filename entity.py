class Entity:
    def __init__(self, x, y, char, colour, name, block_movement=False):
        self.x=x
        self.y=y
        self.char=char
        self.colour=colour
        self.name=name
        self.block_movement=block_movement

    def move(self, dx, dy):
        self.x+=dx
        self.y+=dy

def get_blocking_entities(entities, x, y):
    for entity in entities:
        if entity.block_movement and entity.x==x and entity.y==y:
            return entity
    return None