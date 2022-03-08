import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 1
        self.player = player
        # self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.image.load('assets/rasengan.png')

        # Reduction de l'image du projectile
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()

        # Position du projectile
        self.rect.x = player.rect.x + 100
        self.rect.y = player.rect.y + 70

        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # Tourner le projectile
        self.angle += 1
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        # Verifier si le projectile entre en collision avec un monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            # Suppression du projectile
            self.remove()
            # Infliger des dégats
            monster.damage(self.player.attack)

        # Verifier si le projectile sort de l'ecran
        if self.rect.x > 1080:
            # Suppression du projectile
            self.remove()