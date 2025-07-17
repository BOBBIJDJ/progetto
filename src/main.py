# autore: Diego Cincotta

import pygame

from config import SIZE, saveState
import player as pl
import level as lv

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
max_fps = 60

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

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

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
    
    pygame.display.flip()
    frame_count += 1

    clock.tick(max_fps)

if new_data:
    saveState(levels_data)

pygame.quit()