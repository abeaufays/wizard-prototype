from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from wizard_prototype import utils
from wizard_prototype.game import direction as direction_utils
from wizard_prototype.game import spells

if TYPE_CHECKING:
    from wizard_prototype.game import state


class SpellCastingState(abc.ABC):
    def __init__(self, wizard: Wizard) -> None:
        self.wizard = wizard

    @abc.abstractmethod
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        """
        Decide what to do depending on player input and current current

        Returns True if the action triggers a new turn
        """

    def fail_spell(self) -> None:
        self.wizard.life -= 1

    def switch_state(self, spell: spells.Spell, game_state: state.GameState) -> bool:
        """
        Switch to the input spells next state, and handle side effects

        Returns True if the system should trigger a new turn
        """
        new_state = spell.next_state()
        if new_state is None:
            new_state = Normal(self.wizard)
            spell.effect(game_state)
            self.wizard.current_state = new_state
            return True

        self.wizard.current_state = new_state
        return False


class Normal(SpellCastingState):
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        if direction_utils.is_direction(cmd):
            direction = direction_utils.to_direction(cmd)
            self.wizard.position = utils.add(self.wizard.position, direction.value)
            return True
        else:
            match cmd:
                case "f":
                    spell: spells.Spell = spells.Element(
                        caster=self.wizard, element="󰈸"
                    )
                case "i":
                    spell: spells.Spell = spells.Element(
                        caster=self.wizard, element="󰜗"
                    )
                case "a":
                    spell: spells.Spell = spells.Element(
                        caster=self.wizard, element=""
                    )
                # Ignore other inputs
                case _:
                    return False

            return self.switch_state(spell, game_state)
        return False


class FormPending(SpellCastingState):
    def __init__(self, wizard: Wizard, current_spell: spells.Spell) -> None:
        super().__init__(wizard)
        self.current_spell = current_spell

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            # Cancel spell
            case " ":
                self.wizard.current_state = Normal(self.wizard)
                return True

            case "b":
                form = spells.ProjectileForm(
                    spell=self.current_spell,
                    casted_from=self.wizard.position,
                )
            case "r":
                form = spells.RayForm(
                    spell=self.current_spell,
                    casted_from=self.wizard.position,
                )

            # Fail spell
            case _:
                self.fail_spell()
                self.wizard.current_state = Normal(self.wizard)
                return True

        self.current_spell.assign_form(form)
        return self.switch_state(self.current_spell, game_state)

        return False


class DirectionPending(SpellCastingState):
    def __init__(self, wizard: Wizard, current_spell: spells.Spell) -> None:
        self.wizard: Wizard = wizard
        self.current_spell: spells.Spell = current_spell

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        if direction_utils.is_direction(cmd):
            direction = direction_utils.to_direction(cmd).value
            self.current_spell.assign_direction(direction)

            return self.switch_state(self.current_spell, game_state)
        else:
            # Cancelled and failed spells
            match cmd:
                case " ":
                    self.wizard.current_state = Normal(self.wizard)
                case _:
                    self.fail_spell()
                    self.wizard.current_state = Normal(self.wizard)
                    return True
        return False


class Wizard:
    def __init__(self, position: utils.Vec2D) -> None:
        self.position: utils.Vec2D = position
        self.current_state: SpellCastingState = Normal(self)
        self.life = 10

    def handle_input(
        self,
        cmd: str,
        game_state: state.GameState,
    ) -> None:
        if self.current_state.handle_input(cmd, game_state):
            game_state.new_turn()
