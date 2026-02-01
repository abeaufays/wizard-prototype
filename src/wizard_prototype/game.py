from dataclasses import dataclass

from wizard_prototype import utils

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


@dataclass
class GameState:
    player_position: utils.Vec2D

    def __init__(self):
        self.player_position = (10, 10)
        self.player_direction = UP

    def update(self, cmd: str):
        match cmd:
            case "h":
                self.player_position = utils.add(self.player_position, LEFT)
            case "j":
                self.player_position = utils.add(self.player_position, DOWN)
            case "k":
                self.player_position = utils.add(self.player_position, UP)
            case "l":
                self.player_position = utils.add(self.player_position, RIGHT)
