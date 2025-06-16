import pygame
from config import *

SOUNDS_PATHS = {
    'run': 'Sounds/CoolRun.wav',
    'jump': 'Sounds/Jump.mp3',
    'hit': 'Sounds/Hit.wav',
    'button': 'Sounds/Button_sound.wav'
}

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.is_running_sound_playing = False
        self.load_default_sounds()  # Автоматическая загрузка звуков при создании
        
    def load_default_sounds(self):
        self.load_sound('run', SOUNDS_PATHS['run'])
        self.load_sound('jump', SOUNDS_PATHS['jump'])
        self.load_sound('hit', SOUNDS_PATHS['hit'])
        self.load_sound('button', SOUNDS_PATHS['button'])
    
    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)
    
    def play(self, name, loops=0): #играть звук 
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play(loops)
    
    def stop(self, name): #остановить  
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].stop()

    #метод для "бега"
    def play_run(self): 
        if not self.is_running_sound_playing and 'run' in self.sounds:
            self.play('run', -1)  # -1 для зацикливания
            self.is_running_sound_playing = True
    
    def stop_run(self):
        if self.is_running_sound_playing and 'run' in self.sounds:
            self.stop('run')
            self.is_running_sound_playing = False
    
    def set_volume(self, name, volume): #устанавливает громкость для конкретного звука
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].set_volume(volume)
    
    def set_all_volumes(self, volume):#устанавливает общую громкость для всех звуков
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)