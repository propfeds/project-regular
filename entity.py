import tcod
from render_functions import RenderOrder
from components.inventory import Inventory
from components.item import Item
from components.stairs import Stairs

class Entity:
    def __init__(self, x, y, char, colour, name, block_movement=False, render_order=RenderOrder.CORPSE, combatant=None, ai=None, item=None, inventory=None, stairs=None, level=None):
        self.x=x
        self.y=y
        self.char=char
        self.colour=colour
        self.name=name
        self.block_movement=block_movement
        self.render_order=render_order
        # combatant: knows how to fight
        self.combatant=combatant
        self.ai=ai
        # item: is an item
        self.item=item
        self.inventory=inventory
        self.stairs=stairs
        self.level=level

        if self.combatant:
            self.combatant.owner=self
        if self.ai:
            self.ai.owner=self
        if self.item:
            self.item.owner=self
        if self.inventory:
            self.inventory.owner=self
        if self.stairs:
            self.stairs.owner=self
        if self.level:
            self.level.owner=self

    def __str__(self):
        if not self.item:
            return 'This is not an item you\'re talking about.'
        return str(self.item)

    def move(self, dx, dy):
        self.x+=dx
        self.y+=dy

    def distance_to(self, target):
        dx=target.x-self.x
        dy=target.y-self.y
        return max(abs(dx), abs(dy))
    
    def distance_to_point(self, target_x, target_y):
        dx=target_x-self.x
        dy=target_y-self.y
        return max(abs(dx), abs(dy))

    def move_towards(self, target_x, target_y, game_map, entities):
        dx=target_x-self.x
        dy=target_y-self.y
        distance=max(abs(dx), abs(dy))
        dx=int(round(dx/distance))
        dy=int(round(dy/distance))

        if not(game_map.is_blocked(self.x+dx, self.y+dy) or get_blocking_entities(entities, self.x+dx, self.y+dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        fov=tcod.map_new(game_map.width, game_map.height)
        # Walls are impassable of course
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].block_movement)
        for entity in entities:
            if entity.block_movement and entity!=self and entity!=target:
                # Treat allies as transparent but impassable
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)
        # The 1 is diagonal cost, normally would be 1.41, but 
        my_path=tcod.path_new_using_map(fov, 1)
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Low path size so that monsters won't run off in some random lil corridor
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path)<20:
            x, y=tcod.path_walk(my_path, True) # True means to recompute path
            if x or y: # wtf
                self.x=x
                self.y=y
        else: # Backup option if not movable (corridor stuck)
            self.move_towards(target.x, target.y, game_map, entities)
        # Freeing some ram
        tcod.path_delete(my_path)

def get_blocking_entities(entities, x, y):
    for entity in entities:
        if entity.block_movement and entity.x==x and entity.y==y:
            return entity
    return None