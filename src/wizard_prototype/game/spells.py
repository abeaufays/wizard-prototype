from __future__ import annotations

import abc
from dataclasses import dataclass

from wizard_prototype import utils


class Base(abc.ABC):
    @abc.abstractmethod
    def needs_direction(self) -> bool: ...

    @abc.abstractmethod
    def needs_form(self) -> bool: ...


class Element(Base):
    def __init__(self, element: str) -> None:
        self.element = element

    def needs_direction(self) -> bool:
        return True

    def needs_form(self) -> bool:
        return True


class Form(abc.ABC):
    def __init__(self, spell: Spell) -> None:
        self.spell = spell

    @abc.abstractmethod
    def needs_direction(self) -> bool: ...

    @abc.abstractmethod
    def lifetime(self) -> int: ...

    @abc.abstractmethod
    def affected_tiles(self) -> list[utils.Vec2D]: ...

    @abc.abstractmethod
    def update(self) -> None: ...


class Projectile(Form):
    def __init__(self, spell: Spell, casted_from: utils.Vec2D) -> None:
        super().__init__(spell)
        self.casted_from = casted_from
        self.position = casted_from
        self._lifetime = 10

    def needs_direction(self) -> bool:
        return True

    def lifetime(self) -> int:
        return self._lifetime

    def affected_tiles(self) -> list[utils.Vec2D]:
        return [self.position]

    def update(self) -> None:
        assert self.spell.direction
        self.position = utils.add(self.position, self.spell.direction)
        self._lifetime -= 1


class Ray(Form):
    def __init__(self, spell: Spell, casted_from: utils.Vec2D) -> None:
        super().__init__(spell)
        self.casted_from = casted_from
        self.range = 5
        self._lifetime = 1

    def needs_direction(self) -> bool:
        return True

    def lifetime(self) -> int:
        return self._lifetime

    def affected_tiles(self) -> list[utils.Vec2D]:
        assert self.spell.direction
        result = []
        for i in range(1, self.range + 1):
            result.append(
                utils.add(self.casted_from, utils.mult(self.spell.direction, i))
            )
        return result

    def update(self) -> None:
        self._lifetime -= 1


@dataclass
class Spell:
    base: Base
    direction: utils.Vec2D | None = None
    form: Form | None = None
