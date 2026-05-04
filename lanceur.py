import pygame
import sys
import os
from ia import DeepQAgent
from jeux import TowerDefenseGame
import torch
import pickle
import time
import numpy as np

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense AI - Menu Principal")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Launcher:
    def __init__(self):
        self.game = None
        self.agent = None
        self.mode = None
        self.running = False
        
    def load_agent(self, model_path="tower_defense_model.pth"):
        """Charge ou crée un nouvel agent"""
        self.agent = DeepQAgent(state_size=25, action_size=13)
        if os.path.exists(model_path):
            self.agent.load_model(model_path)
            print(f"✅ Modèle chargé : {model_path}")
        else:
            print("🆕 Nouveau modèle créé")
    
    def show_menu(self):
        """Affiche le menu principal"""
        while True:
            screen.fill((20, 20, 40))
            
            title = font.render("TOWER DEFENSE AI", True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            buttons = [
                ("ENTRAÎNER IA (2000 épisodes)", (320, 250), self.train_mode),
                ("VOIR IA JOUER", (370, 320), self.ai_play_mode),
                ("JOUER CONTRE IA", (370, 390), self.human_vs_ai_mode),
                ("QUITTER", (420, 460), self.quit_game)
            ]
            
            mouse_pos = pygame.mouse.get_pos()
            for text, pos, callback in buttons:
                rect = pygame.Rect(pos[0]-120, pos[1]-20, 240, 40)
                color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (60, 150, 60)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255,255,255), rect, 2)
                text_surf = small_font.render(text, True, (255,255,255))
                screen.blit(text_surf, (pos[0] - text_surf.get_width()//2, pos[1] - text_surf.get_height()//2))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for text, pos, callback in buttons:
                        rect = pygame.Rect(pos[0]-120, pos[1]-20, 240, 40)
                        if rect.collidepoint(event.pos):
                            callback()
    
    def train_mode(self):
        """Mode entraînement IA"""
        self.mode = "train"
        self.load_agent()
        self.game = TowerDefenseGame()
        self.running = True
        self.train_loop()
    
    def ai_play_mode(self):
        """Mode observation IA"""
        self.mode = "ai_play"
        self.load_agent()
        self.game = TowerDefenseGame()
        self.running = True
        self.play_loop()
    
    def human_vs_ai_mode(self):
        """Mode joueur vs IA"""
        self.mode = "human_ai"
        self.load_agent()
        self.game = TowerDefenseGame(human_mode=True)
        self.running = True
        self.human_loop()
    
    def train_loop(self):
        """Boucle d'entraînement"""
        episodes = 2000
        scores = []
        
        print("🚀 DÉBUT ENTRAÎNEMENT 2000 ÉPISODES...")
        for episode in range(episodes):
            state = self.game.reset()
            total_reward = 0
            done = False
            step = 0
            
            while not done and step < 1000:
                # Entraînement rapide (sans rendu pour vitesse)
                action = self.agent.act(state)
                next_state, reward, done, info = self.game.step(action)
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                
                if len(self.agent.memory) > 32:
                    self.agent.replay(32)
                step += 1
            
            scores.append(info['score'])
            
            # Affichage tous les 100 épisodes + rendu visuel
            if episode % 100 == 0:
                avg_score = np.mean(scores[-100:]) if scores else 0
                print(f"Épisode {episode:4d}/{episodes} | Score: {info['score']:4.0f} | Moyenne: {avg_score:4.0f}")
                
                # Rendu visuel rapide
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                self.game.render(screen)
                pygame.display.flip()
                clock.tick(30)
                
                self.agent.save_model("tower_defense_model.pth")
        
        print("✅ ENTRAÎNEMENT TERMINÉ! Modèle sauvegardé.")
        time.sleep(3)
        self.show_menu()
    
    def play_loop(self):
        """Boucle jeu IA seule"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.game.reset()
            
            state = self.game.get_state()
            if state is not None:
                action = self.agent.act(state, epsilon=0.01)
                self.game.step(action)
            
            self.game.render(screen)
            pygame.display.flip()
            clock.tick(30)
            
            if self.game.done:
                time.sleep(1)
                self.game.reset()
    
    def human_loop(self):
        """Boucle joueur vs IA"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                self.game.handle_event(event)
            
            if not self.game.ai_turn and self.human_mode:
                self.game.render(screen)
                pygame.display.flip()
                clock.tick(30)
            else:
                state = self.game.get_state()
                if state is not None:
                    action = self.agent.act(state, epsilon=0.0)
                    self.game.step(action)
                    self.game.render(screen)
                    pygame.display.flip()
                    clock.tick(15)
    
    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.show_menu()
