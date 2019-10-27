import pygame
from pygame.sprite import Sprite

class Teleport(Sprite):
    """ Teleporter that teleports the player to the next level """
    def __init__(self, hub, pos_x, pos_y, level_name):
        """ initialize default values """
        super().__init__()
        self.hub = hub
        self.camera = hub.camera
        self.screen = hub.main_screen
        self.width = 100
        self.height = 100
        self.original_pos = (pos_x, pos_y)
        self.level_name = level_name

        self.rect = pygame.Rect((pos_x, pos_y), (self.width, self.height))
        self.color = (255, 0, 0, 128)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def update(self, player_rect):
        if self.rect.colliderect(player_rect):
            if self.hub.controller.up is True:
                self.hub.open_level(self.level_name)

        self.rect.x = self.original_pos[0] - self.camera.world_offset_x
