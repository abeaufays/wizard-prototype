from typing import TYPE_CHECKING

from wizard_prototype.game import wizard

if TYPE_CHECKING:
    from wizard_prototype.game.spells import casting


class GameState:
    def __init__(self) -> None:
        self.tangible_spells: list[casting.Form] = []
        self.player = wizard.Wizard(position=(5, 5))

    def update(self, cmd: str):
        self.player.handle_input(cmd, self)

    def new_turn(self):
        expired_spells = []

        for form in self.tangible_spells:
            form.update()
            if form.lifetime() < 0:
                expired_spells.append(form)

        for expired_spell in expired_spells:
            self.tangible_spells.remove(expired_spell)
