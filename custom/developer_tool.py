import pygame


def move_player(camera, player_group):
    """ Developer tool, teleports mario 200 to the right and spawns at the roof to look through the world more
     easily. """
    camera.move_camera(200)
    player_group.sprite.rect.y = 0


def get_coordinates(player_group, camera):
    """ Developer tool, prints out x coordinates based on marios left and right rect onto the console."""
    x_coordinates = player_group.sprite.rect.right + camera.world_offset_x
    print("x_coordinates based on player's right side: " + str(x_coordinates))
    x_coordinates = player_group.sprite.rect.left + camera.world_offset_x
    print("x_coordinates based on player's left side: " + str(x_coordinates))


def draw_debug_line(self, screen, player_group):
    """ Developer tool, creates a horizontal lines and text to show the y coordinates.
    Also, created a vertical line on the right side of mario to find the x coordinates based on where he is. """
    increment = 50
    line_total = int(screen.get_rect().height / increment) + 1

    # Draw horizontal y axis lines
    for i in range(0, line_total):
        msg = str(i * increment)
        font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
        message_image = font.render(msg, True, (255, 255, 255))
        message_rect = message_image.get_rect()
        message_rect.y = i * increment
        pygame.draw.line(screen, (255, 255, 255), (0, i * increment),
                         (screen.get_rect().width, i * increment))
        screen.blit(message_image, message_rect)

    # Draw vertical x axis line
    player_rect = player_group.sprite.rect
    msg = str(self.camera.world_offset_x + self.player_group.sprite.rect.right)
    font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
    message_image = font.render(msg, True, (255, 255, 255))
    message_rect = message_image.get_rect()
    message_rect.y = player_group.sprite.rect.top
    message_rect.x = player_group.sprite.rect.right
    pygame.draw.line(self.screen, (255, 255, 255), (player_rect.right, 0),
                     (player_rect.right, self.screen.get_rect().height))
    screen.blit(message_image, message_rect)


def draw_mouse_coordinates(screen, camera):
    """ Developer tool, only called when key 6 is toggled. Displays current coordinates based on mouse cursor is."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_x_coordinates = mouse_x + camera.world_offset_x
    msg = "(" + str(world_x_coordinates) + ", " + str(mouse_y) + ")"
    font = pygame.font.Font('font/kenvector_future_thin.ttf', 20)
    message_image = font.render(msg, True, (255, 255, 255))
    message_rect = message_image.get_rect()

    # Display top right
    screen.blit(message_image, message_rect)
    # Display on mouse cursor
    message_rect.x = mouse_x + 25
    message_rect.y = mouse_y
    screen.blit(message_image, message_rect)


def set_point_a(controller, camera):
    """ Developer Tool, Assigned to key 1, set the coordinates to point A based on where the mouse cursor is. """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    controller.point_a[0] = mouse_x + camera.world_offset_x
    controller.point_a[1] = mouse_y


def set_point_b(controller, camera):
    """ Developer Tool, Assigned to key 2, set the coordinates to point B based on where the mouse cursor is. """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    controller.point_b[0] = mouse_x + camera.world_offset_x
    controller.point_b[1] = mouse_y


def print_description(controller):
    """ Developer tool, used for finding the location, width, and height of given point A and point B"""
    print('      {')
    print('         "x": ' + str(controller.point_a[0]) + ",")
    print('         "y": ' + str(controller.point_a[1]) + ",")
    print('         "width": ' + str(controller.point_b[0] - controller.point_a[0]) + ",")
    print('         "height": ' + str(controller.point_b[1] - controller.point_a[1]))
    print('      },')
