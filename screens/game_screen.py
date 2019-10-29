import pygame
import sys
from pygame.locals import *
from obstacles.floor_collision import FloorCollision
from obstacles.teleporter import Teleport
from player import Player
from pygame import sprite
from AI.enemy import Gumba
from AI.enemy import Koopatroops
from obstacles.bricks import Bricks
from items.coins import Coins
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

        # Bounce physics
        self.counter_bounce = 0
        self.bounce_max_height = 100
        self.bounce_velocity = 35

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

        # Bricks to be spawned
        self.brick_group = sprite.Group()

        # Coins to be spawned
        self.coin_group = sprite.Group()

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

        # Add Brick Instance
        try:
            print(len(self.hub.game_levels[self.level_name]["bricks"]))
            for brick in self.hub.game_levels[self.level_name]["bricks"]:
                self.brick_group.add(Bricks(hub=hub, x=brick["x"], y=brick["y"], insides=brick["inside"],
                                            powerup_group=brick["powerup"], name=brick["name"]))
        except Exception:
            print('no bricks exist within this level')

        # Add Coin Instance
        try:
            print(len(self.hub.game_levels[self.level_name]["coins"]))
            for coin in self.hub.game_levels[self.level_name]["coins"]:
                self.coin_group.add(Coins(hub=hub, x=coin["x"], y=coin["y"], name=coin["name"], state="resting"))
        except Exception:
            print('no coins exist within this level')

        # Add Brick Group Instance
        try:
            print(len(self.hub.game_levels[self.level_name]["brick_group"]))
            for brickset in self.hub.game_levels[self.level_name]["brick_group"]:
                for i in range(0, brickset["Row"]):
                    print(str(i))
                    for j in range(0, brickset["Col"]):
                        print(str(j))
                        row = i * 50
                        col = j * 50
                        print(str(row) + " equals" + str(col))
                        self.brick_group.add(Bricks(hub=hub, x=row, y=col, insides="None",
                                                    powerup_group="Brick", name="Brick"))
        except Exception:
            print('no brickset exist within this level')

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
                if event.key == K_9:
                    self.hub.screen_selector = 1
                if event.key == K_8:
                    self.get_coordinates()
                if event.key == K_7:
                    self.controller.toggle_grid = not self.controller.toggle_grid
                if event.key == K_6:
                    self.controller.toggle_mouse_coordinates = not self.controller.toggle_mouse_coordinates
                if event.key == K_1:
                    # Get point A
                    self.set_point_a()
                if event.key == K_2:
                    # Get point B
                    self.set_point_b()
                if event.key == K_3:
                    # Print description
                    self.print_description()
                    pass

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
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.controller.developer_mode:
                    self.move_player(mouse_x, mouse_y)

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
            self.update_brick_group()
            self.update_coin_group()


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

        # Draw the Bricks
        self.draw_brick_group()

        # Draw the Coins
        self.draw_coin_group()

        if self.controller.toggle_grid:
            self.draw_debug_line()

        if self.controller.toggle_mouse_coordinates:
            self.draw_mouse_coordinates()


    def prep_bg_image(self):
        # Scale the background image
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_rect.width * 3 + 50,
                                                               self.bg_rect.height * 3 + 50))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.bottomleft = self.screen.get_rect().bottomleft

    def update_world_collision(self):
        # Brick Collision with player
        for brick in self.brick_group:
            if brick.rect.colliderect(self.player_group.sprite.rect):
                if self.player_group.sprite.rect.bottom <= brick.rect.top + 25:
                    self.player_group.sprite.rect.bottom = brick.rect.top
                    self.player_group.sprite.reset_jump()
                    self.player_group.sprite.reset_bounce()
                # check if the player hits the left wall
                elif self.player_group.sprite.rect.right < brick.rect.left + 20:
                    self.player_group.sprite.rect.right = brick.rect.left
                # check if the player hits the right wall
                elif self.player_group.sprite.rect.left > brick.rect.right - 20:
                    self.player_group.sprite.rect.left = brick.rect.right

                else:
                    self.player_group.sprite.counter_jump = self.player_group.sprite.jump_max_height
                    if brick.state == self.hub.RESTING:
                        brick.state = self.hub.BUMPED

        # Coin Collision with player
        for coin in self.coin_group:
            if coin.rect.colliderect(self.player_group.sprite.rect) and coin.state == "resting":
                coin.kill()
                self.hub.score += 200

        # Enemy collision with player
        for shell in self.shells_group:
            if shell.rect.colliderect(self.player_group.sprite.rect):
                shell.move = self.player_group.sprite.mario_facing_direction
                shell.state = self.hub.SLIDE
                if shell.move == self.hub.LEFT:
                    shell.rect.right = self.player_group.sprite.rect.left
                else:
                    shell.rect.left = self.player_group.sprite.rect.right
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

    def check_projectile_collision(self, projectile):
        bg_collisions = pygame.sprite.spritecollide(projectile, self.background_collisions, False)
        enemy_collisions = pygame.sprite.spritecollide(projectile, self.enemy_group, False)
        player_collision = pygame.sprite.spritecollide(projectile, self.player_group, False)

        if player_collision:
            for player in player_collision:
                if projectile.rect.right > player.rect.left or projectile.rect.left < player.rect.right:
                    player.die()

        if enemy_collisions:
            for enemies in enemy_collisions:
                if projectile.rect.right > enemies.rect.left + 20 or projectile.rect.left < enemies.rect.right - 20:
                    enemies.state = self.hub.HIT
                    enemies.kill()
                    self.death_group.add(enemies)

        if bg_collisions:
            for collision in bg_collisions:
                # Hits ground
                if projectile.rect.bottom < collision.rect.top + 20:
                    projectile.rect.bottom = collision.rect.top - 5
                # Hit side walls
                elif projectile.rect.right > collision.rect.left + 20\
                        or projectile.rect.left < collision.rect.right - 20:
                    # Checks if player is not on top
                    if projectile.rect.bottom > collision.rect.top:
                        if projectile.name == "shell":
                            projectile.flip_direction()
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

        if not self.camera.camera_hit_right_screen:
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

            for brick in self.brick_group:
                brick.rect.x = brick.original_pos[0] - self.camera.world_offset_x

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
            self.check_projectile_collision(projectile)
            projectile.update()

    def update_brick_group(self):
        for brick in self.brick_group:
            brick.update()

    def update_coin_group(self):
        for coin in self.coin_group:
            coin.update()

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

    def draw_brick_group(self):
        for brick in self.brick_group:
            brick.draw()

    def draw_coin_group(self):
        for coin in self.coin_group:
            coin.draw()

    def move_player(self, mouse_x, mouse_y):
        """ This is for developer use only """
        self.camera.moveCamera(200)
        self.player_group.sprite.rect.y = 0

    def get_coordinates(self):
        x_coordinates = self.player_group.sprite.rect.right + self.camera.world_offset_x
        print("x_coordinates based on player's right side: " + str(x_coordinates))
        x_coordinates = self.player_group.sprite.rect.left + self.camera.world_offset_x
        print("x_coordinates based on player's left side: " + str(x_coordinates))

    def draw_debug_line(self):
        increment = 50
        line_total = int(self.screen.get_rect().height / increment) + 1

        # Draw horizontal y axis lines
        for i in range(0,line_total):
            msg = str(i*increment)
            font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
            message_image = font.render(msg, True, (255, 255, 255))
            message_rect = message_image.get_rect()
            message_rect.y = i*increment
            pygame.draw.line(self.screen, (255, 255, 255), (0, i*increment), (self.screen.get_rect().width, i*increment))
            self.screen.blit(message_image, message_rect)

        # Draw vertical x axis line
        player_rect = self.player_group.sprite.rect
        msg = str(self.camera.world_offset_x + self.player_group.sprite.rect.right)
        font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
        message_image = font.render(msg, True, (255, 255, 255))
        message_rect = message_image.get_rect()
        message_rect.y = self.player_group.sprite.rect.top
        message_rect.x = self.player_group.sprite.rect.right
        pygame.draw.line(self.screen, (255, 255, 255), (player_rect.right, 0), (player_rect.right, self.screen.get_rect().height))
        self.screen.blit(message_image, message_rect)

    def draw_mouse_coordinates(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x_coordinates = mouse_x + self.camera.world_offset_x
        msg = "(" + str(world_x_coordinates) + ", " + str(mouse_y) + ")"
        font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
        message_image = font.render(msg, True, (255, 255, 255))
        message_rect = message_image.get_rect()

        # Display top right
        self.screen.blit(message_image, message_rect)
        # Display on mouse cursor
        message_rect.x = mouse_x + 25
        message_rect.y = mouse_y
        self.screen.blit(message_image, message_rect)

    def set_point_a(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.controller.point_a[0] = mouse_x + self.camera.world_offset_x
        self.controller.point_a[1] = mouse_y

    def set_point_b(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.controller.point_b[0] = mouse_x + self.camera.world_offset_x
        self.controller.point_b[1] = mouse_y

    def print_description(self):
        print('      {')
        print('         "x": ' + str(self.controller.point_a[0]) + ",")
        print('         "y": ' + str(self.controller.point_a[1]) + ",")
        print('         "width": ' + str(self.controller.point_b[0] - self.controller.point_a[0]) + ",")
        print('         "height": ' + str(self.controller.point_b[1] - self.controller.point_a[1]))
        print('      },')
