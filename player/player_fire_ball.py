import pygame
from pygame.sprite import Sprite
from math import sin, cos

class Player_FireBall(Sprite):
    """ Spawns in fire-ball when mario is in fiery state """
    def __init__(self, hub, player_fireball_group, pos_x, pos_y):
        super().__init__()

        self.hub = hub
        self.screen = hub.main_screen
        self.player_fireball_group = player_fireball_group

        self.lifetime = pygame.time.get_ticks() + 1000

        self.index = 0
        self.nextFrame = 100
        self.tick = pygame.time.get_ticks() + self.nextFrame

        self.original_x = pos_x
        self.original_y = pos_y

        self.velocity = 15

        self.fireball_images = [pygame.image.load('imgs/Other/FireBall/fireball_01.gif'),
                                pygame.image.load('imgs/Other/FireBall/fireball_02.gif'),
                                pygame.image.load('imgs/Other/FireBall/fireball_03.gif'),
                                pygame.image.load('imgs/Other/FireBall/fireball_04.gif')]
        self.prep_fireball_images()

        self.current_image = self.fireball_images[self.index]
        self.rect = self.current_image.get_rect()
        self.rect.x = self.original_x
        self.rect.y = self.original_y

    def update(self):
        # check timer to change image
        if pygame.time.get_ticks() > self.tick:
            self.tick = pygame.time.get_ticks() + self.nextFrame
            self.index += 1
            self.index %= len(self.fireball_images)
            self.current_image = self.fireball_images[self.index]

        # check if the fire should die
        if pygame.time.get_ticks() >= self.lifetime:
            self.player_fireball_group.remove(self)

        # update fire ball position
        self.original_x += self.velocity
        self.rect.x = self.original_x - self.hub.camera.world_offset_x

    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def prep_fireball_images(self):
        for i in range (0, len(self.fireball_images)):
            self.fireball_images[i] = pygame.transform.scale(self.fireball_images[i], (25, 25))
