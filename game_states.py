from enum import Enum

class GameStates(Enum):
    PLAYER_DEAD=0
    PLAYER_TURN=1
    ENEMY_TURN=2
    TARGETING=4
    INVENTORY=5
    DROP_INVENTORY=6