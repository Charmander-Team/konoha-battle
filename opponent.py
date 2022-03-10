import pygame
import random

class Opponent(pygame.sprite.Sprite):

    def __init__(self, game, name):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.5
        self.velocity = 1

        # Recuperer l'image de l'ennemi
        self.image = pygame.image.load('assets/' + name + '.png')
        self.image = pygame.transform.scale(self.image, (148*1.5, 125*1.5))
        self.rect = self.image.get_rect()

        # Positionner l'image
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 510

        # Init score du player
        self.score = 0
        self.scoreIncrement = 0

    def damage(self, amount):
        # Infliger les dégats
        self.health -= amount


        # Verifier si sa vie est < 0
        if self.health <= 0:
            # Réapparaitre (comme un nouvel ennemi)
            self.rect.x = 1000 + random.randint(0, 300)
            self.health = self.max_health
            
            # incrémentation du score
            self.game.score += self.scoreIncrement

    def update_health_bar(self, surface):
        # Definir une couleur pour la jauge de vie
        bar_color = (59, 226, 18)
        # Background de la barre de vie (gris foncé)
        back_bar_color = (60, 63, 60)

        # Definir la position de la jauge de vie (ainsi que largeur et epaisseur)
        bar_position = [self.rect.x + 50, self.rect.y - 15, self.health, 5]
        back_bar_position = [self.rect.x + 50, self.rect.y - 15, self.max_health, 5]

        # Dessiner la barre de vie (background en 1er)
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def forward(self):
        # Déplacement possible SI il n'y a pas de collision
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # Sinon (l'annemi est en collision avec le joueur)
        else:
            # Infliger des dégats au joueur
            self.game.player.damage(self.attack)


class Orochimaru(Opponent):

    def __init__(self, game):
        super().__init__(game, "orochimaru")
        self.health = 200
        self.max_health = 200
        self.scoreIncrement = 15

    def update_health_bar(self, surface):

        # Dessiner la barre de vie (background en 1er)
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x, self.rect.y - 10, self.max_health, 7])
        pygame.draw.rect(surface, (59, 226, 18), [self.rect.x, self.rect.y - 10, self.health, 7])


class Kabuto(Opponent):

    def __init__(self, game):
        super().__init__(game, "kabuto")
        self.scoreIncrement = 5