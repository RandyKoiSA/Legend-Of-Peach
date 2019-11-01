import pygame
from pygame.locals import *
from custom.text import Text
from custom.button import Button


class LevelSelectionScreen:
    """ Level Selection Screen, where you can select certain levels to play """

    def __init__(self, hub):
        """ Initialize default values """
        self.hub = hub
        self.gamemode = hub.gamemode
        self.screen = hub.main_screen

        # Set up background
        self.background_image = pygame.image.load('imgs/background/bg-1-1.png')
        self.background_rect = self.background_image.get_rect()
        self.prep_background()

        # get list of all levels
        self.level_list = []
        self.create_level_buttons()
        self.prep_level_buttons()

        # level text
        self.title_text = Text(self.screen, "Select Level")
        self.prep_title_text()

        # Back button
        self.back_button = Button(self.hub, "Back")
        self.prep_back_button()

    def run(self):
        self.run_event()
        self.run_update()
        self.run_draw()

    def run_event(self):
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
        pass

    def run_draw(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.title_text.draw()
        self.back_button.draw()
        self.draw_level_buttons()

    def prep_title_text(self):
        self.title_text.msg_image_rect.center = self.screen.get_rect().center
        self.title_text.msg_image_rect.top = 100

    def prep_back_button(self):
        self.back_button.rect.x = 10
        self.back_button.rect.y = 100
        self.back_button.update_message_position()

    def check_button_clicked(self, mouse_x, mouse_y):
        if self.back_button.rect.collidepoint(mouse_x, mouse_y):
            self.hub.screen_selector = 1
        for button in self.level_list:
            if button.rect.collidepoint(mouse_x, mouse_y):
                # noinspection PyBroadException
                try:
                    self.hub.open_level(button.message)
                    self.gamemode.reset_gamemode()
                    self.hub.screen_selector = 0
                except Exception:
                    print('error: failed to load level')
                    self.hub.screen_selector = 2

    def prep_background(self):
        """ Make background adjustments """
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.background_rect.width * 3 + 70,
                                                        self.background_rect.height * 3 + 70))
        self.background_rect = self.background_image.get_rect()

    def create_level_buttons(self):
        """ Create all existing level and put them in list """
        for level in self.hub.game_levels.keys():
            self.level_list.append(Button(self.hub, level, 70, 50))
        # prit the list of buttons
        print(self.level_list)

    def prep_level_buttons(self):
        """ Adjustments to all the list of buttons created """
        counter = 0
        for button in self.level_list:
            button.rect.center = self.screen.get_rect().center
            button.rect.y -= 200
            button.rect.x -= 150
            button.rect.x += (counter % 4) * 100
            button.rect.y += int(counter / 4) * 70
            button.update_message_position()

            counter += 1

    def draw_level_buttons(self):
        """ Draw all the level buttons onto the screen """
        if self.level_list is []:
            print('level list is empty')
            return
        else:
            # noinspection PyBroadException
            try:
                for button in self.level_list:
                    button.draw()
            except Exception:
                print('error: could not open levels')
