import pygame
from pygame.sprite import Sprite

class Gumba(Sprite):
    """ Gumba class, where the AI will control """
    def __init__(self, hub, x, y):
        """ Initialize default values """
        super().__init__()
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera
        self.original_pos = [x, y]

        self.rect = pygame.Rect((self.original_pos[0], self.original_pos[1]), (50, 50))
        self.gravity = 0
        self.velocity = 5

        self.move = True
        self.kill = False

    def update(self):
        """ Update the Gumba Logic"""
        # Apply gravity
        self.rect.y += self.gravity

        # Check if hit right wall, if so move left
        if self.checkrightedge():
            self.move = False

        # Apply movement
        # Move Right
        if self.move == True:
            self.original_pos[0] += self.velocity

        # Move Left
        if self.move == False:
            self.original_pos[0] -= self.velocity

        self.rect.x = self.original_pos[0] - self.camera.world_offset_x
        self.check_collision()

    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 3)

    def checkrightedge(self):
        if self.rect.right >= self.screen_rect.right:
            return True

    def check_collision(self):
        if self.rect.left <= 0:
            self.kill = True
