from __future__ import annotations

import abc

from wizard_prototype import utils
from wizard_prototype.game import state, wizard


class Spell(abc.ABC):
    def __init__(self, caster: wizard.Wizard):
        self.caster: wizard.Wizard = caster

    def assign_form(self, form: Form):
        self.form = form

    def assign_direction(self, direction: utils.Vec2D):
        self.direction = direction

    @abc.abstractmethod
    def next_state(self) -> wizard.SpellCastingState | None: ...

    @abc.abstractmethod
    def effect(self, game_state: state.GameState): ...


class Element(Spell):
    def __init__(self, caster: wizard.Wizard, element: str) -> None:
        super().__init__(caster)
        self.element = element
        self._required_states = [
            wizard.FormPending(self.caster, self),
            wizard.DirectionPending(self.caster, self),
        ]

    def assign_direction(self, direction: utils.Vec2D) -> bool:
        assert self.form
        if not self.form.needs_direction():
            raise ValueError
        self.direction = direction

    def next_state(self) -> wizard.SpellCastingState | None:
        if self._required_states:
            return self._required_states.pop(0)
        else:
            return None

    def effect(self, game_state: state.GameState) -> None:
        assert self.form
        game_state.tangible_spells.append(self.form)


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

    def display(self) -> str:
        return self.spell.element


class ProjectileForm(Form):
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


class RayForm(Form):
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
