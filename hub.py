import pygame


class Hub:
    """ Hub class, provides a central module to hold all the propertie that are constantly being accessed """

    def __init__(self):
        """ Initialize default values """
        self.CLOCK = pygame.time.Clock()
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.WINDOW_TITLE = "Legend of Peach"
        self.WINDOW_ICON = pygame.image.load('imgs/WINDOW_ICON.png')
        self.BG_COLOR = (135, 206, 235)
        self.FRATERATE = 60

        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def display_screen(self):
        pass