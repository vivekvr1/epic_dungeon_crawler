import pygame
import math
import sys
import os
from assets.player import create_player_image

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
        # Movement
        self.speed = 3
        self.direction = {"up": False, "down": False, "left": False, "right": False}
        
        # Combat
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.damage = 10
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        
        # Stats
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        self.kills = 0
        
        # Inventory
        self.inventory = []
        
        # Image
        self.image = create_player_image()
        self.facing_right = True
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction["up"] = True
            elif event.key == pygame.K_s:
                self.direction["down"] = True
            elif event.key == pygame.K_a:
                self.direction["left"] = True
            elif event.key == pygame.K_d:
                self.direction["right"] = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.direction["up"] = False
            elif event.key == pygame.K_s:
                self.direction["down"] = False
            elif event.key == pygame.K_a:
                self.direction["left"] = False
            elif event.key == pygame.K_d:
                self.direction["right"] = False
    
    def update(self, world):
        # Movement
        dx = 0
        dy = 0
        
        if self.direction["up"]:
            dy -= self.speed
        if self.direction["down"]:
            dy += self.speed
        if self.direction["left"]:
            dx -= self.speed
            self.facing_right = False
        if self.direction["right"]:
            dx += self.speed
            self.facing_right = True
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071
        
        # Update position
        self.x += dx
        self.y += dy
        
        # Keep player on screen
        self.x = max(self.width // 2, min(800 - self.width // 2, self.x))
        self.y = max(self.height // 2, min(600 - self.height // 2, self.y))
        
        # Update rect
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        
        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
    
    def attack(self, target_pos):
        if self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 30  # Half second cooldown at 60 FPS
            
            # Calculate attack direction
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            angle = math.atan2(dy, dx)
            
            # Update facing direction based on attack
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
            
            # Create attack hitbox
            attack_distance = 60
            attack_width = 40
            attack_x = self.x + math.cos(angle) * attack_distance
            attack_y = self.y + math.sin(angle) * attack_distance
            
            self.attack_rect = pygame.Rect(attack_x - attack_width // 2, 
                                          attack_y - attack_width // 2,
                                          attack_width, attack_width)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def gain_experience(self, amount):
        self.experience += amount
        self.kills += 1
        
        # Level up if enough experience
        if self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)
        
        # Improve stats
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.damage += 5
    
    def render(self, screen):
        # Draw player with image
        if not self.facing_right:
            # Flip image if facing left
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x - self.width // 2, self.y - self.height // 2))
        else:
            screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        
        # Draw attack if attacking
        if self.is_attacking:
            pygame.draw.rect(screen, (255, 0, 0, 128), self.attack_rect)  # Red for attack with transparency