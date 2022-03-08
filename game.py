import pygame
from player import Player
from monster import Monster

class Game:

    def __init__(self):
        # Definir si le jeu a commencé
        self.is_playing = False

        # Generer joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        # Groupe de monstres
        self.all_monsters = pygame.sprite.Group()

        self.pressed = {}

    def start(self):
        self.is_playing = True

        # On genere 2 monstres
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        # Reset du jeu (retirer les monstres, remettre le joueur a 100 de vie, remettre la banniere de lancement)
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False

    def update(self, screen):
        # Appliquer l'image du joueur
        screen.blit(self.player.image, self.player.rect)

        # Actualiser la vie du joueur
        self.player.update_health_bar(screen)

        # Recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # Recuperer les monstres
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)

        # Appliquer les images du groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # Appliqur l'ensemble des images de mon groupe de monstres
        self.all_monsters.draw(screen)

        # Verifier si le joueur va a gauche ou a droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)