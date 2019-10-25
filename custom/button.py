import pygame.ftfont
import pygame

class Button:
    def __init__(self, hub, msg, width=200, height=40):
        """ Initialize button attributes. """
        self.game_hub = hub

        # Set the dimensions and properties of the button.
        self.width, self.height = width, height
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)

        self.image = pygame.image.load('imgs/UI/blue_button05.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # Build the button's rect object and center
        self.rect = self.image.get_rect()
        self.rect.center = self.game_hub.main_screen.get_rect().center

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        self.message = msg

    def draw(self):
        """ Draw button onto the screen """
        self.game_hub.main_screen.blit(self.image, self.rect)
        self.game_hub.main_screen.blit(self.msg_image, self.msg_image_rect)

    def update_message_position(self):
        self.msg_image_rect.center = self.rect.center