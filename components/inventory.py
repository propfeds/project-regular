#pylint: disable=no-member
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

    def use_item(self, item_entity, **kwargs):
        results=[]
        if item_entity.item.use_function is None:
            results.append({'message': Message('You don\'t see a way to use the {0}.'.format(item_entity.name), libtcod.yellow)})
        kwargs={**item_entity.item.function_kwargs, **kwargs}
        item_use_results=item_entity.item.use_function(self.owner, **kwargs)
        for result in item_use_results:
            if result.get('consumed'):
                self.remove_item(item_entity)
        results.extend(item_use_results)
        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results=[]
        item.x=self.owner.x
        item.y=self.owner.y
        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You drop the {0}.'.format(item.name), libtcod.lighter_blue)})
        return results
