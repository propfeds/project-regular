import tcod as libtcod
from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity=capacity
        self.contents=[]

    def add_item(self, item):
        results=[]
        if len(self.contents)>=self.capacity:
            results.append({'item_added': None, 'message': Message('Your inventory is full.', libtcod.yellow)})
        else:
            results.append({'item_added': item, 'message': Message('You pick up the {0}.'.format(item.name), libtcod.lighter_blue)})
            self.contents.append(item)
        return results