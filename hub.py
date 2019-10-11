import pygame
from screens.game_screen import GameScreen
from controller import Controller
from camera import Camera

class Hub:
    """ Hub class, provides a central module to hold all the propertie that are constantly being accessed """

    def __init__(self):
        """ Initialize default values """
        self.CLOCK = pygame.time.Clock()
        self.WINDOW_WIDTH = 1080
        self.WINDOW_HEIGHT = 720
        self.WINDOW_TITLE = "Legend of Peach"
        self.WINDOW_ICON = pygame.image.load('imgs/WINDOW_ICON.png')
        self.BG_COLOR = (135, 206, 235)
        self.FRATERATE = 60

        self.controller = Controller(self)
        self.camera = Camera(self)

        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.game_screen = GameScreen(self)

        self.screen_selector = 0
    def display_screen(self):
        if self.screen_selector is 0:
            self.game_screen.run()