type Vec2D = tuple[int, int]


def add(a: Vec2D, b: Vec2D) -> Vec2D:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Vec2D, b: Vec2D) -> Vec2D:
    return (a[0] - b[0], a[1] - b[1])


def mult(a: Vec2D, x: int) -> Vec2D:
    return (a[0] * x, a[1] * x)
