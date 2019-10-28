import pygame
import sys
import json
from screens.game_screen import GameScreen
from screens.main_menu_screen import MainMenuScreen
from screens.level_selection_screen import LevelSelectionScreen
from controller import Controller
from camera import Camera
from gamemode import GameMode


class Hub:
    """ Hub class, provides a central module to hold all the propertie that are constantly being accessed """

    def __init__(self):
        """ Initialize default values """
        self.CLOCK = pygame.time.Clock()
        self.WINDOW_WIDTH = 1080
        self.WINDOW_HEIGHT = 720
        self.WINDOW_TITLE = "Legend of Peach"
        self.WINDOW_ICON = pygame.image.load('imgs/WINDOW_ICON.png')
        self.BG_COLOR = (0, 0, 0)
        self.FRAMERATE = 30
        self.speed = 0

        # PHYSICS VALUES
        self.GRAVITY = 10
        self.velocityAI = 5

        # DEBUG MODE
        self.modeFreeze = False
        self.modePlace = False

        # Load mario levels from mario level
        self.game_levels = self.get_levels()

        self.gamemode = GameMode(self)
        self.controller = Controller(self)
        self.camera = Camera(self)

        # STATES
        self.WALK = 'WALK'
        self.LEFT = 'LEFT'
        self.RIGHT = 'RIGHT'
        self.STOMPED = 'STOMPED'
        self.STAND = 'STAND'
        self.SHELL = 'SHELL'
        self.SLIDE = 'SLIDE'
        self.HIT = 'HIT'
        self.DEATHFALL = 'DEATHFALL'

        # Brick States
        self.RESTING = 'RESTING'
        self.BUMPED = 'BUMPED'
        self.OPENED = 'OPENED'

        """ Initialize the type of screen possible to display
        game_screen is the only one that will probably be reinstance everytime a new level
        opens. """
        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.main_menu_screen = MainMenuScreen(self)
        self.level_screen = LevelSelectionScreen(self)
        self.game_screen = GameScreen(self)

        # Screen selector chooses what screen to display
        self.screen_selector = 1
        self.level_name = ''



    def display_screen(self):
        if self.screen_selector is 1:
            self.main_menu_screen.run()
        elif self.screen_selector is 2:
            self.level_screen.run()
        elif self.screen_selector is 3:
            # display gameover screen
            pass
        elif self.screen_selector is 0:
            # runs the game screen
            self.game_screen.run()
            if self.gamemode.mario_is_dead:
                self.open_level(self.level_name)
                self.gamemode.mario_is_dead = False


    def exit_game(self):
        pygame.quit()
        sys.exit()

    def get_levels(self):
        """ Grab the level data from the JSON file"""
        filename = 'levels.json'
        with open(filename, 'r') as read_file:
            data = json.load(read_file)
            return data

    def open_level(self, level_name, world_offset=0):
        print('new game_screen instantiated')
        self.game_screen = GameScreen(self, level_name)
        self.level_name = level_name
        self.camera.reset_camera()
        self.camera.world_offset_x = world_offset