import pygame
import sys
from pygame.locals import *
from obstacles.floor_collision import FloorCollision
from player import Player

class GameScreen:
    """ Game Screen runs the game. """
    def __init__(self, hub):
        self.screen = hub.main_screen
        self.controller = hub.controller
        self.camera = hub.camera

        # Set up background
        self.bg_image = pygame.image.load('imgs/level_one_map.png')
        self.bg_rect = self.bg_image.get_rect()
        self.prep_bg_image()

        # Add floor collision
        self.collision = FloorCollision(hub, (0, self.bg_rect.bottom - 75), (3325, 75))

        # Add player
        self.player = Player(hub)

    def run(self):
        self.run_event()
        self.run_update()
        self.run_draw()

    def run_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    self.controller.jump = True
                if event.key == K_LEFT or event.key == K_a:
                    self.controller.move_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    self.controller.move_right = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.controller.jump = False
                if event.key == K_LEFT or event.key == K_a:
                    self.controller.move_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    self.controller.move_right = False

    def run_update(self):
        self.player.update()

        self.camera_update()
        self.check_collision()

    def run_draw(self):
        self.screen.blit(self.bg_image, self.bg_rect)
        self.collision.draw()
        self.player.draw()

    def prep_bg_image(self):
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_rect.width * 3 + 50,
                                                               self.bg_rect.height * 3 + 50))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.bottomleft = self.screen.get_rect().bottomleft

    def check_collision(self):
        # Player has hit the ground
        if self.collision.rect.colliderect(self.player):
            self.player.jump_left = 1
            self.player.rect.bottom = self.collision.rect.top

    def camera_update(self):
        self.bg_rect.x = self.camera.world_offset_x * -1
        self.collision.rect.x = self.collision.original_pos[0] - self.camera.world_offset_x