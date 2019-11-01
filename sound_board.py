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