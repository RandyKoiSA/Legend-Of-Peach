import pygame
import sys
from pygame.locals import *
from custom.text import Text
from custom.button import Button
from screens.game_screen import GameScreen

class MainMenuScreen:
    """ Main Menu Screen showing exit button and play button """
    def __init__(self, hub):
        """ Initialize all the default values for MainMenuScreen """
        self.hub = hub
        self.screen = hub.main_screen

        # Title text

        # Play button

        # Exit button

