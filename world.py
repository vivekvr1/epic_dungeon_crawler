import pygame
import random
from assets.player import create_background_tiles

class World:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.tile_size = 50
        
        # Load tile images
        self.floor_tile, self.obstacle_tile = create_background_tiles()
        
        # Generate a simple grid-based world
        self.grid = []
        for y in range(self.height // self.tile_size):
            row = []
            for x in range(self.width // self.tile_size):
                # Create mostly floor tiles with some obstacles
                if random.random() < 0.1:  # 10% chance for obstacle
                    tile_type = "obstacle"
                else:
                    tile_type = "floor"
                row.append(tile_type)
            self.grid.append(row)
        
        # Ensure the center area is clear for player spawn
        center_x = len(self.grid[0]) // 2
        center_y = len(self.grid) // 2
        for y in range(center_y - 1, center_y + 2):
            for x in range(center_x - 1, center_x + 2):
                self.grid[y][x] = "floor"
    
    def is_obstacle(self, x, y):
        # Convert world coordinates to grid coordinates
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        # Check if coordinates are within grid bounds
        if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
            return self.grid[grid_y][grid_x] == "obstacle"
        
        # Treat out-of-bounds as obstacles
        return True
    
    def render(self, screen):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                  self.tile_size, self.tile_size)
                
                if self.grid[y][x] == "floor":
                    # Draw floor tile
                    screen.blit(self.floor_tile, rect)
                else:
                    # Draw obstacle tile
                    screen.blit(self.obstacle_tile, rect)