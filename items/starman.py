import pygame
from pygame.sprite import Sprite


class Starman(Sprite):
    """Base Mushroom class """
    def __init__(self, hub, x, y, name):
        """Seting up values for movement"""
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]
        self.move = self.hub.RIGHT
        self.velX = self.hub.velocityStar
        self.velY = 1
        self.state = self.hub.STAND
        self.scale = (50, 50)
        self.rest_height = y

        # Screen Camera
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.image_index = [pygame.image.load("imgs/Items/Starman.gif")]
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()

        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

        # Physics Values
        self.gravity = self.hub.GRAVITY
        self.check_direction()

        self.killed = False

    def check_direction(self):
        if self.state == self.hub.STAND:
            self.velX = 0
        elif self.move == self.hub.LEFT:
            self.velX = - self.hub.velocityStar
        elif self.move == self.hub.RIGHT:
            self.velX = self.hub.velocityStar

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the Star Logic"""
        if self.state == self.hub.STAND:
            if self.rect.y > (self.rest_height - 50):
                self.rect.y -= self.velY
            else:
                self.state = self.hub.WALK
        else:
            # Apply gravity
            self.rect.y += self.gravity

            self.check_direction()
            # Apply movement
            # Move Right
            self.original_pos[0] += self.velX

        self.check_collision()
        self.check_fell()

    def flip_direction(self):
        if self.move == self.hub.LEFT:
            self.move = self.hub.RIGHT
        else:
            self.move = self.hub.LEFT

    def check_rightedge(self):
        return self.rect.right >= self.screen_rect.right

    def check_collision(self):
        if self.rect.right <= 0:
            self.kill()
            print(self.name + " is Ded")

    def check_fell(self):
        if self.rect.top >= self.screen_rect.bottom:
            self.kill()
