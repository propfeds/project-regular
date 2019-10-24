#pylint: disable=no-member
import tcod as libtcod
from random import randint
from game_messages import Message

class Brute:
    def take_turn(self, target, fov_map, game_map, entities):
        results=[]
        monster=self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target)>=2:
                monster.move_astar(target, entities, game_map)
            elif target.combatant.health>0:
                results.extend(monster.combatant.attack_physical(target))
        return results

class ConfusedLad:
    def __init__(self, prev_ai, nof_turns=5):
        self.prev_ai=prev_ai
        self.nof_turns=nof_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results=[]
        if self.nof_turns:
            dx=self.owner.x+randint(-1, 1)
            dy=self.owner.y+randint(-1, 1)
            if dx!=self.owner.x and dy!=self.owner.y:
                self.owner.move_towards(dx, dy, game_map, entities)
            self.nof_turns-=1
        else:
            self.owner.ai=self.prev_ai
            results.append({'message': Message('The {0} regains self-control.'.format(self.owner.name), libtcod.red)})
        return results