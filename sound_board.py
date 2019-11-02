import pygame


class SoundBoard:
    # Stores eall the necessary sounds to play during the game
    def __init__(self):
        """ Initialize default values"""

        self.one_up = pygame.mixer.Sound('wavs/smb_1-up.wav')
        self.bowser_falls = pygame.mixer.Sound('wavs/smb_bowserfalls.wav')
        self.bowser_fire = pygame.mixer.Sound('wavs/smb_bowserfire.wav')
        self.breakblock = pygame.mixer.Sound('wavs/smb_breakblock.wav')
        self.bump = pygame.mixer.Sound('wavs/smb_bump.wav')
        self.coin = pygame.mixer.Sound('wavs/smb_coin.wav')
        self.fireball = pygame.mixer.Sound('wavs/smb_fireball.wav')
        self.fireworks = pygame.mixer.Sound('wavs/smb_fireworks.wav')
        self.flagpole = pygame.mixer.Sound('wavs/smb_flagpole.wav')
        self.gameover = pygame.mixer.Sound('wavs/smb_gameover.wav')
        self.jump_small = pygame.mixer.Sound('wavs/smb_jump-small.wav')
        self.jump_super = pygame.mixer.Sound('wavs/smb_jump-super.wav')
        self.kick = pygame.mixer.Sound('wavs/smb_kick.wav')
        self.mario_die = pygame.mixer.Sound('wavs/smb_mariodie.wav')
        self.pause = pygame.mixer.Sound('wavs/smb_pause.wav')
        self.pipe = pygame.mixer.Sound('wavs/smb_pipe.wav')
        self.powerup = pygame.mixer.Sound('wavs/smb_powerup.wav')
        self.powerup_appears = pygame.mixer.Sound('wavs/smb_powerup_appears.wav')
        self.stage_clear = pygame.mixer.Sound('wavs/smb_stage_clear.wav')
        self.stomp = pygame.mixer.Sound('wavs/smb_stomp.wav')
        self.vine = pygame.mixer.Sound('wavs/smb_vine.wav')
        self.warning = pygame.mixer.Sound('wavs/smb_warning.wav')
        self.world_clear = pygame.mixer.Sound('wavs/smb_world_clear.wav')
        self.set_volume(0.5)

    def play_main_theme_overworld(self):
        pygame.mixer.music.load('mp3/01-main-theme-overworld.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_underworld(self):
        pygame.mixer.music.load('mp3/02-underworld.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_underwater(self):
        pygame.mixer_music.load('mp3/03-underwater.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_castle(self):
        pygame.mixer_music.load('mp3/04-castle.mp3')
        pygame.mixer.music.play(-1, 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume=0.7):
        self.one_up.set_volume(volume)
        self.bowser_falls.set_volume(volume)
        self.bowser_fire.set_volume(volume)
        self.breakblock.set_volume(volume)
        self.bump.set_volume(volume)
        self.coin.set_volume(volume)
        self.fireball.set_volume(volume)
        self.fireworks.set_volume(volume)
        self.flagpole.set_volume(volume)
        self.gameover.set_volume(volume)
        self.jump_small.set_volume(volume)
        self.jump_super.set_volume(volume)
        self.kick.set_volume(volume)
        self.mario_die.set_volume(volume)
        self.pause.set_volume(volume)
        self.pipe.set_volume(volume)
        self.powerup.set_volume(volume)
        self.powerup_appears.set_volume(volume)
        self.stage_clear.set_volume(volume)
        self.stage_clear.set_volume(volume)
        self.stomp.set_volume(volume)
        self.vine.set_volume(volume)
        self.warning.set_volume(volume)
        self.world_clear.set_volume(volume)