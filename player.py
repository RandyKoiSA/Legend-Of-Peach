import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """ Player class, where the player will control """
    def __init__(self, hub):
        """ Initialize default values """
        super().__init__()
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.controller = hub.controller
        self.camera = hub.camera

        self.rect = pygame.Rect((50, 50), (50, 100))
        self.gravity = 9.8
        self.velocity = 10
        self.jump_left = 1

    def update(self):
        """ Update the player logic """
        # Apply gravity
        self.rect.y += self.gravity

        # Apply movement
        if self.controller.move_right:
            self.rect.x += self.velocity
        if self.controller.move_left:
            self.rect.x -= self.velocity
        if self.controller.jump:
            if self.jump_left != 0:
                self.jump_left -= 1
                self.rect.y -= 150

        self.check_collision()

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 3)

    def check_collision(self):
        if self.rect.left < self.screen_rect.left:
            self.rect.left = self.screen_rect.left
        if self.rect.right > self.screen_rect.right / 2:
            self.rect.right = self.screen_rect.width / 2
            self.camera.world_offset_x += self.velocity
