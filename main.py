import pygame_textinput
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

# Importer un bouton pour charger la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

# Définir la zonne de saisie de texte du joueur
textinput = pygame_textinput.TextInputVisualizer()
# clock = pygame.time.Clock()
pseudo=""

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
        game.update(screen,pseudo)
        
    # Si le jeu n'a pas commencé
    else:
        if pseudo=="":
            # Le joueur renseigne son pseudo
            events = pygame.event.get()

            textinput.update(events)
            textinput.cursor_blink_interval = 100
            width, height = screen.get_size()
            screen.blit(textinput.surface, (-400+width/2, height/2))

            color = (0,0,0) 
            pygame.draw.rect(screen, color, pygame.Rect(-405+width/2, -5+height/2, 700, 40),  2)

            police = pygame.font.SysFont("monospace",40)
            texte = police.render("Rentrer votre pseudo",1,(255,255,255))
            screen.blit(texte,(-275+width/2, -75+height/2))

            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pseudo = textinput.value 

            # pygame.display.update()
            # clock.tick(30)
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