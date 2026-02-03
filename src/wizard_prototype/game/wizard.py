from __future__ import annotations

import abc

from wizard_prototype import utils
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
        match cmd:
            case " ":
                self.wizard.current_state = BasePending(self.wizard)
            # Moves
            case "h":
                self.wizard.position = utils.add(self.wizard.position, utils.LEFT)
                return True
            case "j":
                self.wizard.position = utils.add(self.wizard.position, utils.DOWN)
                return True
            case "k":
                self.wizard.position = utils.add(self.wizard.position, utils.UP)
                return True
            case "l":
                self.wizard.position = utils.add(self.wizard.position, utils.RIGHT)
                return True
        return False


class BasePending(SpellCastingState):
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = Normal(self.wizard)
            case "f":
                self.wizard.current_state = FormPending(self.wizard, "󰈸")
            case "i":
                self.wizard.current_state = FormPending(self.wizard, "󰜗")
            case "a":
                self.wizard.current_state = FormPending(self.wizard, "")
            case _:
                self.wizard.current_state = Normal(self.wizard)
                self.fail_spell()
                return True
        return False


class FormPending(SpellCastingState):
    def __init__(self, wizard: Wizard, base: str) -> None:
        super().__init__(wizard)
        self.base = base

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = Normal(self.wizard)
            case "b":
                self.wizard.current_state = DirectionPending(
                    self.wizard,
                    spells.Projectile(
                        starting_position=self.wizard.position,
                        base=self.base,
                    ),
                )
            case "r":
                self.wizard.current_state = DirectionPending(
                    self.wizard,
                    spells.Ray(
                        starting_position=self.wizard.position,
                        base=self.base,
                    ),
                )
            case _:
                self.fail_spell()
                self.wizard.current_state = Normal(self.wizard)
                return True
        return False


class DirectionPending(SpellCastingState):
    def __init__(self, wizard: Wizard, spell: spells.Spell) -> None:
        self.wizard: Wizard = wizard
        self.spell: spells.Spell = spell

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = BasePending(self.wizard)
            case "h":
                self.spell.give_direction(utils.LEFT)
                game_state.spells.append(self.spell)
                self.wizard.current_state = Normal(self.wizard)
                return True
            case "j":
                self.spell.give_direction(utils.DOWN)
                game_state.spells.append(self.spell)
                self.wizard.current_state = Normal(self.wizard)
                return True
            case "k":
                self.spell.give_direction(utils.UP)
                game_state.spells.append(self.spell)
                self.wizard.current_state = Normal(self.wizard)
                return True
            case "l":
                self.spell.give_direction(utils.RIGHT)
                game_state.spells.append(self.spell)
                self.wizard.current_state = Normal(self.wizard)
                return True
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
