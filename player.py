import pygame
from projectile import Projectile

# Créer joueur
class Player(pygame.sprite.Sprite):

    def __init__(self, game, name):
        super().__init__()
        self.name = name
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 55
        self.velocity = 1
        self.powermode = False
        self.all_projectiles = pygame.sprite.Group()

        self.image = pygame.image.load('assets/' + name + '.png')
        self.image = pygame.transform.scale(self.image, (440/3, 550/3))

        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            # Si le joueur n'as plus de point de vie
            self.game.game_over()

    def update_health_bar(self, surface):
        # Definir une couleur pour la jauge de vie
        bar_color = (59, 226, 18)
        # Background de la barre de vie (gris foncé)
        back_bar_color = (60, 63, 60)

        # Definir la position de la jauge de vie (ainsi que largeur et epaisseur)
        bar_position = [self.rect.x + 20, self.rect.y - 10, self.health, 7]
        back_bar_position = [self.rect.x + 20, self.rect.y - 10, self.max_health, 7]

        # Dessiner la barre de vie (background en 1er)
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def launch_projectile(self):
        if not self.powermode:
            self.all_projectiles.add(Projectile(self, self.name + '_projectile'))
        else:
            self.all_projectiles.add(Projectile(self, self.name + '_super_projectile'))


    def move_right(self):
        # Si le joueur n'est pas en collision avec un ennemi
        if not self.game.check_collision(self, self.game.all_opponents):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def powermode_transformation(self):
        self.attack = 110
        self.velocity = 3
        self.health = 150
        self.max_health = 150
        self.powermode = True

        self.image = pygame.image.load('assets/' + self.name + '_powermode.png')
        self.image = pygame.transform.scale(self.image, (148*1.6, 125*1.6))

    def cancel_transformation(self):
        self.attack = 55
        self.velocity = 1
        self.health = 100
        self.max_health = 100
        self.powermode = False

        self.image = pygame.image.load('assets/' + self.name + '.png')
        self.image = pygame.transform.scale(self.image, (440/3, 550/3))
