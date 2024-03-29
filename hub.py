import pygame
import sys
import json
from screens.game_screen import GameScreen
from screens.main_menu_screen import MainMenuScreen
from screens.level_selection_screen import LevelSelectionScreen
from sound_board import SoundBoard
from screens.HUD_screen import HudScreen
from controller import Controller
from camera import Camera
from gamemode import GameMode


class Hub:
    """ Hub class, provides a central module to hold all the properties that are constantly being accessed """

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
        self.velocityMushroom = 5
        self.velocityStar = 10

        # DEBUG MODE
        self.modeFreeze = False
        self.modePlace = False

        # Load mario levels from mario level
        self.game_levels = self.get_levels()

        self.gamemode = GameMode(self)
        self.controller = Controller(self)
        self.camera = Camera(self)

        # Screen selector chooses what screen to display
        self.screen_selector = 1
        self.level_name = ''

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
        self.RISE = "RISE"
        self.FALL = "FALL"
        # Brick States
        self.RESTING = 'RESTING'
        self.BUMPED = 'BUMPED'
        self.OPENED = 'OPENED'

        """ Initialize the type of screen possible to display
        game_screen is the only one that will probably be reinstance everytime a new level
        opens. """
        self.sound_board = SoundBoard()
        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.hud_screen = HudScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.level_screen = LevelSelectionScreen(self)
        self.game_screen = GameScreen(self)

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
                if self.gamemode.lives == 0:
                    # When mario has no more lives
                    self.gamemode.reset_gamemode()
                    self.sound_board.gameover.play()
                    self.screen_selector = 1
                else:
                    self.open_level(self.level_name)
                    self.gamemode.mario_is_dead = False

        self.hud_screen.run()

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def get_levels():
        """ Grab the level data from the JSON file"""
        filename = 'levels.json'
        with open(filename, 'r') as read_file:
            data = json.load(read_file)
            return data

    def open_level(self, level_name, world_offset=0):
        """ Opens new gamee_screen and level"""
        print('new game_screen instantiated')
        self.game_screen = GameScreen(self, level_name)
        self.level_name = level_name
        theme = self.game_levels[level_name]["theme"]
        self.camera.reset_camera()
        self.camera.world_offset_x = world_offset

        if theme is "0":
            self.sound_board.play_main_theme_overworld()
        elif theme is "1":
            self.sound_board.play_underworld()
        elif theme is "2":
            self.sound_board.play_castle()
        else:
            self.sound_board.play_main_theme_overworld()
