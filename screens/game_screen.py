import pygame
import sys
from pygame.locals import *
from obstacles.floor_collision import FloorCollision
from obstacles.teleporter import Teleport
from player import Player
from pygame import sprite
from AI.gumba import Gumba
from AI.gumba import Koopatroops
import json


class GameScreen:
    """ Game Screen runs the game. """
    def __init__(self, hub, level_name="1-1-1"):
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

        # Teleporter Group
        self.teleporter_group = sprite.Group()

        # Player group spawn player in again if needed
        self.player_group = sprite.GroupSingle()

        # Gumba group spawn gumba when appropriate
        self.enemy_group = sprite.Group()

        # For red or green shells
        self.shells_group = sprite.Group()

        # Projectiles (Shell, Fire, Bullet bills)
        self.projectile_group = sprite.Group()

        # Enemies set to die
        self.death_group = sprite.Group()

        try:
            for gumba in self.hub.game_levels[self.level_name]["gumba_group"]:
                self.enemy_group.add(Gumba(hub=hub, x=gumba["x"], y=gumba["y"]))
        except Exception:
            print('no gumba exist within this level')

        try:
            for koopatroop in self.hub.game_levels[self.level_name]["koopatroop_group"]:
                self.enemy_group.add(Koopatroops(hub=hub, x=koopatroop["x"], y=koopatroop["y"]))
        except Exception:
            print('no koopatroop exist within this level')

        # Add floor collision instances to the map
        try:
            for collision in self.hub.game_levels[self.level_name]["collision_group"]:
                self.background_collisions.add(FloorCollision(hub, (collision["x"], collision["y"]),
                                                              (collision["width"], collision["height"])))
        except Exception:
            print('no collision found in within this level')

        # Add teleport instances
        try:
            for teleporter in self.hub.game_levels[self.level_name]["teleporter"]:
                self.teleporter_group.add(Teleport(hub, teleporter["x"], teleporter["y"], teleporter["level_name"],
                                                   teleporter["world_offset"]))
        except Exception:
            print('no teleporter found within this level')

        # Add player instance
        self.player_spawn_point = self.hub.game_levels[self.level_name]["spawn_point"]
        self.current_player = Player(hub, self.player_spawn_point[0], self.player_spawn_point[1])
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
                if event.key == K_UP or event.key == K_w:
                    self.controller.up = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.controller.jump = False
                    self.controller.jump_pressed = False
                if event.key == K_LEFT or event.key == K_a:
                    self.controller.move_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    self.controller.move_right = False
                if event.key == K_UP or event.key == K_w:
                    self.controller.up = False

    def run_update(self):
        self.update_player_group()
        self.update_teleporter_group()
        self.update_camera()
        self.update_world_collision()
        if not self.hub.modeFreeze:
            self.update_enemy_group()
            self.update_death_group()
            self.update_projectile_group()
            self.update_shell_group()


    def run_draw(self):
        # Draw background image
        self.screen.blit(self.bg_image, self.bg_rect)

        # Draw test collision boxes
        self.draw_world_collision_group()

        # Draw teleporter collision boxes
        self.draw_teleporter_group()

        # Draw gumba
        self.draw_enemy_group()

        # Draw player
        self.draw_player_group()

        # Draw the Death Enemies
        self.draw_death_group()

        # Draw the Shells
        self.draw_shell_group()

        # Draw the Projectiles
        self.draw_projectile_group()

    def prep_bg_image(self):
        # Scale the background image
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_rect.width * 3 + 50,
                                                               self.bg_rect.height * 3 + 50))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.bottomleft = self.screen.get_rect().bottomleft

    def update_world_collision(self):
        # Enemy collision with player
        for shell in self.shells_group:
            if shell.rect.colliderect(self.player_group.sprite.rect):
                shell.move = self.player_group.sprite.mario_facing_direction
                shell.state = self.hub.SLIDE
                if self.player_group.sprite.rect.bottom < shell.rect.top + 20:
                    self.player_group.sprite.reset_bounce()
                    self.player_group.sprite.bounce()
                shell.kill()
                self.projectile_group.add(shell)

        for enemy in self.enemy_group:
            if enemy.rect.colliderect(self.player_group.sprite.rect):
                if self.player_group.sprite.rect.bottom < enemy.rect.top + 20:
                    self.player_group.sprite.reset_bounce()
                    self.player_group.sprite.bounce()
                    enemy.state = self.hub.STOMPED
                    enemy.isstomped = True
                    enemy.death_timer = pygame.time.get_ticks()
                    enemy.kill()
                    if enemy.name == "koopatroop":
                        self.shells_group.add(enemy)
                    else:
                        self.death_group.add(enemy)
                    #self.player_group.sprite.is_jumping = False
                else:
                    # If Mario collides in x direction
                    if self.player_group.sprite.rect.right < enemy.rect.left + 20:
                        self.player_group.sprite.die()
                    elif self.player_group.sprite.rect.left > enemy.rect.right - 20:
                        self.player_group.sprite.die()

        # Player has hit the world's floor or wall such as pipes and stairs
        for collision in self.background_collisions:
            if collision.rect.colliderect(self.player_group.sprite.rect):
                # check if the player is standing on top
                if self.player_group.sprite.rect.bottom < collision.rect.top + 20:
                    self.player_group.sprite.rect.bottom = collision.rect.top
                    self.player_group.sprite.reset_jump()
                    self.player_group.sprite.reset_bounce()
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
        enemy_collisions = pygame.sprite.spritecollide(enemy, self.enemy_group, False)
        if enemy_collisions:
            for enemies in enemy_collisions:
                if enemy.rect.right > enemies.rect.left + 20 or enemy.rect.left < enemies.rect.right - 20:
                    if enemy != enemies:
                        # Checks if enemy colliding with other enemy
                        enemy.flip_direction()

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
                        # enemy.rect.bottom = enemy.rect.bottom - enemy.gravity

    def update_camera(self):
        # update the bg image off set
        self.bg_rect.x = self.camera.world_offset_x * -1

        # checks if the background is at its end and stop camera movement
        if self.screen.get_rect().right > self.bg_rect.right:
            self.bg_rect.right = self.screen.get_rect().right
            self.camera.camera_hit_right_screen = True
        else:
            self.camera.camera_hit_right_screen = False

        # update the collisions off set
        for collision in self.background_collisions:
            collision.rect.x = collision.original_pos[0] - self.camera.world_offset_x

        for enemy in self.enemy_group:
            enemy.rect.x = enemy.original_pos[0] - self.camera.world_offset_x

        for shell in self.shells_group:
            shell.rect.x = shell.original_pos[0] - self.camera.world_offset_x

        for projectile in self.projectile_group:
            projectile.rect.x = projectile.original_pos[0] - self.camera.world_offset_x

        for dead in self.death_group:
            dead.rect.x = dead.original_pos[0] - self.camera.world_offset_x

    def update_player_group(self):
        for player in self.player_group:
            player.update()

    def update_enemy_group(self):
        """ updating the gumba group """
        for enemy in self.enemy_group:
            self.check_enemy_collision(enemy=enemy)
            enemy.update()

    def update_death_group(self):
        """ Updating the soon to die Enemy Group"""
        for enemy in self.death_group:
            enemy.update()
            if enemy.killed:
                try:
                    self.death_group.remove(enemy)
                    print(enemy.name + " is ded")
                except AssertionError:
                    print("ERROR: Remove Gumba does not exist")
                    pass

    def update_shell_group(self):
        for shell in self.shells_group:
            shell.update()

    def update_projectile_group(self):
        for projectile in self.projectile_group:
            projectile.update()

    def draw_player_group(self):
        """ Draw the player onto the screen """
        for player in self.player_group:
            player.draw()

    def draw_enemy_group(self):
        """  Draw all enemies onto the screen"""
        # Draw all the gumbas onto the screen
        for gumba in self.enemy_group:
            gumba.draw()

    def draw_death_group(self):
        """ Draw all the soon to die enemies"""
        for enemy in self.death_group:
            enemy.draw()

    def draw_shell_group(self):
        for shell in self.shells_group:
            shell.draw()

    def draw_projectile_group(self):
        for projectile in self.projectile_group:
            projectile.draw()

    def draw_world_collision_group(self):
        """ Draw the collision lines """
        for collision in self.background_collisions:
            collision.draw()

    def update_teleporter_group(self):
        for teleporter in self.teleporter_group:
            teleporter.update(self.player_group.sprite.rect)

    def draw_teleporter_group(self):
        for teleporter in self.teleporter_group:
            teleporter.draw()
