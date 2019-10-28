import pygame
from pygame.sprite import Sprite


class Bricks(Sprite):
    """Bricks that can be broken"""
    def __init__(self, hub, x, y, insides="None", powerup_group="Brick", name='brick'):
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]

        self.rest_height = y
        self.velY = 0
        self.state = hub.RESTING
        self.scale = (50, 50)

        # Screen Camera
        self.screen = self.hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.frameRate = 30
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.image_index = [pygame.image.load("imgs/Blocks/BrickBlockDark.png"),
                            pygame.image.load("imgs/Blocks/EmptyBlock.png")]
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()

        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

        self.insides = insides
        self.coin_total = 0
        self.setup_contents()
        self.group = powerup_group
        self.powerup_in_box = True
        self.bumped_up = False


    def setup_contents(self):
        """Puts in Coins if content is needed"""
        if self.insides == 'coins':
            self.coin_total = 6
        else:
            self.coin_total = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.check_state()

    def check_state(self):
        if self.state == self.hub.RESTING:
            self.resting()
        elif self.state == self.hub.BUMPED:
            self.bumped()
        elif self.state == self.hub.OPENED:
            self.opened()

    def resting(self):
        """State when not moving"""
        if self.insides == 'coins':
            if self.coin_total == 0:
                self.state = self.hub.OPENED

    def start_bump(self):
        """Start of bumped state"""
        self.velY = -6
        if self.insides == 'coins':

            if self.coin_total > 0:
                # Spawn coin
                print("Spawn a coin")
                self.coin_total -= 1
                if self.coin_total == 0:
                    self.index = 1
                    self.image = self.image_index[self.index]
                    self.image = pygame.transform.scale(self.image, self.scale)
        elif self.insides == 'star':
            self.index = 1
            self.image = self.image_index[self.index]
            self.image = pygame.transform.scale(self.image, self.scale)

        self.state = self.hub.BUMPED

    def bumped(self):
        """Bump state actions"""
        self.rect.y += self.velY
        self.velY += self.hub.GRAVITY

        if self.rect.y >= (self.rest_height + 5):
            self.rect.y = self.rest_height
            if self.insides == 'coins':
                if self.coin_total == 0:
                    print("Spawn a coin")
                    self.state = self.hub.OPENED
                else:
                    self.state = self.hub.RESTING
            elif self.insides == 'star':
                self.state = self.hub.OPENED
            else:
                self.state = self.hub.RESTING

    def opened(self):
        """Action during Opened State"""
        self.index = 1
        self.image = self.image_index[self.index]
        if self.powerup_in_box and self.insides == 'star':
            print("Spawn a Star")
            self.powerup_in_box = False


class BrickPieces(Sprite):
    """ Pieces appear when brick is broken"""
    def __init__(self, hub, x, y, velx, vely):
        super().__init__()
        self.hub = hub
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera
        self.image = pygame.image.load("imgs/Blocks/BrickBlockBrown.png")
        self.image = pygame.transform.scale(self.image,  (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velX = velx
        self.velY = vely
        self.gravity = hub.GRAVITY

    def update(self):
        """Update Brick Piece"""
        self.rect.x += self.velX
        self.rect.y += self.velY
        self.velY += self.gravity
        self.check_gone()

    def check_gone(self):
        """Remove When off Screen"""
        if self.rect.y > self.screen_rect.bottom:
            self.kill()
