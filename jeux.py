import pygame
import numpy as np
import random
import math
from enum import Enum

pygame.init()
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 12, 12
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class TowerType(Enum):
    BASIC = 0
    FAST = 1
    SLOW = 2
    AOE = 3

class GameState(Enum):
    PLACING = 0
    WAVES = 1
    GAME_OVER = 2

class TowerDefenseGame:
    def __init__(self, human_mode=False):
        self.human_mode = human_mode
        self.ai_turn = True
        self.reset()
    
    def reset(self):
        """Réinitialise le jeu"""
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.gold = 100
        self.lives = 10
        self.wave = 0
        self.enemies = []
        self.projectiles = []
        self.tower_range = 2
        self.state = GameState.PLACING
        self.placement_costs = [20, 30, 40, 50]
        self.last_spawn = 0
        self.done = False
        self.score = 0
        self.path = self.generate_path()
        self.place_base()
        return self.get_state()
    
    def generate_path(self):
        """Génère un chemin pour les ennemis"""
        path = [(0, 5)]  # Départ
        x, y = 0, 5
        
        # Vers la droite
        while x < GRID_WIDTH - 3:
            x += random.choice([1, 2])
            path.append((x, y))
        
        # Vers le bas
        while y < GRID_HEIGHT - 1:
            y += random.choice([1, 2])
            path.append((x, y))
        
        path.append((GRID_WIDTH-1, GRID_HEIGHT-1))  # Base
        return path
    
    def place_base(self):
        self.base_pos = (GRID_WIDTH-1, GRID_HEIGHT-1)
    
    def get_state(self):
        """État du jeu pour l'IA (25 valeurs)"""
        if self.done:
            return np.zeros(25)
            
        state = np.zeros(25)
        
        # Grille 5x5 centrale
        cx, cy = GRID_WIDTH//2, GRID_HEIGHT//2
        for i in range(5):
            for j in range(5):
                x, y = cx-2+i, cy-2+j
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    state[i*5+j] = self.grid[y, x] / 4.0
        
        # Ressources
        state[5] = min(self.gold / 100.0, 1.0)
        state[6] = min(self.lives / 10.0, 1.0)
        state[7] = self.wave / 20.0
        
        # Ennemis proches (4 max)
        for i, enemy in enumerate(self.enemies[:4]):
            state[9+i] = min(enemy['health']/50.0, 1.0)
        
        # Tours par type
        tower_count = [0,0,0,0]
        for t in range(4):
            count = np.sum(self.grid == t+1)
            tower_count[t] = count
        for i in range(4):
            state[13+i] = min(tower_count[i]/5.0, 1.0)
        
        return state
    
    def step(self, action):
        """Exécute une action de l'IA"""
        reward = 0
        
        # Placement tour (actions 0-11)
        if action < 12 and self.state == GameState.PLACING:
            tower_type = action % 4
            grid_x = (action // 4) * 3
            grid_y = (action % 3) * 3
            
            if (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT and 
                self.grid[grid_y, grid_x] == 0 and 
                self.gold >= self.placement_costs[tower_type]):
                
                self.grid[grid_y, grid_x] = tower_type + 1
                self.gold -= self.placement_costs[tower_type]
                reward += 10
        
        self.update_game()
        reward += self.calculate_reward()
        
        done = self.lives <= 0 or self.wave >= 15
        self.done = done
        
        info = {'score': self.score, 'wave': self.wave}
        return self.get_state(), reward, done, info
    
    def calculate_reward(self):
        """Calcule la récompense"""
        reward = 0
        reward += self.lives * 0.1
        reward -= len(self.enemies) * 0.5
        
        if random.random() < 0.05:
            self.gold += 5
            reward += 2
        
        self.score += reward
        return reward
    
    def update_game(self):
        """Met à jour le jeu"""
        current_time = pygame.time.get_ticks()
        
        # Spawn ennemis
        if current_time - self.last_spawn > 800 and len(self.enemies) < 8:
            self.enemies.append({
                'pos': [self.path[0][0]*TILE_SIZE + 20, self.path[0][1]*TILE_SIZE + 20],
                'health': random.randint(20, 40),
                'speed': random.uniform(0.8, 1.2),
                'path_idx': 0
            })
            self.last_spawn = current_time
        
        # Update ennemis
        for enemy in self.enemies[:]:
            if enemy['path_idx'] < len(self.path)-1:
                tx, ty = self.path[enemy['path_idx']+1]
                target_x = tx * TILE_SIZE + 20
                target_y = ty * TILE_SIZE + 20
                
                dx = target_x - enemy['pos'][0]
                dy = target_y - enemy['pos'][1]
                dist = math.hypot(dx, dy)
                
                if dist < 5:
                    enemy['path_idx'] += 1
                else:
                    enemy['pos'][0] += dx * enemy['speed'] * 0.02
                    enemy['pos'][1] += dy * enemy['speed'] * 0.02
            
            # Base atteinte
            if enemy['path_idx'] >= len(self.path)-1:
                self.lives -= 1
                self.enemies.remove(enemy)
        
        # Tours attaquent
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y,x] > 0:
                    tower_pos = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
                    for enemy in self.enemies[:]:
                        dist = math.hypot(enemy['pos'][0]-tower_pos[0], enemy['pos'][1]-tower_pos[1])
                        if dist < 120:
                            enemy['health'] -= 1
                            if enemy['health'] <= 0:
                                self.enemies.remove(enemy)
                                self.gold += 8
        
        # Fin de vague
        if len(self.enemies) == 0 and self.state == GameState.WAVES:
            self.wave += 1
            self.gold += 50
            self.state = GameState.PLACING
    
    def handle_event(self, event):
        """Gestion humaine"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.human_mode:
            mx, my = event.pos
            grid_x = mx // TILE_SIZE
            grid_y = my // TILE_SIZE
            if (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT and 
                self.grid[grid_y, grid_x] == 0 and self.gold >= 20):
                self.grid[grid_y, grid_x] = 1
                self.gold -= 20
    
    def render(self, screen):
        """Rendu graphique"""
        screen.fill((20, 40, 20))
        
        # Grille
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, (50, 80, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, (50, 80, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Chemin
        for i in range(len(self.path)-1):
            p1 = (self.path[i][0]*TILE_SIZE + 20, self.path[i][1]*TILE_SIZE + 20)
            p2 = (self.path[i+1][0]*TILE_SIZE + 20, self.path[i+1][1]*TILE_SIZE + 20)
            pygame.draw.line(screen, (255, 140, 0), p1, p2, 8)
        
        # Tours
        colors = [(100,100,255), (100,255,100), (255,100,255), (255,255,100)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y,x] > 0:
                    color = colors[int(self.grid[y,x])-1]
                    pygame.draw.rect(screen, color, 
                                   (x*TILE_SIZE+5, y*TILE_SIZE+5, TILE_SIZE-10, TILE_SIZE-10))
        
        # Ennemis ✅ CORRIGÉ
        for enemy in self.enemies:
            pygame.draw.circle(screen, (255, 50, 50), 
                             (int(enemy['pos'][0]), int(enemy['pos'][1])), 12)
        
        # Base
        pygame.draw.rect(screen, (255, 100, 100), 
                        (self.base_pos[0]*TILE_SIZE, self.base_pos[1]*TILE_SIZE, 
                         TILE_SIZE*2, TILE_SIZE*2))
        
        # UI
        font = pygame.font.Font(None, 36)
        texts = [
            f"Or: {self.gold}",
            f"Vies: {self.lives}",
            f"Vague: {self.wave}",
            f"Score: {int(self.score)}"
        ]
        
        for i, text in enumerate(texts):
            surf = font.render(text, True, (255, 255, 255))
            screen.blit(surf, (SCREEN_WIDTH - 200, 20 + i*40))
        
        if self.done:
            game_over = font.render("GAME OVER", True, (255, 50, 50))
            screen.blit(game_over, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
