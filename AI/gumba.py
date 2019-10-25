import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Base Enemy Class, where the AI will control """
    def __init__(self, hub, x, y, direction, name, images, frame, scale):
        """Seting up values for AI"""
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]
        self.move = direction
        self.velX = 0

        # Screen Camera
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.frameRate = frame
        self.clock = pygame.time.get_ticks() + self.frameRate
        self.image_index = images
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]

        # Physics Values
        self.gravity = 9.8
        self.velocity = 0
        self.check_direction()

        # AI BOOLS
        self.kill = False

    def check_direction(self):
        if self.move == "STILL" or self.hub.modeFreeze == True:
            self.velocity = 0
        elif self.move == "LEFT":
            self.velocity = -self.hub.velocityAI
        elif self.move == "RIGHT":
            self.velocity = self.hub.velocityAI

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the Enemy Logic"""
        # Apply gravity
        self.rect.y += self.gravity

        # Check if hit right wall, if so move left
        if self.check_rightedge():
            self.move = "LEFT"

        self.check_direction()
        # Apply movement
        # Move Right
        self.original_pos[0] += self.velocity
        self.rect.x = self.original_pos[0] - self.camera.world_offset_x
        self.check_collision()

    def flip_direction(self):
        if self.move == "LEFT":
            self.move = "RIGHT"
        else:
            self.move = "LEFT"

    def check_rightedge(self):
        if self.rect.right >= self.screen_rect.right:
            return True

    def check_collision(self):
        if self.rect.left <= 0:
            self.kill = True


class Gumba(Enemy):
    def __init__(self, hub, x, y):
        self.name = "goomba"
        self.frame = 60
        self.scale = (50, 50)
        self.direction = "LEFT"
        self.image_index = [pygame.image.load("imgs/Cut-Sprites-For-Mario/Characters/113_goomba.png")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)


class Paratroops(Enemy):
    def __init__(self, hub, x, y):
        self.name = "paratroop"
        self.frame = 60
        self.scale = (50, 50)
        self.direction = "LEFT"
        self.image_index = [pygame.image.load("")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)


class Koopatroops(Enemy):
    def __init__(self, hub, x, y):
        self.name = "koopatroop"
        self.frame = 60
        self.scale = (50, 50)
        self.direction = "LEFT"
        self.image_index = [pygame.image.load("")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)


class Piranhaplant(Enemy):
    def __init__(self, hub, x, y):
        self.name = "piranhaplant"
        self.frame = 60
        self.scale = (50, 50)
        self.direction = "STILL"
        self.image_index = [pygame.image.load("")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)