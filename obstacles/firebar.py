import pygame
from pygame.sprite import Sprite
import os


class Firebar(Sprite):
    """Firebar the can collide"""

    def __init__(self, hub, x, y, name='firebar', direction='LEFT'):
        super().__init__()
        self.name = name
        self.hub = hub
        self.original_pos = (x + 4, y + 28)

        self.scale = (271, 271)

        self.screen = self.hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        self.index = 0
        self.increment = 1
        self.frameRate = 30
        self.clock = 0
        self.image_index = []
        self.setimages()
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, self.scale)
        self.brick = pygame.image.load("imgs/Blocks/2/EmptyBlock.png")
        self.rect = self.image.get_rect()
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.rect.center = self.original_pos
        # self.mask = pygame.mask.from_surface(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask2 = pygame.mask.Mask((80, 80), True)
        self.mask.erase(self.mask2, (95, 95))
        self.direction = direction

    def setimages(self):
        for i in os.listdir("imgs\Firebar"):
            self.image_index.append(pygame.image.load("imgs/Firebar/" + i))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.check_direction()
        if pygame.time.get_ticks() > self.clock:
            self.clock = pygame.time.get_ticks() + self.frameRate
            self.index += self.increment
            self.index %= len(self.image_index)
            self.image = self.image_index[self.index]
            self.image = pygame.transform.scale(self.image, self.scale)
            self.mask = pygame.mask.from_surface(self.image)
            self.mask.erase(self.mask2, (95, 95))

    def check_direction(self):
        if self.direction == self.hub.LEFT:
            self.increment = -1
        else:
            self.increment = 1
