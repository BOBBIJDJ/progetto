# autore: Diego Cincotta

# modulo per la gestione della finestra e del game loop
import pygame
# file con le classi per la gestione di Giocatore, NPC e armi
import characters as ch
import player as pl
import weapons as wp
import objects as obj
import textboxes as tbx
# file con la classe per la gestione dei livelli
import level as lv
import copy
from config import * # SIZE, WIDTH, HEIGHT, X_RATIO, Y_RATIO, MIN_RATIO, MAX_RATIO
# dimensioni della finestra di gioco
# SIZE = (WIDTH, HEIGHT) = (512, 512)

# inizializzazione della finestra di gioco
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
max_fps = 60
# font = pygame.font.Font("assets/font/pixel.ttf")
# creazione del rettangolo rappresentante la finestra di gioco da
# usare come limite per gli altri oggetti
CLAMP_RECT = pygame.Rect(
    (16*X_RATIO),(16*Y_RATIO),WIDTH-(32*X_RATIO),HEIGHT-(32*Y_RATIO)
)

# inizializzazione del personaggio controllato dal giocatore
player = pl.Player(screen, CLAMP_RECT, 4)

# text = font.render("Start", False, "white")
# text_rect = text.get_rect()
# text_rect.center = (256,256)

# contatore frame per la gestione delle animazioni
frame_count = 0

# inizio del game loop
running = True
in_menu = True

levels = lv.levels

while running:

    # ad inizio loop si controllano eventuali eventi o tasti premuti
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # si controlla se tra gli eventi c'è la chiusura della finestra
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
    # if player.rect.colliderect(text_rect):
    #     start = True
        # text = font.render("Start", False, "red")

    for level in levels:
        if not level.passed:
            level.playLevel(screen, player, clock, max_fps)
            if not level.passed:
                running = False
                break
    
    # infine si aggiorna la finestra di gioco con le modifiche effettuate
    pygame.display.flip()
    # e si aumenta il contatore dei frame
    frame_count += 1

    # si fissa ssil numero massimo di frame al secondo
    clock.tick(max_fps)

pygame.quit()
