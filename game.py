import pygame
from player import Player
from enemy import Enemy
from world import World
from ui import UI
from coin import Coin
from assets.sounds import load_sounds
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.world = World()
        self.player = Player(400, 300)
        self.enemies = []
        self.coins = []
        self.ui = UI(screen)
        self.spawn_timer = 0
        self.coin_timer = 0
        self.game_state = "playing"  # playing, game_over, victory
        
        # Visual effects
        self.particles = []
        
        # Load sounds
        self.sounds = load_sounds()
        
        # Spawn initial enemies
        self.spawn_enemies(5)
    
    def spawn_enemies(self, count):
        for _ in range(count):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            enemy_type = random.choice(["skeleton", "zombie", "demon"])
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def spawn_coin(self):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        self.coins.append(Coin(x, y))
    
    def handle_event(self, event):
        # Always pass keyboard events to player for movement
        self.player.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if self.game_state == "game_over" or self.game_state == "victory":
                if event.key == pygame.K_r:
                    self.__init__(self.screen)  # Reset game
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.player.attack(pygame.mouse.get_pos())
                # Add attack particles
                self.add_particles(pygame.mouse.get_pos(), 10, (255, 200, 0))
    
    def add_particles(self, pos, count, color):
        for _ in range(count):
            particle = {
                'x': self.player.x,
                'y': self.player.y,
                'dx': (pos[0] - self.player.x) / 20 + random.uniform(-1, 1),
                'dy': (pos[1] - self.player.y) / 20 + random.uniform(-1, 1),
                'size': random.randint(2, 5),
                'color': color,
                'life': random.randint(10, 30)
            }
            self.particles.append(particle)
    
    def update(self):
        if self.game_state == "playing":
            # Update player
            self.player.update(self.world)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update(self.player)
                
                # Check if player hits enemy
                if self.player.is_attacking and self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.damage)
                    # Add hit particles
                    self.add_particles((enemy.x, enemy.y), 15, (255, 0, 0))
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.player.gain_experience(10)
                
                # Check if enemy hits player
                if enemy.is_attacking and enemy.attack_rect.colliderect(self.player.rect):
                    self.player.take_damage(enemy.damage)
                    # Play hit sound
                    self.sounds['hit'].play()
            
            # Update coins
            for coin in self.coins[:]:
                coin.update()
                # Check if player collects coin
                if self.player.rect.colliderect(coin.rect) and not coin.collected:
                    coin.collected = True
                    self.player.health = min(self.player.health + coin.health_value, self.player.max_health)
                    self.coins.remove(coin)
                    # Play coin sound
                    self.sounds['coin'].play()
                    # Add coin particles
                    self.add_particles((self.player.x, self.player.y), 20, (255, 215, 0))
            
            # Update particles
            for particle in self.particles[:]:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.particles.remove(particle)
            
            # Spawn more enemies over time
            self.spawn_timer += 1
            if self.spawn_timer >= 300:  # Every 5 seconds (60 FPS)
                self.spawn_enemies(1)
                self.spawn_timer = 0
            
            # Spawn coins periodically
            self.coin_timer += 1
            if self.coin_timer >= 600:  # Every 10 seconds (60 FPS)
                self.spawn_coin()
                self.coin_timer = 0
            
            # Check game over condition
            if self.player.health <= 0:
                self.game_state = "game_over"
            
            # Check victory condition (kill 20 enemies)
            if self.player.kills >= 20:
                self.game_state = "victory"
    
    def render(self):
        # Draw world
        self.world.render(self.screen)
        
        # Draw coins
        for coin in self.coins:
            coin.render(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # Draw player
        self.player.render(self.screen)
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'], 
                              (int(particle['x']), int(particle['y'])), 
                              particle['size'])
        
        # Draw UI
        self.ui.render(self.player)
        
        # Draw game state messages
        if self.game_state == "game_over":
            font = pygame.font.SysFont(None, 64)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 
                                    self.screen.get_height() // 2 - text.get_height() // 2))
            
            font = pygame.font.SysFont(None, 32)
            text = font.render("Press R to restart", True, (255, 255, 255))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 
                                    self.screen.get_height() // 2 + 50))
        
        elif self.game_state == "victory":
            font = pygame.font.SysFont(None, 64)
            text = font.render("VICTORY!", True, (0, 255, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 
                                    self.screen.get_height() // 2 - text.get_height() // 2))
            
            font = pygame.font.SysFont(None, 32)
            text = font.render("Press R to play again", True, (255, 255, 255))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 
                                    self.screen.get_height() // 2 + 50))