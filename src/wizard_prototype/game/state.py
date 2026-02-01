from dataclasses import dataclass

from wizard_prototype import utils
from wizard_prototype.game import wizard

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


@dataclass
class Projectile:
    position: utils.Vec2D
    direction: utils.Vec2D
    lifetime: int = 10

    def update(self):
        self.position = utils.add(self.position, self.direction)
        self.lifetime -= 1


class GameState:
    def __init__(self) -> None:
        self.debug: str = ""
        self.spell_casting_mode: bool = False
        self.spell_buffer: str = ""
        self.player_direction: utils.Vec2D = UP
        self.projectiles: list[Projectile] = []
        self.player = wizard.Wizard(position=(5, 5), direction=UP)

    def update(self, cmd: str):
        if self.spell_casting_mode:
            match cmd:
                case "f":
                    self.projectiles.append(
                        Projectile(
                            position=utils.add(
                                self.player.position, self.player.direction
                            ),
                            direction=self.player.direction,
                        )
                    )
                    self.spell_casting_mode = False
                    self.new_turn()
                case " ":
                    self.spell_casting_mode = False
                case default:
                    self.debug = default

        else:
            match cmd:
                # Moves
                case "h":
                    self.player.position = utils.add(self.player.position, LEFT)
                    self.player.direction = LEFT
                    self.new_turn()
                case "j":
                    self.player.position = utils.add(self.player.position, DOWN)
                    self.player.direction = DOWN
                    self.new_turn()
                case "k":
                    self.player.position = utils.add(self.player.position, UP)
                    self.player.direction = UP
                    self.new_turn()
                case "l":
                    self.player.position = utils.add(self.player.position, RIGHT)
                    self.player.direction = RIGHT
                    self.new_turn()
                # Turn around
                case "H":
                    self.player.direction = LEFT
                case "J":
                    self.player.direction = DOWN
                case "K":
                    self.player.direction = UP
                case "L":
                    self.player.direction = RIGHT
                # Spells
                case " ":
                    self.spell_casting_mode = True
                case default:
                    self.debug = default

    def new_turn(self):
        to_remove = []

        for projectile in self.projectiles:
            projectile.update()
            if projectile.lifetime < 0:
                to_remove.append(projectile)

        for projectile_to_remove in to_remove:
            self.projectiles.remove(projectile_to_remove)
