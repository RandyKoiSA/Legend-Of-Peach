import pygame
from pygame.sprite import Sprite


class Pipe(Sprite):
    """ Pipe is similar to world collisions, used to hide piranhas flowers """
    def __init__(self, hub, pipetype = 0, pos_x=0, pos_y=0):
        super().__init__()
        self.hub = hub
        self.screen = hub.main_screen
        self.image_list = [pygame.image.load('imgs/Misc-2/12.png'),
                           pygame.image.load('imgs/Misc-2/13.png'),
                           pygame.image.load('imgs/Misc-2/14.png')]
        self.prep_image_list()
        try:
            self.image = self.image_list[pipetype]
        except LookupError:
            self.image = self.image_list[0]

        self.original_x = pos_x
        self.original_y = pos_y
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.x = self.original_x - self.hub.camera.world_offset_x
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def prep_image_list(self):
        self.image_list[0] = pygame.transform.scale(self.image_list[0], (100, 100))
        self.image_list[1] = pygame.transform.scale(self.image_list[1], (100, 160))
        self.image_list[2] = pygame.transform.scale(self.image_list[2], (100, 205))
        pass