# autore: Diego Cincotta

import pygame

from config import SIZE, levels_data
import characters as ch
import player as pl
import weapons as wp
import objects as obj
import textboxes as tbx
import level as lv

# inizializzazione della finestra di gioco
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
max_fps = 60

# inizializzazione del personaggio controllato dal giocatore
player = pl.Player(screen, 4)

# contatore frame per la gestione delle animazioni
frame_count = 0

# inizio del game loop
running = True

levels = [
    lv.Level(**level) for level in levels_data
]

while running:

    # ad inizio loop si controllano eventuali eventi o tasti premuti
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # si controlla se tra gli eventi c'è la chiusura della finestra
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
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

    # si fissa il numero massimo di frame al secondo
    clock.tick(max_fps)

pygame.quit()
