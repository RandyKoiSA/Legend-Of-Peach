import pygame
from custom.text import Text
from custom.button import Button

class HudScreen:
    """ HUD screen showing data such as points and lives """
    def __init__(self, hub):
        self.hub = hub
        self.screen = hub.main_screen
        self.gamemode = hub.gamemode

        self.score_text = Text(self.screen, str(self.gamemode.score))
        self.score_rect = self.score_text.get_rect()
        self.prep_score_text()

        self.lives_text = Text(self.screen, str(self.gamemode.lives))
        self.lives_rect = self.lives_text.get_rect()
        self.prep_lives_text()

    def run(self):
        self.run_event()
        self.run_update()
        self.run_draw()

    def prep_score_text(self):
        pass

    def prep_lives_text(self):
        pass

    def run_event(self):
        pass

    def run_update(self):
        pass

    def run_draw(self):
        pass

