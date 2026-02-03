from wizard_prototype.game import spells, wizard


class GameState:
    def __init__(self) -> None:
        self.debug: str = ""
        self.spells: list[spells.Spell] = []
        self.player = wizard.Wizard(position=(5, 5))

    def update(self, cmd: str):
        self.player.handle_input(cmd, self)

    def new_turn(self):
        expired_spells = []

        for spell in self.spells:
            spell.update()
            if spell.lifetime < 0:
                expired_spells.append(spell)

        for expired_spell in expired_spells:
            self.spells.remove(expired_spell)
