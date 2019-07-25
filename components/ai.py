import tcod as libtcod

class Brute:
    def take_turn(self, target, fov_map, game_map, entities):
        # pylint: disable=no-member
        # Fuck off seriously
        monster=self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target)>=2:
                monster.move_astar(target, entities, game_map)
            elif target.combatant.health>0:
                monster.combatant.attack(target)