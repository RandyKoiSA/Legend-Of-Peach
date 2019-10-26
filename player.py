import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """ Player class, where the player will control """
    def __init__(self, hub):
        """ Initialize default values """
        super().__init__()
        self.hub = hub
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.controller = hub.controller
        self.camera = hub.camera
        self.gamemode = hub.gamemode

        self.mario_motion_state = "idle"
        self.mario_upgrade_state = "regular"

        # keep track on what image of multiple images
        self.index = 0
        self.change_freq = 120
        self.player_clock = pygame.time.get_ticks() + self.change_freq

        # regular mario image and collision
        self.image_idle = pygame.image.load("imgs/Mario/RegularMario/MarioStanding.png")
        self.image_run = [pygame.image.load('imgs/Mario/RegularMario/MarioRun01.gif'),
                          pygame.image.load('imgs/Mario/RegularMario/MarioRun02.gif'),
                          pygame.image.load('imgs/Mario/RegularMario/MarioRun03.gif')]
        self.image_jump = pygame.image.load('imgs/Mario/RegularMario/MarioJumping.png')

        # prep mario image
        self.prep_mario_images()

        # get current image and rect
        self.current_image = self.image_idle
        self.rect = self.current_image.get_rect()

        # Set initial position
        self.rect.x = 50
        self.rect.y = 550

        # player's fall rate, run velocity, jumping state
        self.gravity = 10
        self.velocity = 10
        self.is_jumping = False

        # Get mario time when jumping
        self.counter_jump = 0
        self.jump_max_height = 400
        self.jump_velocity = 25     # How fast the player will jump

        self.is_dead = False

    def update(self):
        """ Update the player logic """
        # Check if mario is jumping
        self.update_state()

        # Apply gravity
        self.rect.y += self.gravity

        # Apply movement
        if self.controller.move_right:
            self.rect.x += self.velocity
            self.mario_motion_state = "running"
        if self.controller.move_left:
            self.rect.x -= self.velocity
            self.mario_motion_state = "running"
        if not self.controller.move_left and not self.controller.move_right:
            if not self.gamemode.mario_in_air:
                self.mario_motion_state = "idle"
                self.reset_animations()
        if self.controller.jump:
            # turn off controller jump to prevent holding jump space bar
            self.controller.jump = False
            if not self.is_jumping:
                self.jump()

        # Check if the player is jumping
        if self.is_jumping:
            if self.counter_jump < self.jump_max_height:
                self.counter_jump += self.jump_velocity
                self.rect.y -= self.jump_velocity
            if self.counter_jump > self.jump_max_height:
                self.is_jumping = False

        self.check_collision()

    def draw(self):
        # draw current image
        self.screen.blit(self.current_image, self.rect)

    def check_collision(self):
        """ Check player's collision with actor and other objects """
        # Checks if the player hits the left screen
        if self.rect.left < self.screen_rect.left:
            self.rect.left = self.screen_rect.left

        # Checks if the player goes pass the right screen
        # If so, move the world camera off set
        if self.rect.right > self.screen_rect.right / 2:
            # Move camera and set player to the middle of screen
            if not self.camera.camera_hit_right_screen:
                self.rect.right = self.screen_rect.width / 2

            # If camera hits the very right screen, player can move upon half the screen
            if self.rect.right > self.screen_rect.right:
                self.rect.right = self.screen_rect.right
                self.camera.player_hit_right_screen = True
            elif self.rect.right < self.screen_rect.right:
                self.camera.player_hit_right_screen = False

            # Move camera respective to player movement
            self.camera.moveCamera(self.velocity)

        # Check if the player is fallen off the screen (mario is dead)
        if self.rect.top > self.screen_rect.bottom:
            self.die()

    def jump(self):
        self.is_jumping = True
        self.gamemode.mario_in_air = True
        self.mario_motion_state = "jumping"

    def throw(self):
        pass

    def get_bigger(self):
        pass

    def get_smaller(self):
        pass

    def die(self):
        # play mario is dying animation
        if not self.is_dead:
            print("mario is dead")
            self.gamemode.lives -= 1
            self.gamemode.mario_is_dead = True
            self.is_dead = True

    def become_fire_mario(self):
        pass

    def prep_mario_images(self):
        # Adjustment to mario images
        # adjust regular mario images
        self.image_idle = pygame.transform.scale(self.image_idle, (50, 50))
        for i in range(len(self.image_run)):
            self.image_run[i] = pygame.transform.scale(self.image_run[i], (50, 50))
        self.image_jump = pygame.transform.scale(self.image_jump, (50, 50))

    def reset_jump(self):
        """ Reset mario's jump when mario hits the ground"""
        self.gamemode.mario_in_air = False
        self.is_jumping = False
        self.counter_jump = 0

    def update_state(self):
        """ Update state determine what state the player is in """

        if self.mario_motion_state is "jumping" or self.gamemode.mario_in_air:
            self.current_image = self.image_jump
        else:
            if self.mario_motion_state is "idle":
                self.current_image = self.image_idle
            if self.mario_motion_state is "running":
                # start timer
                if pygame.time.get_ticks() > self.player_clock:
                    self.player_clock = pygame.time.get_ticks() + self.change_freq
                    self.index += 1
                    self.index %= len(self.image_run)
                    self.current_image = self.image_run[self.index]

        # self.rect = self.current_image.get_rect()

    def reset_animations(self):
        self.index = 0
        self.player_clock = pygame.time.get_ticks()

