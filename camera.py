class Camera:
    """ Camera helps move the game screen around"""
    def __init__(self, hub):
        self.world_offset_x = 0
        self.player_offset_x = 0
        self.camera_hit_right_screen = False
        self.player_hit_right_screen = False

    def moveCamera(self, velocity):
        if not self.camera_hit_right_screen:
            self.world_offset_x += velocity
        if not self.player_hit_right_screen:
            self.player_offset_x += velocity

    def reset_camera(self):
        self.world_offset_x = 0
        self.player_offset_x = 0
        self.camera_hit_right_screen = False
        self.player_hit_right_screen = False