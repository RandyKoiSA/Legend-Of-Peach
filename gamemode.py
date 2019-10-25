

class GameMode:
    """ Gamemode stores all data related to the game and win/lose conditions."""
    def __init__(self, hub):
        self.currentlevel = 1
        self.lives = 3

        self.mario_is_dead = False

