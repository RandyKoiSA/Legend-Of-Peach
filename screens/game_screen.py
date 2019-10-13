import pygame
import sys
from pygame.locals import *
from obstacles.floor_collision import FloorCollision
from player import Player
from pygame.sprite import Group, GroupSingle
import json


class GameScreen:
    """ Game Screen runs the game. """
    def __init__(self, hub):
        self.screen = hub.main_screen
        self.controller = hub.controller
        self.camera = hub.camera
        self.gamemode = hub.gamemode

        # Load json level
        self.json_levels = self.get_levels()

        # Set up background
        self.bg_image = pygame.image.load(self.json_levels["level_one"]["background_image"])
        self.bg_rect = self.bg_image.get_rect()
        self.prep_bg_image()

        # Back Collision Group where all the background collisions will be store
        # This does not include brick collision.
        self.background_collisions = Group()

        # Player group spawn player in again if needed
        self.player_group = GroupSingle()

        # Add instances
        # Add floor collisions instances to the map
        for collision in self.json_levels["level_one"]["collision_group"]:
            self.background_collisions.add(FloorCollision(hub, (collision["x"], collision["y"]),
                                                          (collision["width"], collision["height"])))
        # Add player
        self.player_group.add(Player(hub))

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
        self.update_player_group()

        self.update_camera()
        self.update_collision()

    def run_draw(self):
        self.screen.blit(self.bg_image, self.bg_rect)
        # Draw test collision boxes
        for collision in self.background_collisions:
            collision.draw()
        self.draw_player_group()

    def prep_bg_image(self):
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_rect.width * 3 + 50,
                                                               self.bg_rect.height * 3 + 50))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.bottomleft = self.screen.get_rect().bottomleft

    def update_collision(self):
        # Player has hit the ground or wall
        for collision in self.background_collisions:
            if collision.rect.colliderect(self.player_group.sprite):
                # check if the player is standing on top
                if self.player_group.sprite.rect.bottom < collision.rect.top + 20:
                    self.player_group.sprite.rect.bottom = collision.rect.top
                    self.player_group.sprite.jump_left = 1
                else:
                    # check if the player hits the left wall
                    if self.player_group.sprite.rect.right < collision.rect.left + 20:
                        self.player_group.sprite.rect.right = collision.rect.left
                    # check if the player hits the right wall
                    if self.player_group.sprite.rect.left > collision.rect.right - 20:
                        self.player_group.sprite.rect.left = collision.rect.right


    def update_camera(self):
        self.bg_rect.x = self.camera.world_offset_x * -1
        for collision in self.background_collisions:
            collision.rect.x = collision.original_pos[0] - self.camera.world_offset_x

    def get_levels(self):
        filename = 'levels.json'
        with open(filename, 'r') as read_file:
            data = json.load(read_file)
            return data

    def update_player_group(self):
        for player in self.player_group:
            player.update()

    def draw_player_group(self):
        for player in self.player_group:
            player.draw()
