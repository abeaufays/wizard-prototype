from dataclasses import dataclass

from wizard_prototype import utils


@dataclass
class Wizard:
    position: utils.Vec2D
    direction: utils.Vec2D
