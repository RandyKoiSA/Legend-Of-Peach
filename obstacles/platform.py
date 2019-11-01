import pygame
from pygame.sprite import Sprite

class Platform(Sprite):
    """Platforms that fall when stood on"""
    def __init__(self, hub, x, y, name='platform'):
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]

        self.velY = 0
        self.state = hub.RESTING
        self.scale = (120, 20)

        # Screen Camera
        self.screen = self.hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        self.clock = 0
        self.first_touch = False
        # Image
        self.image = pygame.image.load("imgs/Platform/MovingPlatform.png")
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()

        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.check_state()

    def check_state(self):
        if self.state == self.hub.RESTING:
            self.resting()
        elif self.state == self.hub.FALL:
            self.start_falling()

    def resting(self):
        self.first_touch = False
        self.velY = 0
        pass

    def start_falling(self):
        self.velY = 2
        if not self.first_touch:
            print("TOUCHED")
            self.first_touch = True
            self.clock = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.clock > 400:
            self.falling()

    def falling(self):
            print("FALLING")
            self.velY += 4
            self.rect.y += self.velY

    def check_gone(self):
        """Remove When off screen"""
        if self.rect.y > self.screen_rect.bottom:
            self.kill()