import pygame
from pygame.sprite import Sprite


class Coins(Sprite):
    """Coins"""
    def __init__(self, hub, x, y, name='coin', state='floating'):
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]

        self.rest_height = y

        self.rest_x = x
        self.velY = 0
        self.upwards = True
        self.state = state
        self.scale = (30, 50)
        self.scale2 = (14, 50)
        self.scale3 = (4, 50)

        # Screen Camera
        self.screen = self.hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.change_freq = 120
        self.player_clock = pygame.time.get_ticks() + self.change_freq
        self.frameRate = 30
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.image_index = [pygame.image.load("imgs/Items/coin1.png"),
                            pygame.image.load("imgs/Items/coin2.png"),
                            pygame.image.load("imgs/Items/coin3.png"),
                            pygame.image.load("imgs/Items/coin2.png")]

        self.image_index[0] = pygame.transform.scale(self.image_index[0], self.scale)
        self.image_index[1] = pygame.transform.scale(self.image_index[1], self.scale2)
        self.image_index[2] = pygame.transform.scale(self.image_index[2], self.scale3)
        self.image_index[3] = pygame.transform.scale(self.image_index[3], self.scale2)

        self.resting_index = [pygame.image.load("imgs/Items/CoinForBlackBG.png"),
                              pygame.image.load("imgs/Items/CoinForBlackBG1.png"),
                              pygame.image.load("imgs/Items/CoinForBlackBG2.png"),
                              pygame.image.load("imgs/Items/CoinForBlackBG1.png")]

        for i in range(len(self.resting_index)):
            self.resting_index[i] = pygame.transform.scale(self.resting_index[i], self.scale)

        if self.state == "floating":
            self.image = self.image_index[self.index]
        else:
            self.image = self.resting_index[self.index]

        self.rect = self.image.get_rect()

        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.check_state()

    def check_state(self):
        if self.state == "floating":
            self.start_anim()
        elif self.state == "resting":
            self.resting()

    def start_anim(self):
        """Starts coin spin animation"""
        self.velY = 5

        if self.rect.y == (self.rest_height - 60):
            self.upwards = False

        if self.upwards:
            self.rect.y -= self.velY
        else:
            self.rect.y += self.velY

        # start timer
        if pygame.time.get_ticks() > self.player_clock:
            self.player_clock = pygame.time.get_ticks() + self.change_freq
            if self.index == 0:
                self.original_pos[0] += 8
            elif self.index == 1:
                self.original_pos[0] += 5
            elif self.index == 2:
                self.original_pos[0] -= 5
            elif self.index == 3:
                self.original_pos[0] -= 8
            self.index += 1
            self.index %= len(self.image_index)
            self.image = self.image_index[self.index]

        if self.rect.y == self.rest_height:
            self.hub.gamemode.coins += 1
            self.hub.gamemode.check_coins()
            self.hub.gamemode.score += 200
            self.kill()

    def resting(self):
        """Starts coin rest animation"""
        # start timer
        if pygame.time.get_ticks() > self.player_clock:
            self.player_clock = pygame.time.get_ticks() + self.change_freq
            self.index += 1
            self.index %= len(self.resting_index)
            self.image = self.resting_index[self.index]
