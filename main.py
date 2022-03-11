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
play_button_naruto = pygame.image.load('assets/button_naruto.png')
play_button_naruto = pygame.transform.scale(play_button_naruto, (150, 150))
play_button_naruto_rect = play_button_naruto.get_rect()
play_button_naruto_rect.x = math.ceil(screen.get_width() / 2.9)
play_button_naruto_rect.y = math.ceil(screen.get_height() / 3)

# Boutton Sakura
play_button_sakura = pygame.image.load('assets/button_sakura.png')
play_button_sakura = pygame.transform.scale(play_button_sakura, (150, 150))
play_button_sakura_rect = play_button_sakura.get_rect()
play_button_sakura_rect.x = math.ceil(screen.get_width() / 2)
play_button_sakura_rect.y = math.ceil(screen.get_height() / 3)

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
            if play_button_naruto_rect.collidepoint(event.pos):
                # Incarner Naruto
                game.start('naruto', 'rasengan', 'oodame_rasengan')
                # Jouer le son
                pygame.mixer.Sound("assets/sounds/naruto_voice.mp3").play()
            elif play_button_sakura_rect.collidepoint(event.pos):
                # Incarner Sakura
                game.start('sakura', 'kunai', 'double_kunai')
                # Jouer le son
                pygame.mixer.Sound('assets/sounds/sakura_voice.mp3').play()