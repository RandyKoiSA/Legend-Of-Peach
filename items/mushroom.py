import pygame
from pygame.sprite import Sprite


class Mushroom(Sprite):
    """Base Mushroom class """
    def __init__(self, hub, x, y, direction, name, images, scale):
        """Seting up values for movement"""
        super().__init__()
        # Values
        self.name = name
        self.hub = hub
        self.original_pos = [x, y]
        self.move = direction
        self.velX = self.hub.velocityMushroom
        self.velY = 1
        self.state = self.hub.STAND
        self.scale = scale
        self.rest_height = y

        # Screen Camera
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.camera = hub.camera

        # Images
        self.index = 0
        self.image_index = images
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, scale)
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
            self.velX = - self.hub.velocityMushroom
        elif self.move == self.hub.RIGHT:
            self.velX = self.hub.velocityMushroom

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the Mushroom Logic"""
        if self.state == self.hub.STAND:
            if self.rect.y > (self.rest_height - 50):
                self.rect.y -= self.velY
            else:
                self.state = self.hub.WALK
        else:
            # Apply gravity
            self.rect.y += self.gravity

            # Check if hit right wall, if so move left
            #if self.check_rightedge():
                #self.move = self.hub.LEFT

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


class Magic(Mushroom):
    def __init__(self, hub, x, y):
        self.name = "magic"
        self.scale = (50, 50)
        self.hub = hub
        self.direction = self.hub.RIGHT
        self.image_index = [pygame.image.load("imgs/Items/MagicMushroom.png")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, scale=self.scale)


class Oneup(Mushroom):
    def __init__(self, hub, x, y):
        self.name = "oneup"
        self.scale = (50, 50)
        self.hub = hub
        self.direction = self.hub.RIGHT
        self.image_index = [pygame.image.load("imgs/Items/1upMushroomDark.png")]
        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, scale=self.scale)
