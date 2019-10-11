class Camera:
    """ Camera helps move the game screen around"""
    def __init__(self, hub):
        self.world_offset_x = 0
        self.player_offset_x = 0