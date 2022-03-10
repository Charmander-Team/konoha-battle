import pygame
from player import Player
from opponent import Orochimaru, Kabuto

class Game:

    def __init__(self):
        # Definir si le jeu a commencé
        self.is_playing = False

        # Generer joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        # Groupe d'ennemis
        self.all_opponents = pygame.sprite.Group()

        self.pressed = {}

        # Récupérer ennemis
        self.score = 0

    def start(self):
        self.is_playing = True

        # On genere 3 ennemis + 1 "boss"
        self.spawn_opponent(Kabuto)
        self.spawn_opponent(Kabuto)
        self.spawn_opponent(Kabuto)
        self.spawn_opponent(Orochimaru)


    def game_over(self):
        # Reset du jeu (retirer les ennemis, remettre le joueur a 100 de vie, remettre la banniere de lancement)
        self.all_opponents = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False

    def update(self, screen,pseudo):
        # Appliquer l'image du joueur
        screen.blit(self.player.image, self.player.rect)
        
        # Afficher le pseudo du joueur
        police = pygame.font.SysFont("monospace",25)
        pseudoTxt = police.render(pseudo,1,(0,0,0))
        screen.blit(pseudoTxt, (30,30))
        
        # Afficher le score du joueur
        # scoreTxt = police.render(str(self.player.score),1,(0,0,0))
        scoreTxt = police.render(f"{self.score}",1,(0,0,0))
        screen.blit(scoreTxt, (30,50))

        # Actualiser la vie du joueur
        self.player.update_health_bar(screen)

        # Recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # Recuperer les ennemis
        for monster in self.all_opponents:
            monster.forward()
            monster.update_health_bar(screen)

        # Appliquer les images du groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # Appliqur l'ensemble des images de mon groupe d'ennemis'
        self.all_opponents.draw(screen)

        # Verifier si le joueur va a gauche ou a droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_opponent(self, opponents_class_name):
        self.all_opponents.add(opponents_class_name.__call__(self))