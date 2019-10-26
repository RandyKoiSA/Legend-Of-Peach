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
    def __init__(self, hub, level_name="1-1"):
        self.hub = hub
        self.screen = hub.main_screen
        self.controller = hub.controller
        self.camera = hub.camera
        self.gamemode = hub.gamemode
        self.level_name = level_name

        # Set up background
        self.bg_image = pygame.image.load(self.hub.game_levels[self.level_name]["background_image"])
        self.bg_rect = self.bg_image.get_rect()
        self.prep_bg_image()

        # Back Collision Group where all the background collisions will be store
        # This does not include brick collision.
        self.background_collisions = sprite.Group()

        # Player group spawn player in again if needed
        self.player_group = sprite.GroupSingle()

        # Gumba group spawn gumba when apporiate
        self.gumba_group = sprite.Group()
        #
        # Add gumba instances to the game
        for gumba in self.hub.game_levels[self.level_name]["gumba_group"]:
            self.gumba_group.add(Gumba(hub=hub, x=gumba["x"], y=gumba["y"]))

        # Add floor collision instances to the map
        for collision in self.hub.game_levels[self.level_name]["collision_group"]:
            self.background_collisions.add(FloorCollision(hub, (collision["x"], collision["y"]),
                                                          (collision["width"], collision["height"])))

        # Add player instance
        self.current_player = Player(hub)
        self.player_group.add(self.current_player)

    def run(self):
        """ Run through the loop process"""
        self.run_event()
        self.run_update()
        self.run_draw()

    def run_event(self):
        """ Run events """
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
                    self.controller.jump_pressed = True
                if event.key == K_LEFT or event.key == K_a:
                    self.controller.move_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    self.controller.move_right = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.controller.jump = False
                    self.controller.jump_pressed = False
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
        # Goomba collision with player
        for gumba in self.gumba_group:
            if gumba.rect.colliderect(self.player_group.sprite.rect):
                if self.player_group.sprite.rect.bottom < gumba.rect.top + 20:
                    self.player_group.sprite.rect.bottom = gumba.rect.top
                    gumba.state = self.hub.STOMPED
                    gumba.death_timer = pygame.time.get_ticks()
                    self.player_group.sprite.is_jumping = False

        # Player has hit the world's floor or wall such as pipes and stairs
        for collision in self.background_collisions:
            if collision.rect.colliderect(self.player_group.sprite.rect):
                # check if the player is standing on top
                if self.player_group.sprite.rect.bottom < collision.rect.top + 20:
                    self.player_group.sprite.rect.bottom = collision.rect.top
                    self.player_group.sprite.is_jumping = False
                    self.gamemode.mario_in_air = False
                else:
                    # check if the player hits the left wall
                    if self.player_group.sprite.rect.right < collision.rect.left + 20:
                        self.player_group.sprite.rect.right = collision.rect.left
                    # check if the player hits the right wall
                    if self.player_group.sprite.rect.left > collision.rect.right - 20:
                        self.player_group.sprite.rect.left = collision.rect.right

    def check_enemy_collision(self, enemy):
        """ Checks the enemy colliding with Pipes"""
        bg_collisions = pygame.sprite.spritecollide(enemy, self.background_collisions, False)
        if bg_collisions:
            for collision in bg_collisions:
                # Hits ground
                if enemy.rect.bottom < collision.rect.top + 20:
                    enemy.rect.bottom = collision.rect.top - 5
                # Hit side walls
                elif enemy.rect.right > collision.rect.left + 20 or enemy.rect.left < collision.rect.right - 20:
                    # Checks if player is not on top
                    if enemy.rect.bottom > collision.rect.top:
                        enemy.flip_direction()
                        enemy.rect.bottom = enemy.rect.bottom - enemy.gravity


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

    def update_player_group(self):
        for player in self.player_group:
            player.update()

    def update_enemy_group(self):
        """ updating the gumba group """
        for enemy in self.gumba_group:
            self.check_enemy_collision(enemy=enemy)

            enemy.update()
            if enemy.kill:
                try:
                    self.gumba_group.remove(enemy)
                    print("Gumba ded")
                except AssertionError:
                    print("ERROR: Remove Gumba does not exist")
                    pass

    def draw_player_group(self):
        """ Draw the player onto the screen """
        for player in self.player_group:
            player.draw()

    def draw_enemy_group(self):
        """  Draw all enemies onto the screen"""
        # Draw all the gumbas onto the screen
        for gumba in self.gumba_group:
            gumba.draw()

    def draw_world_collision_group(self):
        """ Draw the collision lines """
        for collision in self.background_collisions:
            collision.draw()
