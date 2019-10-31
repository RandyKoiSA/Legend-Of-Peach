from pygame.sprite import Sprite
import pygame


class Points(Sprite):
    """ Display points onto the screen and kill itself after a certain amount of time """
    def __init__(self, hub, point_group, type="100pts", pos_x=0, pos_y=0):
        super().__init__()
        self.hub = hub
        self.screen = hub.main_screen
        self.point_group = point_group
        self.lifetime = 1000
        self.velocity = 5
        self.points_image = {
            "1-up": pygame.image.load('imgs/Other/1up.png'),
            "100pts": pygame.image.load('imgs/Other/100pts.png'),
            "200pts": pygame.image.load('imgs/Other/200pts.png'),
            "400pts": pygame.image.load('imgs/Other/400pts.png'),
            "500pts": pygame.image.load('imgs/Other/500pts.png'),
            "800pts": pygame.image.load('imgs/Other/800pts.png'),
            "1000pts": pygame.image.load('imgs/Other/1000pts.png'),
            "2000pts": pygame.image.load('imgs/Other/2000pts.png'),
            "4000pts": pygame.image.load('imgs/Other/4000pts.png'),
            "5000pts": pygame.image.load('imgs/Other/5000pts.png'),
            "8000pts": pygame.image.load('imgs/Other/8000pts.png')
        }
        self.type = type

        try:
            self.current_image = self.points_image[type]
        except LookupError:
            self.current_image = self.points_image["100pts"]

        self.prep_curremt_image()

        self.original_x = pos_x
        self.original_y = pos_y

        self.rect = self.current_image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.start_tick = pygame.time.get_ticks() + self.lifetime

    def update(self):
        self.rect.y -= self.velocity
        self.rect.x = self.original_x - self.hub.camera.world_offset_x
        if pygame.time.get_ticks() >= self.start_tick:
            self.point_group.remove(self)

    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def prep_curremt_image(self):
        self.current_image = pygame.transform.scale(self.current_image, (45, 20))
        pass
