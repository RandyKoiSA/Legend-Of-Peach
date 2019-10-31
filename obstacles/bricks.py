import pygame
from pygame.sprite import Sprite


class Bricks(Sprite):
    """Bricks that can be broken"""
    def __init__(self, hub, x, y, insides="None", powerup_group="Brick", name='brick', theme='0'):
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
        self.frameRate = 120
        self.clock = 0
        self.theme = theme
        self.image_index = [pygame.image.load("imgs/Blocks/"+str(self.theme)+"/BrickBlock.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/EmptyBlock.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock000.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock001.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock002.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock003.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock004.png"),
                            pygame.image.load("imgs/Blocks/"+str(self.theme)+"/QBlock005.png")]
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.clock = pygame.time.get_ticks() + self.frameRate

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
        if self.insides == 'coin':
            self.coin_total = 1
        elif self.insides == 'coins':
            self.coin_total = 6
        else:
            self.coin_total = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.group == "box":
            if pygame.time.get_ticks() > self.clock:
                self.clock = pygame.time.get_ticks() + self.frameRate
                self.index += 1
                self.index %= 6
                self.image = self.image_index[self.index + 2]
                self.image = pygame.transform.scale(self.image, (50, 50))
        self.check_state()

    def check_state(self):
        if self.state == self.hub.RESTING:
            self.resting()
        elif self.state == self.hub.BUMPED:
            self.start_bump()
        elif self.state == self.hub.OPENED:
            self.opened()

    def resting(self):
        """State when not moving"""
        if self.insides == 'coins':
            if self.coin_total <= 0:
                self.state = self.hub.OPENED
            else:
                self.state = self.hub.RESTING

    def start_bump(self):
        """Start of bumped state"""
        self.velY = -5
        self.rect.y += self.velY
        if (self.insides == 'coins' or self.insides == 'coin') and not self.bumped_up:
            self.bumped_up = True
            if self.coin_total > 0:
                print("Spawn a coin" + str(self.coin_total))
                self.coin_total -= 1
                if self.coin_total <= 0:
                    self.index = 1
        elif self.insides == 'star' or self.insides == 'gshroom' or self.insides == 'rshroom':
            self.bumped_up = True
            self.index = 1
        else:
            self.bumped_up = True
        if self.rect.y <= (self.rest_height - 20) or self.rect.y >= (self.rest_height + 20):
            self.bumped()

    def bumped(self):
        """Bump state actions"""
        if self.rect.y <= (self.rest_height - 20) or self.rect.y >= (self.rest_height + 20):
            self.rect.y = self.rest_height
            self.bumped_up = False
            self.velY = 0
        if self.insides == 'coins' or self.insides == 'coin':
            if self.coin_total == 0:
                self.state = self.hub.OPENED
            else:
                self.state = self.hub.RESTING
        elif self.insides == 'star' or self.insides == 'gshroom' or self.insides == 'rshroom':
            self.state = self.hub.OPENED
        else:
            self.kill()

    def opened(self):
        """Action during Opened State"""
        if self.rect.y <= (self.rest_height - 10) or self.rect.y >= (self.rest_height + 10):
            self.rect.y = self.rest_height
        self.image = self.image_index[1]
        self.image = pygame.transform.scale(self.image, self.scale)
        if self.powerup_in_box and (self.insides == 'star' or self.insides == 'coin' or self.insides == 'gshroom' or
                                    self.insides == 'rshroom'):
            self.insides = "None"
            self.powerup_in_box = False


class BrickPieces(Sprite):
    """ Pieces appear when brick is broken"""
    def __init__(self, hub, x, y, velx, vely, theme='0'):
        super().__init__()
        self.hub = hub
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera
        self.theme = theme
        self.image = pygame.image.load("imgs/Blocks/"+self.theme+"/BrickBlock.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.original_pos = [x, y]
        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]
        self.velX = velx
        self.velY = vely
        self.gravity = hub.GRAVITY
        self.turntimer = 0

    def update(self):
        """Update Brick Piece"""
        self.rect.x += self.velX
        if pygame.time.get_ticks() - self.turntimer > 100:
            self.turntimer = pygame.time.get_ticks()
            self.image = pygame.transform.rotozoom(self.image, self.velX, 1)
        print("PIECE AT " + str(self.rect.x))
        self.rect.y += self.velY
        self.velY += self.gravity
        self.check_gone()

    def check_gone(self):
        """Remove When off Screen"""
        if self.rect.y > self.screen_rect.bottom:
            print("REMOVED PIECE")
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)