# autore: Diego Cincotta

import pygame

from config import SIZE, saveState, ASSETS_PATH
import player as pl
import level as lv

# inizializzazione della finestra di gioco
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
max_fps = 60

# contatore frame per la gestione delle animazioni
frame_count = 0

start_menu = lv.StartMenu()

levels_data = start_menu.getLevels(screen)

if not start_menu.quit:
    player = pl.Player(**(levels_data["player"]))
    new_data = False
    
    # inizio del game loop
    running = True
else:
    running = False

while running:

    # ad inizio loop si controllano eventuali eventi o tasti premuti
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # si controlla se tra gli eventi c'è la chiusura della finestra
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
    for level in levels_data["levels"]:
        if level["passed"]:
            continue
        current_level = lv.CLASSES[level["class"]](**level["args"])
        if not current_level.passed:
            current_level.playLevel(screen, player, clock, max_fps)
        if not current_level.quit:
            level["passed"] = True
            levels_data["player"] = player.getData()
            new_data = True
        else:
            running = False
            break
        del current_level
    
    # infine si aggiorna la finestra di gioco con le modifiche effettuate
    pygame.display.flip()
    # e si aumenta il contatore dei frame
    frame_count += 1

    # si fissa il numero massimo di frame al secondo
    clock.tick(max_fps)

if new_data:
    saveState(levels_data)

pygame.quit()
