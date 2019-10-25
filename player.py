import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """ Player class, where the player will control """
    def __init__(self, hub):
        """ Initialize default values """
        super().__init__()
        self.screen = hub.main_screen
        self.screen_rect = self.screen.get_rect()
        self.controller = hub.controller
        self.camera = hub.camera

        # players image and collision
        self.image = pygame.image.load("imgs/Cut-Sprites-For-Mario/Characters/219_mario_idle.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 550

        # player's fall rate, run velocity, jumping state
        self.gravity = 10
        self.velocity = 10
        self.is_jumping = False

        # Get mario time when jumping
        self.jump_initial_time = 0
        self.jump_max_air_time = 300    # How long the player will keep jumping
        self.jump_velocity = 25     # How fast the player will jump

    def update(self):
        """ Update the player logic """
        # Apply gravity
        self.rect.y += self.gravity

        # Apply movement
        if self.controller.move_right:
            self.rect.x += self.velocity
        if self.controller.move_left:
            self.rect.x -= self.velocity
        if self.controller.jump:
            self.controller.jump = False
            if not self.is_jumping:
                self.jump()

        # Check if the player is jumping
        if self.is_jumping:
            if pygame.time.get_ticks() < self.jump_initial_time:
                self.rect.y -= self.jump_velocity

        self.check_collision()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_collision(self):
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

    def jump(self):
        self.is_jumping = True
        self.jump_initial_time = pygame.time.get_ticks() + self.jump_max_air_time

    def throw(self):
        pass

    def get_bigger(self):
        pass

    def get_smaller(self):
        pass

    def die(self):
        pass

    def become_fire_mario(self):
        pass
