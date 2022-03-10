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
banner = pygame.image.load('assets/game_banner.png')
banner = pygame.transform.scale(banner, (2560/6, 1090/6))
banner_rect = banner.get_rect()
# On utilise math.ceil pour arrondir a un entier
banner_rect.x = math.ceil(screen.get_width() / 3.33)
banner_rect.y = math.ceil(screen.get_height() / 10)

# Boutton Naruto
play_button_naruto = pygame.image.load('assets/naruto_button.png')
play_button_naruto = pygame.transform.scale(play_button_naruto, (150, 150))
play_button_naruto_rect = play_button_naruto.get_rect()
play_button_naruto_rect.x = math.ceil(screen.get_width() / 2.9)
play_button_naruto_rect.y = math.ceil(screen.get_height() / 3)

# Boutton Sakura
play_button_sakura = pygame.image.load('assets/sakura_button.png')
play_button_sakura = pygame.transform.scale(play_button_sakura, (150, 150))
play_button_sakura_rect = play_button_sakura.get_rect()
play_button_sakura_rect.x = math.ceil(screen.get_width() / 2)
play_button_sakura_rect.y = math.ceil(screen.get_height() / 3)

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
        # Ajout de l'écran de demarrage
        screen.blit(play_button, play_button_rect)
        screen.blit(play_button_naruto, play_button_naruto_rect)
        screen.blit(play_button_sakura, play_button_sakura_rect)
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
                game.player.powermode_transformation()
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