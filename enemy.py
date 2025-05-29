import pygame
import math
import random
from assets.player import create_enemy_image

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
        # Set stats based on enemy type
        if enemy_type == "skeleton":
            self.health = 30
            self.max_health = 30
            self.damage = 5
            self.speed = 1.5
        elif enemy_type == "zombie":
            self.health = 50
            self.max_health = 50
            self.damage = 8
            self.speed = 1.0
        elif enemy_type == "demon":
            self.health = 80
            self.max_health = 80
            self.damage = 12
            self.speed = 2.0
            
        # Create enemy image
        self.image = create_enemy_image(enemy_type)
        self.facing_right = True
        
        # Combat
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 50
        
        # AI
        self.state = "wander"  # wander, chase, attack
        self.wander_direction = random.uniform(0, 2 * math.pi)
        self.wander_timer = random.randint(60, 180)  # 1-3 seconds at 60 FPS
        self.detection_range = 200
    
    def update(self, player):
        # AI state machine
        distance_to_player = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
        
        # Change state based on distance to player
        if distance_to_player <= self.attack_range:
            self.state = "attack"
        elif distance_to_player <= self.detection_range:
            self.state = "chase"
        else:
            if self.state != "wander":
                self.state = "wander"
                self.wander_timer = random.randint(60, 180)
                self.wander_direction = random.uniform(0, 2 * math.pi)
        
        # Execute behavior based on state
        if self.state == "wander":
            # Move in random direction
            dx = math.cos(self.wander_direction) * self.speed
            dy = math.sin(self.wander_direction) * self.speed
            
            self.x += dx
            self.y += dy
            
            # Update facing direction
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
            
            # Keep enemy on screen
            self.x = max(self.width // 2, min(800 - self.width // 2, self.x))
            self.y = max(self.height // 2, min(600 - self.height // 2, self.y))
            
            # Update wander timer and direction
            self.wander_timer -= 1
            if self.wander_timer <= 0:
                self.wander_timer = random.randint(60, 180)
                self.wander_direction = random.uniform(0, 2 * math.pi)
        
        elif self.state == "chase":
            # Move towards player
            angle = math.atan2(player.y - self.y, player.x - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            
            # Update facing direction
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
                
            self.x += dx
            self.y += dy
        
        elif self.state == "attack":
            # Attack player if cooldown is ready
            if self.attack_cooldown <= 0:
                self.attack(player)
                self.attack_cooldown = 60  # 1 second cooldown at 60 FPS
            else:
                self.attack_cooldown -= 1
        
        # Update rect position
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
    
    def attack(self, player):
        self.is_attacking = True
        
        # Create attack hitbox
        angle = math.atan2(player.y - self.y, player.x - self.x)
        attack_distance = 40
        attack_width = 30
        attack_x = self.x + math.cos(angle) * attack_distance
        attack_y = self.y + math.sin(angle) * attack_distance
        
        self.attack_rect = pygame.Rect(attack_x - attack_width // 2, 
                                      attack_y - attack_width // 2,
                                      attack_width, attack_width)
    
    def take_damage(self, amount):
        self.health -= amount
    
    def render(self, screen):
        # Draw enemy with image
        if not self.facing_right:
            # Flip image if facing left
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x - self.width // 2, self.y - self.height // 2))
        else:
            screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        
        # Draw health bar
        health_bar_width = 30
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x - health_bar_width // 2, 
                         self.y - self.height // 2 - 10, 
                         health_bar_width, health_bar_height))
        
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x - health_bar_width // 2, 
                         self.y - self.height // 2 - 10, 
                         health_bar_width * health_ratio, health_bar_height))
        
        # Draw attack if attacking
        if self.is_attacking:
            pygame.draw.rect(screen, (255, 255, 0, 128), self.attack_rect)  # Yellow for enemy attack with transparency
            self.is_attacking = False