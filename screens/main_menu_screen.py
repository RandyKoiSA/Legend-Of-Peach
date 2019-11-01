import pygame
from pygame.locals import *
from custom.text import Text
from custom.button import Button


class MainMenuScreen:
    """ Main Menu Screen showing exit button and play button """

    def __init__(self, hub):
        """ Initialize all the default values for MainMenuScreen """
        self.hub = hub
        self.screen = hub.main_screen

        # Set up background
        self.background_image = pygame.image.load('imgs/background/bg-1-1.png')
        self.background_rect = self.background_image.get_rect()
        self.prep_background()

        # Title image
        self.title_image = pygame.image.load('imgs/MainMenu/main_menu.png')
        self.title_rect = self.title_image.get_rect()
        self.prep_title()

        # Instruction text
        self.movement_text = Text(self.screen, "Movement: Arrow Keys/WASD")
        self.prep_movement_text()

        # Movement Text
        self.action_text = Text(self.screen, "Fire/Sprint: Shift/CTRL")
        self.prep_action_text()

        # Level Selection Mode
        self.level_button = Button(self.hub, "Level Select")
        self.prep_level_button()

        # Exit button
        self.exit_button = Button(self.hub, "Exit Game")
        self.prep_exit_button()

    def run(self):
        self.run_event()
        self.run_update()
        self.run_draw()

    def run_event(self):
        """ Run the event on the main screen """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.hub.exit_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.hub.exit_game()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_button_clicked(mouse_x, mouse_y)

    def run_update(self):
        """ Run all instances in them main menu screen """
        pass

    def run_draw(self):
        """ Draw all the stuff onto my main menu screen"""
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.title_image, self.title_rect)
        self.movement_text.draw()
        self.action_text.draw()
        self.level_button.draw()
        self.exit_button.draw()

    def prep_title(self):
        """ Make adjusts for title screen"""
        # Rescale the title image
        self.title_image = pygame.transform.scale(self.title_image,
                                                  (self.title_rect.width * 2, self.title_rect.height * 2))
        # Set the title rect
        self.title_rect = self.title_image.get_rect()

        # Move the title screen to the middle
        self.title_rect.center = self.screen.get_rect().center
        # Create top offset
        self.title_rect.top -= 200

    def prep_movement_text(self):
        """ Make adjustments for control text """
        self.movement_text.msg_image_rect.center = self.title_rect.center
        self.movement_text.msg_image_rect.bottom += 150

    def prep_background(self):
        """ Make background adjustments """
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.background_rect.width * 3 + 70,
                                                        self.background_rect.height * 3 + 70))
        self.background_rect = self.background_image.get_rect()

    def prep_action_text(self):
        """ Make adjustments to the action text """
        self.action_text.msg_image_rect.center = self.movement_text.msg_image_rect.center
        self.action_text.msg_image_rect.bottom += 50

    def prep_level_button(self):
        """ Make adjustments to the level button """
        self.level_button.rect.center = self.action_text.msg_image_rect.center
        self.level_button.rect.bottom += 50
        self.level_button.update_message_position()

    def prep_exit_button(self):
        """ Make adjustments to the exit button """
        self.exit_button.rect.center = self.level_button.rect.center
        self.exit_button.rect.bottom += 50
        self.exit_button.update_message_position()

    def check_button_clicked(self, mouse_x, mouse_y):
        if self.level_button.rect.collidepoint(mouse_x, mouse_y):
            # open level screen
            self.hub.screen_selector = 2
        elif self.exit_button.rect.collidepoint(mouse_x, mouse_y):
            self.hub.exit_game()
