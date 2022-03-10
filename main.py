import pygame
import math
from game import Game

pygame.init()


# Generer la fenetre de jeu
pygame.display.set_caption("Konoha Battle")
screen = pygame.display.set_mode((1080, 720))

# Importer background
background = pygame.image.load('assets/bg_forest.jpg')

# Charger la banniere
banner = pygame.image.load('assets/naruto_banner.png')
banner = pygame.transform.scale(banner, (2560/4, 1090/4))
banner_rect = banner.get_rect()
# On utilise math.ceil pour arrondir a un entier
banner_rect.x = math.ceil(screen.get_width() / 5)
banner_rect.y = math.ceil(screen.get_height() / 5)


#choix du perso
#menu.add.selector('personnage :'), [('naruto', 1), ('sakura',2)], onchange=set_difficulty)

# Importer un bouton pour charger la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

# Charger le jeu
game = Game()

running = True
# Boucle tant que running = True
while running:

    # Appliquer le background
    background = pygame.transform.scale(background, (1080, 720))
    screen.blit(background, (0, 0))

    # Verifier si le jeu a commencé
    if game.is_playing:
        # Déclencher les instructions de partie
        game.update(screen)
    # Si le jeu n'a pas commencé
    else:
        # Ajout de l'écran de bienvenue
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    # Mettre a jour l'écran
    pygame.display.flip()

    # Si le joueur ferme la fenetre
    for event in pygame.event.get():

        # Event = fermeture de la fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")

        # Event keydown
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()
            elif event.key == pygame.K_x:
                game.player.kyuubi_transformation()
            elif event.key == pygame.K_w:
                game.player.cancel_transformation()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verification si la souris est en collision avec le boutton "play"
            if play_button_rect.collidepoint(event.pos):
                # Mettre le jeu en mode "lancé"
                game.start()
                #jouer le son
                click_song = pygame.mixer.Sound("assets/sounds/click.ogg")
                click_song.play()