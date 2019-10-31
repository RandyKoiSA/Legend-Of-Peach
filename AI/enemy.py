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
        self.velX = self.hub.velocityAI
        self.velY = 0
        self.state = hub.STAND
        self.scale = scale
        self.counter_bounce = 0
        self.bounce_max_height = 100
        self.bounce_velocity = 35

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

        self.death_timer = 0

        # Physics Values
        self.gravity = self.hub.GRAVITY
        self.velocity = 0
        self.check_direction()

        # AI booleans
        self.killed = False
        self.isstomped = False
        self.isflipped = False
        self.isbouncing = False
        self.checked = False

    def check_direction(self):
        if self.state == self.hub.STAND:
            self.velX = 0
        elif self.move == self.hub.LEFT:
            self.velX = - self.hub.velocityAI
        elif self.move == self.hub.RIGHT:
            self.velX = self.hub.velocityAI

    def check_cam(self):
        if self.camera.world_offset_x + self.screen_rect.right > self.original_pos[0] and\
         not self.checked:
            self.state = self.hub.WALK
            self.checked = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the Enemy Logic"""
        # Apply gravity
        self.rect.y += self.gravity
        self.curr_state()
        self.check_collision()
        # print(self.name + " is " + self.state)
        self.check_fell()

    def flip_direction(self):
        if self.move == self.hub.LEFT:
            self.move = self.hub.RIGHT
        else:
            self.move = self.hub.LEFT

    def check_rightedge(self):
        if self.rect.right >= self.screen_rect.right:
            return True

    def check_rightedgekill(self):
        if self.rect.left >= self.screen_rect.right:
            self.kill()
            print(self.name + " is Ded")

    def check_collision(self):
        if self.rect.right <= 0:
            self.kill()
            print(self.name + " is Ded")

    def check_fell(self):
        if self.rect.top == self.screen_rect.bottom:
            self.kill()

    def curr_state(self):
        """Enemy State Behavior"""
        if self.state == self.hub.STAND:
            self.check_cam()
        if self.state == self.hub.WALK:
            self.walking()
        elif self.state == self.hub.STOMPED:
            self.stomped()
        elif self.state == self.hub.HIT:
            self.start_death_falling()
        elif self.state == self.hub.DEATHFALL:
            self.death_falling()
        elif self.state == self.hub.SLIDE:
            self.slide()
        elif self.state == self.hub.SHELL:
            self.shell()

    def shell(self):
        self.velX = 0

    def slide(self):
        if self.move == self.hub.RIGHT or self.hub.STAND:
            self.velX = 20
        if self.move == self.hub.LEFT:
            self.velX = -20
        self.check_rightedgekill()
        self.check_collision()
        self.original_pos[0] += self.velX

    def walking(self):
        # Check if hit right wall, if so move left
        if self.check_rightedge():
            self.move = self.hub.LEFT

        self.check_direction()
        # Apply movement
        # Move Right
        self.original_pos[0] += self.velX

        if pygame.time.get_ticks() > self.clock:
            self.index = (self.index + 1) % 2
            self.image = self.image_index[self.index]
            self.image = pygame.transform.scale(self.image, self.scale)
            self.clock = pygame.time.get_ticks() + self.frameRate
            if self.move == self.hub.LEFT and not self.isflipped:
                self.image = pygame.transform.flip(self.image, True, False)

    def stomped(self):
        """Placeholder for when enemy stomped"""
        pass

    def start_death_falling(self):
        """Death Jump State"""
        self.isbouncing = True
        if self.move == self.hub.RIGHT or self.move == self.hub.STAND:
            self.velX = 10
        else:
            self.velX = -10
        # self.index = 3
        # self.image = self.image_index[self.index]
        self.state = self.hub.DEATHFALL

        if pygame.time.get_ticks() > self.clock:
            self.index = (self.index + 1) % 2
            self.image = self.image_index[self.index]
            self.image = pygame.transform.scale(self.image, self.scale)
            self.clock = pygame.time.get_ticks() + self.frameRate
            self.image = pygame.transform.flip(self.image, False, True)

    def death_falling(self):
        """Death falling"""

        if self.isbouncing:
            if self.counter_bounce < self.bounce_max_height:
                self.counter_bounce += self.bounce_velocity
                self.rect.y -= self.bounce_velocity
            if self.counter_bounce > self.bounce_max_height:
                self.isbouncing = False
        else:
            self.rect.y += self.velY
            self.rect.x += self.velX
            self.velY += self.gravity
        if pygame.time.get_ticks() > self.clock:
            self.index = (self.index + 1) % (len(self.image_index) - 1)
            self.image = self.image_index[self.index]
            self.image = pygame.transform.scale(self.image, self.scale)
            self.clock = pygame.time.get_ticks() + self.frameRate
            self.image = pygame.transform.flip(self.image, False, True)

        if self.rect.y > self.screen_rect.bottom:
            self.kill()

    def next_frame(self):
        """Frame change"""
        self.image = self.image_index[self.index]


class Gumba(Enemy):
    def __init__(self, hub, x, y):
        self.name = "goomba"
        self.frame = 100
        self.scale = (50, 50)
        self.direction = hub.LEFT
        self.image_index = [pygame.image.load("imgs/Enemies/LittleGoomba/goomba_01.gif"),
                            pygame.image.load("imgs/Enemies/LittleGoomba/goomba_02.gif")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)

    def stomped(self):
        """When Mario stomps him"""
        self.image = self.image_index[self.index]
        self.image = pygame.transform.scale(self.image, (50, 25))
        if self.isstomped:
            self.isstomped = False
            self.rect.y += 10
            self.gravity = 0

        if(pygame.time.get_ticks() - self.death_timer) > 500:
            self.killed = True


class Koopatroops(Enemy):
    def __init__(self, hub, x, y):
        self.name = "koopatroop"
        self.frame = 100
        self.scale = (50, 50)
        self.direction = hub.LEFT
        self.image_index = [pygame.image.load("imgs/Enemies/KoopaTroopa/KoopaT00.gif"),
                            pygame.image.load("imgs/Enemies/KoopaTroopa/KoopaT01.gif"),
                            pygame.image.load("imgs/Enemies/KoopaTroopa/ShellGreen.png")]

        super().__init__(hub=hub, x=x, y=y, direction=self.direction, name=self.name,
                         images=self.image_index, frame=self.frame, scale=self.scale)

    def stomped(self):
        self.velX = 0
        self.gravity = 0
        if self.isstomped:
            self.name = "shell"
            self.isstomped = False
            shelly = self.rect.bottom - 20
            shellx = self.rect.x
            self.image = self.image_index[2]
            self.image = pygame.transform.scale(self.image, (40, 35))
            self.rect = self.image.get_rect()
            self.rect.x = shellx
            self.rect.bottom = shelly
        self.state = self.hub.SHELL


class Paratroops(Enemy):
    def __init__(self, hub, x, y):
        self.name = "paratroop"
        self.frame = 100
        self.scale = (50, 50)
        self.direction = hub.RIGHT
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
