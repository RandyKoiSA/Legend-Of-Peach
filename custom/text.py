import pygame.ftfont


class Text:
    """ Renders a text onto the screen """
    def __init__(self, screen, message,
                 text_color=(255, 255, 255), background_color=(125, 125, 125),
                 pos_x=0, pos_y=0, font_size=48):
        """ Initialize default values """

        self.screen = screen
        self.message = message
        self.text_color = text_color
        self.font_size = font_size
        self.background_color = background_color
        self.font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)

        # Turn message into a rendered image and center on the button
        self.msg_image = self.font.render(self.message, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()

        # Placement of the mesasge
        self.msg_image_rect.centerx = pos_x
        self.msg_image_rect.centery = pos_y

    def draw(self):
        """ Draw the text on the given screen """
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def update_message(self):
        """ Updating the message if it ends up changing """
        self.msg_image = self.font.render(self.message, True, self.text_color)
