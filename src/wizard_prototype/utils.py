type Vec2D = tuple[int, int]

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


def add(a: Vec2D, b: Vec2D) -> Vec2D:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Vec2D, b: Vec2D) -> Vec2D:
    return (a[0] - b[0], a[1] - b[1])
