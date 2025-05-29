import pygame
import os

def load_sounds():
    sounds = {}
    
    # Initialize mixer
    pygame.mixer.init()
    
    try:
        # Try to load sounds if they exist
        coin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'coin.wav')
        hit_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'hit.wav')
        
        if os.path.exists(coin_path):
            sounds['coin'] = pygame.mixer.Sound(coin_path)
        else:
            sounds['coin'] = create_beep_sound(800)
            
        if os.path.exists(hit_path):
            sounds['hit'] = pygame.mixer.Sound(hit_path)
        else:
            sounds['hit'] = create_beep_sound(200)
    except:
        # Fallback to simple beep sounds
        sounds['coin'] = create_beep_sound(800)
        sounds['hit'] = create_beep_sound(200)
    
    return sounds

def create_beep_sound(frequency):
    # Create a simple beep sound as a placeholder
    sound = pygame.mixer.Sound(buffer=bytes([128] * 1000))
    return sound