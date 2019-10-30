

class Controller:
    """ Controller managers the players keyboard and mouse inputs """
    def __init__(self, hub):
        self.move_left = False
        self.move_right = False
        self.jump = False
        self.up = False


        # Developer use only
        self.developer_mode = False
        self.toggle_grid = False
        self.toggle_mouse_coordinates = False
        self.point_a = [0, 0]
        self.point_b = [0, 0]