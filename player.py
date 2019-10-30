import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """ Player class, where the player will control """
    def __init__(self, hub, pos_x= 50, pos_y=50):
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
        self.mario_facing_direction = hub.RIGHT
        self.mario_image_flipped = False

        # keep track on what image of multiple images
        self.index = 0
        self.change_freq = 120
        self.player_clock = pygame.time.get_ticks() + self.change_freq

        # regular mario image
        self.regular_image_idle = [pygame.image.load("imgs/Mario/RegularMario/MarioStanding.png")]
        self.regular_image_run = [pygame.image.load('imgs/Mario/RegularMario/MarioRun01.gif'),
                          pygame.image.load('imgs/Mario/RegularMario/MarioRun02.gif'),
                          pygame.image.load('imgs/Mario/RegularMario/MarioRun03.gif')]
        self.regular_image_jump = [pygame.image.load('imgs/Mario/RegularMario/MarioJumping.png')]

        # super mario image
        self.super_image_idle = [pygame.image.load("imgs/Mario/SuperMario/SuperMarioStanding.png")]
        self.super_image_run = [pygame.image.load("imgs/Mario/SuperMario/SM_run_01.gif"),
                                pygame.image.load("imgs/Mario/SuperMario/SM_run_02.gif"),
                                pygame.image.load("imgs/Mario/SuperMario/SM_run_03.gif")]
        self.super_image_jump = [pygame.image.load("imgs/Mario/SuperMario/SuperMarioJumping.png")]

        # fiery mario image
        self.fiery_image_idle = [pygame.image.load('imgs/Mario/FieryMario/FieryMarioStanding.png')]
        self.fiery_image_run = [pygame.image.load('imgs/Mario/FieryMario/FieryMarioRunning_01.gif'),
                                pygame.image.load('imgs/Mario/FieryMario/FieryMarioRunning_02.gif'),
                                pygame.image.load('imgs/Mario/FieryMario/FieryMarioRunning_03.gif')]
        self.fiery_image_jump = [pygame.image.load('imgs/Mario/FieryMario/FieryMarioJumping.png')]

        # prep mario image
        self.prep_mario_images()

        # get current list, image, and rect using
        self.current_list = self.regular_image_idle
        self.current_image = self.current_list[self.index]
        self.rect = self.current_image.get_rect()

        # Set initial position
        self.rect.x = pos_x
        self.rect.y = pos_y

        # player's fall rate, run velocity, jumping state
        self.gravity = self.hub.GRAVITY
        self.velocity = 10
        self.is_jumping = False
        self.is_bouncing = False

        # Get mario time when jumping
        self.counter_jump = 0
        self.jump_max_height = 350
        self.jump_velocity = 25     # How fast the player will jump
        self.counter_bounce = 0
        self.bounce_max_height = 100
        self.bounce_velocity = 35

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
            self.mario_facing_direction = self.hub.RIGHT

        if self.controller.move_left:
            self.rect.x -= self.velocity
            self.mario_motion_state = "running"
            self.mario_facing_direction = self.hub.LEFT

        if not self.controller.move_left and not self.controller.move_right:
            if not self.gamemode.mario_in_air:
                self.mario_motion_state = "idle"

                self.reset_animations()
        if self.controller.jump:
            # turn off controller jump to prevent holding jump space bar
            self.controller.jump = False
            if not self.is_jumping or not self.is_bouncing:
                self.jump()

        # Check if the player is jumping
        if self.is_jumping:
            if self.counter_jump < self.jump_max_height:
                self.counter_jump += self.jump_velocity
                self.rect.y -= self.jump_velocity
            if self.counter_jump > self.jump_max_height:
                self.is_jumping = False

        if self.is_bouncing:
            if self.counter_bounce < self.bounce_max_height:
                self.counter_bounce += self.bounce_velocity
                self.rect.y -= self.bounce_velocity
            if self.counter_bounce > self.bounce_max_height:
                self.is_bouncing = False

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

    def bounce(self):
        self.is_bouncing = True
        self.gamemode.mario_in_air = True
        self.mario_motion_state = "jumping"
        print("Mario Bounced off AI")

    def throw(self):
        pass

    def get_bigger(self):
        # if mario is regular change to super
        if self.mario_upgrade_state is "regular":
            self.mario_upgrade_state = "super"
        # if mario is super or fiery, add points to score
        elif self.mario_upgrade_state is "super" or self.mario_upgrade_state is "fiery":
            # TODO add score to gamemode
            pass

    def get_smaller(self):
        # if mario is regular, mario dies
        if self.mario_upgrade_state is "regular":
            self.die()
        # if mario is super, change to regular mario
        elif self.mario_upgrade_state is "super":
            self.mario_upgrade_state = "regular"
        # if mario is fiery, change to super mario
        elif self.mario_upgrade_state is "fiery":
            self.mario_upgrade_state = "fiery"

    def die(self):
        # play mario is dying animation
        if not self.is_dead:
            print("mario is dead")
            self.gamemode.lives -= 1
            self.gamemode.mario_is_dead = True
            self.is_dead = True

    def become_fire_mario(self):
        # if mario is regular, turn into super mario
        if self.mario_upgrade_state is "regular":
            self.mario_upgrade_state = "super"
        # if mario is super, turn into fiery mario
        elif self.mario_upgrade_state is "super":
            self.mario_upgrade_state = "fiery"
        # if mario is fiery, add points to score
        elif self.mario_upgrade_state is "fiery":
            # add points to score
            pass
        else:
            print('ERROR: become_fire_mario(), mario upgrades state does not exist. ')

    def set_image_direction(self):
        if self.mario_facing_direction == self.hub.LEFT:
            self.current_image = pygame.transform.flip(self.current_image, True, False)

    def prep_mario_images(self):
        """ Adjustment images """
        # Adjusting regular mario images
        for i in range(len(self.regular_image_idle)):
            self.regular_image_idle[i] = pygame.transform.scale(self.regular_image_idle[i], (50, 50))
        for i in range(len(self.regular_image_run)):
            self.regular_image_run[i] = pygame.transform.scale(self.regular_image_run[i], (50, 50))
        for i in range(len(self.regular_image_jump)):
            self.regular_image_jump[i] = pygame.transform.scale(self.regular_image_jump[i], (50, 50))

        # Adjusting super mario images
        for i in range(len(self.super_image_idle)):
            self.super_image_idle[i] = pygame.transform.scale(self.super_image_idle[i], (50, 100))
        for i in range(len(self.super_image_run)):
            self.super_image_run[i] = pygame.transform.scale(self.super_image_run[i], (50, 100))
        for i in range(len(self.super_image_jump)):
            self.super_image_jump[i] = pygame.transform.scale(self.super_image_jump[i], (50, 100))

        # Adjusting fiery mario images
        for i in range(len(self.fiery_image_idle)):
            self.fiery_image_idle[i] = pygame.transform.scale(self.fiery_image_idle[i], (50, 100))
        for i in range(len(self.fiery_image_jump)):
            self.fiery_image_jump[i] = pygame.transform.scale(self.fiery_image_jump[i], (50, 100))
        for i in range(len(self.fiery_image_run)):
            self.fiery_image_run[i] = pygame.transform.scale(self.fiery_image_run[i], (50, 100))

    def reset_jump(self):
        """ Reset mario's jump when mario hits the ground"""
        self.gamemode.mario_in_air = False
        self.is_jumping = False
        self.counter_jump = 0

    def reset_bounce(self):
        """Reset Mario's bounce when mario hits the ground or enemy"""
        self.gamemode.mario_in_air = False
        self.is_bouncing = False
        self.counter_bounce = 0

    def update_state(self):
        """ Update state determine what state the player is in """
        if pygame.time.get_ticks() > self.player_clock:
            self.player_clock = pygame.time.get_ticks() + self.change_freq
            self.index += 1
            self.index %= len(self.current_list)
            self.current_image = self.current_list[self.index]
            self.set_image_direction()

        if self.mario_motion_state is "jumping" or self.gamemode.mario_in_air:
            # jumping as regular
            if self.mario_upgrade_state is "regular":
                self.current_list = self.regular_image_jump
            # jumping as super
            elif self.mario_upgrade_state is "super":
                self.current_list = self.super_image_jump
            # jumping as fiery
            elif self.mario_upgrade_state is "fiery":
                self.current_list = self.fiery_image_jump
        else:
            if self.mario_motion_state is "idle":
                if self.mario_upgrade_state is "regular":
                    self.current_list = self.regular_image_idle
                elif self.mario_upgrade_state is "super":
                    self.current_list = self.super_image_idle
                elif self.mario_upgrade_state is "fiery":
                    self.current_list = self.fiery_image_idle
                else:
                    print('ERROR: mario upgrade state does not exist. ')
            if self.mario_motion_state is "running":
                if self.mario_upgrade_state is "regular":
                    self.current_list = self.regular_image_run
                elif self.mario_upgrade_state is "super":
                    self.current_list = self.super_image_run
                elif self.mario_upgrade_state is "fiery":
                    self.current_list = self.fiery_image_run
                else:
                    print('ERROR: mario upgrade stats does not exist. ')

        self.update_rect()

    def reset_animations(self):
        self.index = 0
        self.player_clock = pygame.time.get_ticks()

    def update_rect(self):
        position_x = self.rect.x
        position_y = self.rect.bottom
        self.rect = self.current_image.get_rect()
        self.rect.x = position_x
        self.rect.bottom = position_y

