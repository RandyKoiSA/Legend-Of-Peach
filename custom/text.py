import pygame.ftfont
import pygame

class Button:
    def __init__(self, hub, msg):
        """ Initialize button attributes. """
        self.game_hub = hub

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('imgs/UIpack/Font/kenvector_future.ttf', 20)


        self.image = pygame.image.load('imgs/UIpack/PNG/blue_button00.png')
        # Build the button's rect object and center
        self.rect = self.image.get_rect()
        self.rect.center = self.game_hub.main_screen.get_rect().center

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """ Draw button onto the screen """
        self.game_hub.main_screen.blit(self.image, self.rect)
        self.game_hub.main_screen.blit(self.msg_image, self.msg_image_rect)

    def update_message_position(self):
        self.msg_image_rect.center = self.rect.center