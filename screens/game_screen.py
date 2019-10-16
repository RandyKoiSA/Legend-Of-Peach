import pygame
import sys
from pygame.locals import *
from obstacles.floor_collision import FloorCollision
from player import Player
from pygame import sprite
from AI.gumba import Gumba
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
        self.background_collisions = sprite.Group()

        # Player group spawn player in again if needed
        self.player_group = sprite.GroupSingle()

        # Gumba group spawn gumba when apporiate
        self.gumba_group = sprite.Group()

        # Add gumba instances to the game
        for gumba in self.json_levels["level_one"]["gumba_group"]:
            self.gumba_group.add(Gumba(hub=hub, x=gumba["x"], y=gumba["y"]))

        # Add floor collision instances to the map
        for collision in self.json_levels["level_one"]["collision_group"]:
            self.background_collisions.add(FloorCollision(hub, (collision["x"], collision["y"]),
                                                          (collision["width"], collision["height"])))

        # Add player instance
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
        self.update_enemy_group()
        self.update_camera()
        self.update_world_collision()

    def run_draw(self):
        # Draw background image
        self.screen.blit(self.bg_image, self.bg_rect)

        # Draw test collision boxes
        self.draw_world_collision_group()

        # Draw gumba
        self.draw_enemy_group()

        # Draw player
        self.draw_player_group()

    def prep_bg_image(self):
        # Scale the background image
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_rect.width * 3 + 50,
                                                               self.bg_rect.height * 3 + 50))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.bottomleft = self.screen.get_rect().bottomleft

    def update_world_collision(self):
        # Player has hit the world's floor or wall such as pipes and stairs
        for collision in self.background_collisions:
            if collision.rect.colliderect(self.player_group.sprite.rect):
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

    def check_enemy_x_collide(self, enemy):
        """ Checks the enemy colliding with Pipes"""
        collide_bg = pygame.sprite.spritecollideany(enemy, self.background_collisions)
        if collide_bg:
            print(collide_bg.rect)
            enemy.move = not enemy.move

    def update_camera(self):
        # update the bg image off set
        self.bg_rect.x = self.camera.world_offset_x * -1

        # checks if the background is at its end and stop camera movement
        if self.screen.get_rect().right > self.bg_rect.right:
            self.bg_rect.right = self.screen.get_rect().right
            self.camera.camera_hit_right_screen = True

        # update the collisions off set
        for collision in self.background_collisions:
            collision.rect.x = collision.original_pos[0] - self.camera.world_offset_x

    def get_levels(self):
        """ Grab the level data from the JSON file"""
        filename = 'levels.json'
        with open(filename, 'r') as read_file:
            data = json.load(read_file)
            return data

    def update_player_group(self):
        for player in self.player_group:
            player.update()

    def update_enemy_group(self):
        """ updating the gumba group """
        for gumba in self.gumba_group:
            self.check_enemy_x_collide(gumba)
            gumba.update()
            if gumba.kill:
                try:
                    self.gumba_group.remove(gumba)
                    print("Gumba ded")
                except AssertionError:
                    print("ERROR: Remove Gumba does not exist")
                    pass

    def draw_player_group(self):
        for player in self.player_group:
            player.draw()

    def draw_enemy_group(self):
        for gumba in self.gumba_group:
            gumba.draw()

    def draw_world_collision_group(self):
        for collision in self.background_collisions:
            collision.draw()
