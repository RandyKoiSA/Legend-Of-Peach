from pygame.sprite import Sprite
import pygame


class FloorCollision(Sprite):
    """ Floor Collision creates a rect for the player to walk on """
    def __init__(self, hub, pos=(50, 50), size=(50, 50)):
        """ Initialize default values """
        super().__init__()
        self.screen = hub.main_screen

        self.original_pos = (pos[0], pos[1])
        self.rect = pygame.Rect((pos[0], pos[1]), (size[0], size[1]))
        self.color = (0, 0, 255, 128)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 1)
