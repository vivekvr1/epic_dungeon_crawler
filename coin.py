import pygame
import random
import math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.health_value = 10
        self.collected = False
        self.animation_timer = 0
        
    def update(self):
        # Simple floating animation
        self.animation_timer += 1
        offset = math.sin(self.animation_timer * 0.1) * 2
        self.rect.y = self.y - self.height // 2 + offset
        
    def render(self, screen):
        if not self.collected:
            # Draw coin as a gold circle
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y + math.sin(self.animation_timer * 0.1) * 2), 7)
            # Add shine effect
            pygame.draw.circle(screen, (255, 255, 200), (self.x - 2, self.y - 2 + math.sin(self.animation_timer * 0.1) * 2), 2)