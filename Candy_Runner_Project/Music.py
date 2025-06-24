import pygame
from config import *

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.is_running_sound_playing = False
        self.load_default_sounds()
        
    def load_default_sounds(self):
        self.load_sound('run', SOUNDS_PATHS['run'])
        self.load_sound('jump', SOUNDS_PATHS['jump'])
        self.load_sound('hit', SOUNDS_PATHS['hit'])
        self.load_sound('button', SOUNDS_PATHS['button'])
        self.load_sound('Death_player', SOUNDS_PATHS['Death_player'])
        self.load_sound('exit_sound', SOUNDS_PATHS['exit_sound'])
        self.load_sound('Game_over', SOUNDS_PATHS['Game_over'])
        self.load_sound('success', SOUNDS_PATHS['success'])
        self.load_sound('Win', SOUNDS_PATHS['Win'])
    
    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)
    
    def play_music(self, name, loops=-1, volume=0.5): #для обработки фоновой музыки
        if name in SOUNDS_PATHS:
            pygame.mixer.music.load(SOUNDS_PATHS[name])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)

    def stop_music(self,name): #для обработки фоновой музыки
        if name in SOUNDS_PATHS:
            pygame.mixer.music.stop()
    
    def play(self, name, loops=0):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play(loops)
    
    def stop(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].stop()

    def play_run(self): #для звука бега
        if not self.is_running_sound_playing and 'run' in self.sounds:
            self.play('run', -1)
            self.is_running_sound_playing = True
    
    def stop_run(self): #для звука бега
        if self.is_running_sound_playing and 'run' in self.sounds:
            self.stop('run')
            self.is_running_sound_playing = False
    