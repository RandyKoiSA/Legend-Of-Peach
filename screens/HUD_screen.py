from custom.text import Text


class HudScreen:
    """ HUD screen showing data such as points and lives """
    def __init__(self, hub):
        """ Initialize default values """
        self.hub = hub
        self.screen = hub.main_screen
        self.gamemode = hub.gamemode

        # Add Score Text / Number
        self.score_text = Text(self.screen, str("SCORE: "))
        self.score_number_text = Text(self.screen, str(self.gamemode.score))
        self.prep_score()

        # Add Lives Text / Number
        self.lives_text = Text(self.screen, str("LIVES: "))
        self.lives_number_text = Text(self.screen, str(self.gamemode.lives))
        self.prep_lives_text()

        # Add Coin Text / Number
        self.coin_text = Text(self.screen, str("COINS: "))
        self.coin_number_text = Text(self.screen, str(self.gamemode.coins))
        self.prep_coin_text()

        # Add Time Text / Number
        self.time_text = Text(self.screen, str("TIME: "))
        self.time_number_text = Text(self.screen, str(self.gamemode.time))
        self.prep_time_text()

        # Add World Text / Name
        self.world_text = Text(self.screen, str("WORLD: "))
        self.world_name_text = Text(self.screen, str(self.hub.level_name))
        self.prep_world_name_text()

    def run(self):
        self.run_event()
        self.run_update()
        self.run_draw()

    def run_event(self):
        pass

    def run_update(self):
        self.coin_number_text.message = str(self.gamemode.coins)
        self.coin_number_text.update_message()

        self.score_number_text.message = str(self.gamemode.score)
        self.score_number_text.update_message()

        self.lives_number_text.message = str(self.gamemode.lives)
        self.lives_number_text.update_message()

        self.world_name_text.message = str(self.hub.level_name)
        self.world_name_text.update_message()

        self.time_number_text.message = str(self.gamemode.time)
        self.time_number_text.update_message()

    def run_draw(self):
        self.score_text.draw()
        self.score_number_text.draw()
        self.lives_text.draw()
        self.lives_number_text.draw()
        self.coin_text.draw()
        self.coin_number_text.draw()
        self.time_text.draw()
        self.time_number_text.draw()
        self.world_text.draw()
        self.world_name_text.draw()

    def prep_coin_text(self):
        self.coin_text.msg_image_rect.right = self.lives_text.msg_image_rect.right - 100
        self.coin_text.msg_image_rect.bottom = self.lives_text.msg_image_rect.bottom

        self.coin_number_text.msg_image_rect.center = self.coin_text.msg_image_rect.center
        self.coin_number_text.msg_image_rect.centery += 25

    def prep_time_text(self):
        self.time_text.msg_image_rect.left = self.score_text.msg_image_rect.right + 100
        self.time_text.msg_image_rect.bottom = self.score_text.msg_image_rect.bottom

        self.time_number_text.msg_image_rect.center = self.time_text.msg_image_rect.center
        self.time_number_text.msg_image_rect.y += 25

    def prep_world_name_text(self):
        self.world_text.msg_image_rect.x = self.screen.get_rect().width / 2
        self.world_text.msg_image_rect.y = 10

        self.world_name_text.msg_image_rect.left = self.world_text.msg_image_rect.left
        self.world_name_text.msg_image_rect.y += 40

    def prep_score(self):
        self.score_text.msg_image_rect.x = 50
        self.score_text.msg_image_rect.y = 10

        self.score_number_text.msg_image_rect.center = self.score_text.msg_image_rect.center
        self.score_number_text.msg_image_rect.y += 25

    def prep_lives_text(self):
        self.lives_text.msg_image_rect.right = self.screen.get_rect().right - 50
        self.lives_text.msg_image_rect.y = 10

        self.lives_number_text.msg_image_rect.center = self.lives_text.msg_image_rect.center
        self.lives_number_text.msg_image_rect.y += 25
