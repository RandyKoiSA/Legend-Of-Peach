import pygame
from hub import Hub


def run_game():
    """ Main game structure that runs the whole program """
    # Initialize pygame
    pygame.init()

    # Set up the hub
    hub = Hub()
    pygame.display.set_caption(hub.WINDOW_TITLE)
    pygame.display.set_icon(hub.WINDOW_ICON)

    while True:
        """ Game Loop, as long as this is true the game will run. """
        # Clear Screen
        hub.main_screen.fill(hub.BG_COLOR)

        # Decide what screen to display
        hub.display_screen()

        # Display the screen onto the window
        pygame.display.flip()
        hub.CLOCK.tick(hub.FRAMERATE)


# If the console command runs this file, it will run the game
if __name__ == '__main__':
    run_game()