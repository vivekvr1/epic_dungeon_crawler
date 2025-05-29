import pygame
import os
import random

# Create simple player sprite
def create_player_image():
    image = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Body (blue)
    pygame.draw.rect(image, (0, 0, 200), (10, 15, 20, 20))
    
    # Head (skin tone)
    pygame.draw.circle(image, (255, 220, 180), (20, 10), 8)
    
    # Arms
    pygame.draw.rect(image, (0, 0, 200), (5, 15, 5, 15))
    pygame.draw.rect(image, (0, 0, 200), (30, 15, 5, 15))
    
    # Legs
    pygame.draw.rect(image, (50, 50, 150), (12, 35, 7, 5))
    pygame.draw.rect(image, (50, 50, 150), (22, 35, 7, 5))
    
    return image

# Create simple enemy sprites
def create_enemy_image(enemy_type):
    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    
    if enemy_type == "skeleton":
        # Skeleton (white/gray)
        pygame.draw.rect(image, (220, 220, 220), (8, 12, 14, 15))  # Body
        pygame.draw.circle(image, (200, 200, 200), (15, 8), 6)     # Skull
        pygame.draw.rect(image, (220, 220, 220), (5, 12, 4, 12))   # Left arm
        pygame.draw.rect(image, (220, 220, 220), (21, 12, 4, 12))  # Right arm
        
    elif enemy_type == "zombie":
        # Zombie (green)
        pygame.draw.rect(image, (50, 150, 50), (8, 12, 14, 15))    # Body
        pygame.draw.circle(image, (100, 200, 100), (15, 8), 6)     # Head
        pygame.draw.rect(image, (50, 150, 50), (5, 12, 4, 12))     # Left arm
        pygame.draw.rect(image, (50, 150, 50), (21, 12, 4, 12))    # Right arm
        
    elif enemy_type == "demon":
        # Demon (red)
        pygame.draw.rect(image, (150, 0, 0), (8, 12, 14, 15))      # Body
        pygame.draw.circle(image, (200, 0, 0), (15, 8), 6)         # Head
        pygame.draw.polygon(image, (150, 0, 0), [(10, 3), (15, 0), (20, 3)])  # Horns
        pygame.draw.rect(image, (150, 0, 0), (5, 12, 4, 12))       # Left arm
        pygame.draw.rect(image, (150, 0, 0), (21, 12, 4, 12))      # Right arm
    
    return image

# Create background tile images
def create_background_tiles():
    # Brighter floor tile with texture
    floor_tile = pygame.Surface((50, 50))
    
    # Lighter stone floor base color (blue-gray)
    floor_tile.fill((80, 90, 120))
    
    # Add stone texture pattern
    for _ in range(20):
        x = random.randint(0, 49)
        y = random.randint(0, 49)
        size = random.randint(2, 6)
        color_var = random.randint(-10, 10)
        color = (90 + color_var, 100 + color_var, 130 + color_var)
        pygame.draw.rect(floor_tile, color, (x, y, size, size))
    
    # Add subtle grid lines
    pygame.draw.line(floor_tile, (70, 80, 110), (0, 0), (50, 0))
    pygame.draw.line(floor_tile, (70, 80, 110), (0, 0), (0, 50))
    
    # Brighter obstacle (wall)
    obstacle_tile = pygame.Surface((50, 50))
    
    # Stone wall base color (warm beige)
    obstacle_tile.fill((180, 160, 140))
    
    # Add brick pattern
    for i in range(0, 50, 10):
        offset = 0 if (i // 10) % 2 == 0 else 5
        for j in range(0, 50, 10):
            if j + offset < 50:
                brick_color = (190 + random.randint(-15, 15), 
                              170 + random.randint(-15, 15), 
                              150 + random.randint(-15, 15))
                pygame.draw.rect(obstacle_tile, brick_color, 
                               (j + offset, i, 9, 9))
    
    # Add mortar lines
    for i in range(0, 50, 10):
        pygame.draw.line(obstacle_tile, (150, 140, 130), (0, i), (50, i))
    for j in range(0, 50, 10):
        pygame.draw.line(obstacle_tile, (150, 140, 130), (j, 0), (j, 50))
    
    return floor_tile, obstacle_tile