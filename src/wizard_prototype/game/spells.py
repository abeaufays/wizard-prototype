import abc

from wizard_prototype import utils


class Spell(abc.ABC):
    @property
    @abc.abstractmethod
    def element(self) -> str: ...

    @property
    @abc.abstractmethod
    def lifetime(self) -> int: ...

    @abc.abstractmethod
    def affected_tiles(self) -> list[utils.Vec2D]: ...

    @abc.abstractmethod
    def update(self) -> None: ...


class Projectile(Spell):
    def __init__(
        self,
        position: utils.Vec2D,
        direction: utils.Vec2D,
        element: str,
    ):
        self.position: utils.Vec2D = position
        self.direction: utils.Vec2D = direction
        self._element: str = element
        self._lifetime: int = 10

    @property
    def lifetime(self) -> int:
        return self._lifetime

    @property
    def element(self) -> str:
        return self._element

    def update(self) -> None:
        self.position = utils.add(self.position, self.direction)
        self._lifetime -= 1

    def affected_tiles(self) -> list[utils.Vec2D]:
        return [self.position]


class Ray(Spell):
    def __init__(
        self,
        starting_position: utils.Vec2D,
        direction: utils.Vec2D,
        element: str,
    ):
        self.starting_position: utils.Vec2D = starting_position
        self.direction: utils.Vec2D = direction
        self.range: int = 5
        self._element: str = element
        self._lifetime: int = 1

    @property
    def lifetime(self) -> int:
        return self._lifetime

    @property
    def element(self) -> str:
        return self._element

    def update(self) -> None:
        self._lifetime -= 1

    def affected_tiles(self) -> list[utils.Vec2D]:
        result = []
        for i in range(1, self.range + 1):
            result.append(
                utils.add(self.starting_position, utils.mult(self.direction, i))
            )
        return result
