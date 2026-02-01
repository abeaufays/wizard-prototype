from dataclasses import dataclass, field

from wizard_prototype import utils

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


@dataclass
class Projectile:
    position: utils.Vec2D
    direction: utils.Vec2D

    def update(self):
        self.position = utils.add(self.position, self.direction)


@dataclass
class GameState:
    player_position: utils.Vec2D = (10, 10)
    player_direction = UP
    projectiles: list[Projectile] = field(default_factory=list)

    def update(self, cmd: str):
        match cmd:
            # Moves
            case "h":
                self.player_position = utils.add(self.player_position, LEFT)
                self.player_direction = LEFT
                self.new_turn()
            case "j":
                self.player_position = utils.add(self.player_position, DOWN)
                self.player_direction = DOWN
                self.new_turn()
            case "k":
                self.player_position = utils.add(self.player_position, UP)
                self.player_direction = UP
                self.new_turn()
            case "l":
                self.player_position = utils.add(self.player_position, RIGHT)
                self.player_direction = RIGHT
                self.new_turn()
            # Turn around
            case "H":
                self.player_direction = LEFT
            case "J":
                self.player_direction = DOWN
            case "K":
                self.player_direction = UP
            case "L":
                self.player_direction = RIGHT
            # Spells
            case "f":
                self.projectiles.append(
                    Projectile(
                        position=utils.add(self.player_position, self.player_direction),
                        direction=self.player_direction,
                    )
                )
                self.new_turn()

    def new_turn(self):
        for projectile in self.projectiles:
            projectile.update()
