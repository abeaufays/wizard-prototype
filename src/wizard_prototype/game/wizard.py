from __future__ import annotations

import abc

from wizard_prototype import utils
from wizard_prototype.game import direction as direction_utils
from wizard_prototype.game import spells, state


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


class Normal(SpellCastingState):
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        if direction_utils.is_direction(cmd):
            direction = direction_utils.to_direction(cmd)
            self.wizard.position = utils.add(self.wizard.position, direction.value)
            return True
        else:
            match cmd:
                case "f":
                    self.wizard.current_state = FormPending(
                        self.wizard, spells.Spell(base=spells.Element("󰈸"))
                    )
                case "i":
                    self.wizard.current_state = FormPending(
                        self.wizard, spells.Spell(base=spells.Element("󰜗"))
                    )
                case "a":
                    self.wizard.current_state = FormPending(
                        self.wizard, spells.Spell(base=spells.Element(""))
                    )
        return False


class FormPending(SpellCastingState):
    def __init__(self, wizard: Wizard, current_spell: spells.Spell) -> None:
        super().__init__(wizard)
        self.current_spell = current_spell

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = Normal(self.wizard)
            case "b":
                self.current_spell.form = spells.Projectile(
                    spell=self.current_spell,
                    casted_from=self.wizard.position,
                )
                self.wizard.current_state = DirectionPending(
                    self.wizard,
                    self.current_spell,
                )
            case "r":
                self.current_spell.form = spells.Ray(
                    spell=self.current_spell,
                    casted_from=self.wizard.position,
                )
                self.wizard.current_state = DirectionPending(
                    self.wizard,
                    self.current_spell,
                )
            case _:
                self.fail_spell()
                self.wizard.current_state = Normal(self.wizard)
                return True
        return False


class DirectionPending(SpellCastingState):
    def __init__(self, wizard: Wizard, current_spell: spells.Spell) -> None:
        self.wizard: Wizard = wizard
        self.current_spell: spells.Spell = current_spell

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        if direction_utils.is_direction(cmd):
            direction = direction_utils.to_direction(cmd).value
            self.current_spell.direction = direction

            game_state.spells.append(self.current_spell)
            self.wizard.current_state = Normal(self.wizard)

            return True
        else:
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
