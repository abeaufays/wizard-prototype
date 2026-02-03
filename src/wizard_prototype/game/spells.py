import abc

from wizard_prototype import utils


class Spell(abc.ABC):
    @property
    @abc.abstractmethod
    def base(self) -> str: ...

    @property
    @abc.abstractmethod
    def lifetime(self) -> int: ...

    @abc.abstractmethod
    def affected_tiles(self) -> list[utils.Vec2D]: ...

    @abc.abstractmethod
    def update(self) -> None: ...

    @abc.abstractmethod
    def give_direction(self, direction: utils.Vec2D): ...


class Projectile(Spell):
    def __init__(
        self,
        starting_position: utils.Vec2D,
        base: str,
    ):
        self.position: utils.Vec2D = starting_position
        self.direction: utils.Vec2D | None = None
        self._base: str = base
        self._lifetime: int = 10

    @property
    def lifetime(self) -> int:
        return self._lifetime

    @property
    def base(self) -> str:
        return self._base

    def update(self) -> None:
        assert self.direction
        self.position = utils.add(self.position, self.direction)
        self._lifetime -= 1

    def affected_tiles(self) -> list[utils.Vec2D]:
        return [self.position]

    def give_direction(self, direction: utils.Vec2D):
        self.direction = direction


class Ray(Spell):
    def __init__(
        self,
        starting_position: utils.Vec2D,
        base: str,
    ):
        self.starting_position: utils.Vec2D = starting_position
        self.direction: utils.Vec2D | None = None
        self.range: int = 5
        self._base: str = base
        self._lifetime: int = 1

    @property
    def lifetime(self) -> int:
        return self._lifetime

    @property
    def base(self) -> str:
        return self._base

    def update(self) -> None:
        self._lifetime -= 1

    def affected_tiles(self) -> list[utils.Vec2D]:
        assert self.direction
        result = []
        for i in range(1, self.range + 1):
            result.append(
                utils.add(self.starting_position, utils.mult(self.direction, i))
            )
        return result

    def give_direction(self, direction: utils.Vec2D):
        self.direction = direction
