from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def is_direction(cmd: str) -> bool:
    return len(cmd) == 1 and cmd in "hjkl"


def to_direction(cmd: str) -> Direction:
    match cmd:
        case "h":
            return Direction.LEFT
        case "j":
            return Direction.DOWN
        case "k":
            return Direction.UP
        case "l":
            return Direction.RIGHT
        case _:
            raise ValueError
