import pygame
from custom.text import Text
from custom.button import Button

class HudScreen:
    """ HUD screen showing data such as points and lives """
    def __init__(self, hub):
        self.hub = hub
        self.screen = hub.main_screen
        self.gamemode = hub.gamemode

        self.score_text = Text(self.screen, str())

