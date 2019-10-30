

class GameMode:
    """ Gamemode stores all data related to the game and win/lose conditions."""
    def __init__(self, hub):
        self.currentlevel = 1
        self.lives = 3
        self.score = 0
        self.mario_is_dead = False
        self.mario_in_air = False
        self.mario_is_running = False

