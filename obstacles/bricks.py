import pygame
from pygame.sprite import Sprite

class Bricks(Sprite):
    """Bricks that can be broken"""
    def __init__(self, hub, x, y, insides=None, powerup_group=None, name='brick'):
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]
        self.velX = 0
        self.velY = 0
        self.state = hub.RESTING
        self.scale = (50, 50)

        # Screen Camera
        self.screen = hub.main_menu_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.frameRate = 30
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.image = pygame.image.load("imgs/Blocks/BrickBlockBrown.png")
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect

        self.insides = insides
        self.setup_contents()
        self.group = powerup_group
        self.powerup_in_box = True

    def draw(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        pass