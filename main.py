import json
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

# Définir la zonne de saisie de texte du joueur
textinput = pygame_textinput.TextInputVisualizer()
pseudo = ""

# data score
loopDataScore = 0

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
        game.update(screen, pseudo)
        
    # Si le jeu n'a pas commencé
    else:

        # Si pas de pseudo
        if pseudo == "":

            events = pygame.event.get()
            # Gestion de l'input
            textinput.update(events)
            textinput.cursor_blink_interval = 100

            # On set la longueur et la largeur de l'ecran
            width, height = screen.get_size()
            # Affichage de l'input
            screen.blit(textinput.surface, (-400 + width / 2, height / 2))

            # Couleur de l'input
            color = (0, 0, 0)

            # Affichage du carré contenant l'input
            pygame.draw.rect(screen, color, pygame.Rect(-405 + width / 2, -5 + height / 2, 700, 40),  2)

            # Gestion du titre de l'input
            police = pygame.font.SysFont("monospace", 40)
            text = police.render("Rentrer votre pseudo", 1, (255, 255, 255))

            # Affichage du titre de l'input
            screen.blit(text, (-275 + width / 2, -75 + height / 2))

            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enregistrement du pseudo apres appuie sur "enter"
                        pseudo = textinput.value 

        else:
            # Gestion de la police et de la taille du score
            police = pygame.font.SysFont("monospace", 20)
            head = police.render("Pseudo Score", 1, (0, 0, 0))

            # Ajout de l'écran de demarrage
            screen.blit(play_button_naruto, play_button_naruto_rect)
            screen.blit(play_button_sakura, play_button_sakura_rect)
            screen.blit(banner, banner_rect)
            screen.blit(head, (30, 10))

            # Lecture du score.json
            with open("score.json", 'r') as objfile:
                if loopDataScore < 1:
                    data = json.loads(objfile.read())

            # Affichage des 3 premieres (ordre décroissant)
            data.sort(key=lambda x: x.get('score'), reverse=True)
            loopDataScore += 1

            i = 0
            loop = 0
            for d in data:
                if loop == 3:
                    break
                ligne = police.render(f"{d['pseudo']} {d['score']}", 1, (0, 0, 0))
                screen.blit(ligne, (30, 30 + i))
                i += 20
                loop += 1

    # Mettre à jour l'écran
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

            # Verification si la souris est en collision avec le boutton "personnage"
            if play_button_naruto_rect.collidepoint(event.pos):

                # Init data json
                loopDataScore = 0
                # Incarner Naruto
                game.start('naruto', 'rasengan', 'oodama_rasengan')
                # Jouer le son
                pygame.mixer.Sound("assets/sounds/naruto_voice.mp3").play()
            elif play_button_sakura_rect.collidepoint(event.pos):
                
                # Init data json
                loopDataScore = 0
                # Incarner Sakura
                game.start('sakura', 'kunai', 'double_kunai')
                # Jouer le son
                pygame.mixer.Sound('assets/sounds/sakura_voice.mp3').play()
