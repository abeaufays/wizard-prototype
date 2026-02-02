from __future__ import annotations

import abc

from wizard_prototype import utils
from wizard_prototype.game import spells, state


class WizardState(abc.ABC):
    def __init__(self, wizard) -> None:
        self.wizard = wizard

    @abc.abstractmethod
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        """
        Decide what to do depending on player input and current current

        Returns True if the action triggers a new turn
        """

    def fail_spell(self) -> None:
        self.wizard.life -= 1


class Normal(WizardState):
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = ElementPending(self.wizard)
            # Moves
            case "h":
                self.wizard.position = utils.add(self.wizard.position, utils.LEFT)
                self.wizard.direction = utils.LEFT
                return True
            case "j":
                self.wizard.position = utils.add(self.wizard.position, utils.DOWN)
                self.wizard.direction = utils.DOWN
                return True
            case "k":
                self.wizard.position = utils.add(self.wizard.position, utils.UP)
                self.wizard.direction = utils.UP
                return True
            case "l":
                self.wizard.position = utils.add(self.wizard.position, utils.RIGHT)
                self.wizard.direction = utils.RIGHT
                return True
            # Turn around
            case "H":
                self.wizard.direction = utils.LEFT
            case "J":
                self.wizard.direction = utils.DOWN
            case "K":
                self.wizard.direction = utils.UP
            case "L":
                self.wizard.direction = utils.RIGHT
        return False


class ElementPending(WizardState):
    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = Normal(self.wizard)
            case "f":
                self.wizard.current_state = FormPending(self.wizard, "󰈸")
            case _:
                self.fail_spell()
                return True
        return False


class FormPending(WizardState):
    def __init__(self, wizard: Wizard, element: str) -> None:
        super().__init__(wizard)
        self.element = element

    def handle_input(self, cmd: str, game_state: state.GameState) -> bool:
        match cmd:
            case " ":
                self.wizard.current_state = Normal(self.wizard)
            case "b":
                game_state.spells.append(
                    spells.Projectile(
                        position=utils.add(self.wizard.position, self.wizard.direction),
                        direction=self.wizard.direction,
                        element=self.element,
                    )
                )
                self.wizard.current_state = Normal(self.wizard)
                return True
            case _:
                self.fail_spell()
                return True
        return False


class Wizard:
    def __init__(self, position: utils.Vec2D, direction: utils.Vec2D) -> None:
        self.position: utils.Vec2D = position
        self.direction: utils.Vec2D = direction
        self.current_state: WizardState = Normal(self)

    def handle_input(
        self,
        cmd: str,
        game_state: state.GameState,
    ) -> None:
        if self.current_state.handle_input(cmd, game_state):
            game_state.new_turn()
