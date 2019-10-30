import pygame
from pygame.sprite import Sprite


class Fireflower(Sprite):
    """Fire flower"""
    def __init__(self, hub, x, y, name='fireflower'):
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]

        self.rest_height = y

        self.velY = 5

        self.scale = (50, 50)

        # Screen Camera
        self.screen = self.hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.change_freq = 240
        self.player_clock = pygame.time.get_ticks() + self.change_freq
        self.frameRate = 30
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.image_index = [pygame.image.load("imgs/Items/FireFlower.gif")]

        for i in range(len(self.image_index)):
            self.image_index[i] = pygame.transform.scale(self.image_index[i], self.scale)

        self.image = self.image_index[self.index]

        self.rect = self.image.get_rect()

        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.start_anim()

    def start_anim(self):
        """Starts flower rising animation"""

        if self.rect.y > (self.rest_height - 50):
            self.rect.y -= self.velY