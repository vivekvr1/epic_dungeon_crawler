import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        
        # Create UI background with transparency
        self.ui_bg = pygame.Surface((220, 180), pygame.SRCALPHA)
        self.ui_bg.fill((0, 0, 0, 128))  # Semi-transparent black
    
    def render(self, player):
        # Draw UI background
        self.screen.blit(self.ui_bg, (5, 5))
        
        # Draw health bar with gradient
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        # Health bar background
        pygame.draw.rect(self.screen, (100, 0, 0), 
                        (10, 10, health_bar_width, health_bar_height))
        
        # Health bar fill with gradient
        for i in range(int(health_bar_width * health_ratio)):
            # Create a gradient from red to bright red
            color_val = min(255, 150 + i)
            pygame.draw.line(self.screen, (color_val, 0, 0), 
                           (10 + i, 10), (10 + i, 10 + health_bar_height))
        
        # Health bar border
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (10, 10, health_bar_width, health_bar_height), 1)
        
        health_text = self.font.render(f"Health: {player.health}/{player.max_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 35))
        
        # Draw mana bar with gradient
        mana_bar_width = 200
        mana_bar_height = 15
        mana_ratio = player.mana / player.max_mana
        
        # Mana bar background
        pygame.draw.rect(self.screen, (0, 0, 100), 
                        (10, 60, mana_bar_width, mana_bar_height))
        
        # Mana bar fill with gradient
        for i in range(int(mana_bar_width * mana_ratio)):
            # Create a gradient from blue to bright blue
            color_val = min(255, 150 + i)
            pygame.draw.line(self.screen, (0, 0, color_val), 
                           (10 + i, 60), (10 + i, 60 + mana_bar_height))
        
        # Mana bar border
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (10, 60, mana_bar_width, mana_bar_height), 1)
        
        mana_text = self.font.render(f"Mana: {player.mana}/{player.max_mana}", True, (255, 255, 255))
        self.screen.blit(mana_text, (10, 80))
        
        # Draw level and experience with glowing effect
        level_text = self.font.render(f"Level: {player.level}", True, (255, 255, 150))
        self.screen.blit(level_text, (10, 105))
        
        # XP bar with gradient
        xp_bar_width = 200
        xp_bar_height = 8
        xp_ratio = player.experience / player.experience_to_level
        
        # XP bar background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (10, 130, xp_bar_width, xp_bar_height))
        
        # XP bar fill with gradient
        for i in range(int(xp_bar_width * xp_ratio)):
            # Create a gradient from gold to bright gold
            green_val = min(255, 150 + i)
            pygame.draw.line(self.screen, (200, green_val, 0), 
                           (10 + i, 130), (10 + i, 130 + xp_bar_height))
        
        exp_text = self.font.render(f"EXP: {player.experience}/{player.experience_to_level}", True, (255, 255, 255))
        self.screen.blit(exp_text, (10, 140))
        
        # Draw kills counter with progress
        kills_text = self.font.render(f"Kills: {player.kills}/20", True, (255, 255, 255))
        self.screen.blit(kills_text, (10, 160))
        
        # Draw kills progress bar
        kills_bar_width = 200
        kills_bar_height = 5
        kills_ratio = player.kills / 20
        
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (10, 180, kills_bar_width, kills_bar_height))
        
        pygame.draw.rect(self.screen, (200, 50, 50), 
                        (10, 180, kills_bar_width * kills_ratio, kills_bar_height))
        
        # Draw controls help
        controls_text = self.font.render("WASD: Move | Left Click: Attack | Collect Coins for Health", True, (200, 200, 200))
        self.screen.blit(controls_text, (self.screen.get_width() - controls_text.get_width() - 10, 10))