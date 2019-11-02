import pygame
from pygame.sprite import Sprite
from Points import Points

class Flag_Pole(Sprite):
    def __init__(self, hub, x, y):
        super().__init__()
        
        self.hub = hub
        self.camera = self.hub.camera
        self.screen = hub.main_screen
        
        self.image_list = [pygame.image.load('imgs/Misc-2/2.png'),
                           pygame.image.load('imgs/Misc-2/3.png'),
                           pygame.image.load('imgs/Misc-2/4.png'),
                           pygame.image.load('imgs/Misc-2/5.png')]
        self.prep_image_list()
        
        
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()

        self.original_x = x
        self.original_y = y

        self.rect.x = x
        self.rect.y = y

    def prep_image_list(self):
        size = 95
        for i in range (0, len(self.image_list)):
            self.image_list[i] = pygame.transform.scale(self.image_list[i], (size, size*6))

    def update(self, player_rect, point_group):
        self.rect.x = self.original_x - self.camera.world_offset_x

        # check if the player collide with it
        if self.rect.colliderect(player_rect):
            if player_rect.top < self.rect.top + 142:
                # give 1000 pts
                self.hub.gamemode.score += 1000
                point_group.add(Points(self.hub, point_group, "1000pts", self.rect.centerx,
                                       self.rect.centery))
            elif player_rect.top < self.rect.top + 284:
                # give 500 pts
                self.hub.gamemode.score += 500
                point_group.add(Points(self.hub, point_group, "500pts", self.rect.centerx,
                                self.rect.centery))
                self.image = self.image_list[1]
            elif player_rect.top < self.rect.top + 426:
                # give 200 pts
                self.hub.gamemode.score += 200
                point_group.add(Points(self.hub, point_group, "200pts", self.rect.centerx,
                                       self.rect.centery))
                self.image = self.image_list[2]
            else:
                # give 100 pts
                self.hub.gamemode.score += 100
                point_group.add(Points(self.hub, point_group, "100pts", self.rect.centerx,
                                       self.rect.centery))
                self.image = self.image_list[3]

    def draw(self):
        self.screen.blit(self.image, self.rect)