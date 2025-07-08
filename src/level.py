'''
## Gestisce la classe Level per la rappresentazione e la riproduzione 
## dei livelli del gioco
'''

import copy
from typing import Literal

import pygame

import player as pl
import characters as ch
import weapons as wp
import objects as obj
import textboxes as tbx

from config import X_RATIO, Y_RATIO, ASSETS_PATH

JSON_list = list
Rotation = Literal["left", "right"]
CharacterSet = list[
    dict[
        str, 
        ch.Character | tuple[int, int] | Literal["left", "right"]
    ]
]
ObjectSet = list[
    dict[
        str, 
        obj.Object | tuple[int, int]
    ]
]

class Level:
    '''
    ## Una classe per rappresentare i livelli del gioco.

    ### Attributi
    passed -> bool:
        stato di superamento del livello
    
    ### Metodi
    playLevel(screen, player, clock, max_fps) -> None:
        imposta il livello e lo riproduce con un sub-gameloop

    '''
    def __init__(
        self,
        name : str,
        is_menu : bool = False,
        has_fog : bool = False,
        scale_fact : int | float = 1,
        start_pos : tuple[int, int] = (256, 256), 
        characters : JSON_list = [], 
        objects : JSON_list = [],
        dialogues : JSON_list = [],
    ) -> None:
        '''
        ## Inizializza un oggetto Livello -> None

        ### Parametri:
            name = nome del livello (e della cartella corrispondente) 
                -> str
            start_pos = posizione iniziale del giocatore
                -> tuple[int, int] 
            characters_ref = lista delle entità presenti nel livello
                -> [
                    {
                        "type" : tipo di entità (es. ch.Subplayer(...)),
                        "pos" : tuple[int, int] (es. (x, y)),
                        "rot" : Rotation ("left" o "right"),
                    },
                    ...
                ]
            objects_ref = lista di oggetti presenti nel livello
                -> [
                    {
                        "type" : tipo di oggetto (es. obj.Chest()),
                        "pos" : tuple[int, int] ( es. (x, y)),
                    },
                    ...
                ]
            dialogue_box_ref = lista di finestra di dialogo presenti
                -> [
                    {
                        "type" : tipo di finestra (es. tbx.TextBox(...)),
                        "pos" : tuple[int, int] (es (x, y))
                    },
                    ...
                ]
            has_fog = attiva o disattiva l'effetto visuale oscurata 
                -> bool
            is_menu = attiva o disattiva la scelta della classe 
                -> bool
            scale_fact = fattore di ingrandimento -> int o float
        '''
        self._name = name
        self._path = f"{ASSETS_PATH}/levels/{self._name}"
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._bg = pygame.image.load(f"{self._path}/bg.png")
        self._bg = pygame.transform.scale_by(self._bg, self._scale_fact)
        self._bg_rect = self._bg.get_rect()
        # self._battle_bg = pygame.image.load(f"assets/levels/battle/bg.png")
        # self._battle_bg = pygame.transform.scale_by(self._bg, self._scale_fact)
        # self._battle_bg_rect = self._battle_bg.get_rect()
        self._player_start_pos = start_pos
        self._characters_ref = characters # [{"type" : NPC1, "pos" : (x,y), "rot" : rot}, ...]
        self._objects_ref = objects # [{"type" : obj1, "pos" : (x,y)}, ...] 
        self._dialogues_ref = dialogues
        self.passed = False
        self._is_menu = is_menu
        self._has_fog = has_fog
        self._setBoundMask()
        if self._has_fog:
            self._setFog()

    def _getCharacters(self):
        self._characters : CharacterSet = []
        for character in self._characters_ref:
            class_ = character["type"]["class"]
            kwargs = character["type"]["args"]
            self._characters.append({
                "type" : ch.CLASSES[class_](**kwargs),
                "pos" : character["pos"],
                "rot" : character["rot"],
            })
            
    def _getObjects(self):
        self._objects : ObjectSet= []
        for object in self._objects_ref:
            class_ = object["type"]["class"]
            kwargs = object["type"]["args"]
            self._objects.append({
                "type" : obj.CLASSES[class_](**kwargs),
                "pos" : object["pos"],
            })
        
    def _getDialogues(self):
        self._dialogues = []
        for box in self._dialogues_ref:
            class_ = box["type"]["class"]
            kwargs = box["type"]["args"]
            self._dialogues.append({
                "type" : tbx.CLASSES[class_](**kwargs),
            })

    def _setBoundMask(self) -> None:
        '''
        ## Imposta la maschera per le collisioni con il livello -> None
        '''
        mask_surface = pygame.image.load(f"{self._path}/mask.png")
        mask_surface = pygame.transform.scale_by(mask_surface, self._scale_fact)
        self._mask = pygame.mask.from_surface(mask_surface)

    def _doesBoundMaskOverlap(
        self, 
        player : pl.Player, 
    ) -> bool:
        '''
        ## Verifica la collisione tra la maschera del giocatore e quella
        del livello -> bool
        '''
        overlap = self._mask.overlap(player.mask, player.next_pos)
        if overlap is None:
            return False
        else:
            return True
    
    def _setFog(self) -> None:
        '''
        ## Imposta la maschera per la visuale oscurata -> None
        '''
        self._fog_bg = pygame.image.load("assets/fog/fog.png")
        self._fog_bg = pygame.transform.scale_by(self._fog_bg, self._scale_fact)
        fog_circle = pygame.image.load("assets/fog/circle.png")
        fog_circle = pygame.transform.scale_by(fog_circle, self._scale_fact)
        self.fog_circle_mask = pygame.mask.from_surface(fog_circle)

    def _setFogPos(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        '''
        ## Sposta la maschera per la visuale oscurata -> None
        '''
        self._fog_mask = pygame.mask.from_surface(self._fog_bg)
        self._fog_mask.erase(self.fog_circle_mask, (pos[0] - 64, pos[1] - 64))
        self._fog_mask.invert()
        self._fog_mask_surf = self._fog_mask.to_surface()
        self._fog_mask_surf.set_colorkey((255,255,255))
        screen.blit(self._fog_mask_surf, self._bg_rect)
    
    def _setBattle(
        self,
        screen : pygame.Surface,
        player : pl.Player,
        enemy : ch.Enemy,
    ) -> None:
        tmp = 0 # SOSTITUIRE posizione di partenza
        screen.blit(self._battle_bg, self._battle_bg_rect)
        player.setPos(
            screen,
            (tmp*self._scale_fact[0], tmp*self._scale_fact[1]),
        )
        enemy.setPos(
            screen,
            (tmp*self._scale_fact[0], tmp*self._scale_fact[1]),
        )


    def _setLevel(
        self, 
        screen : pygame.Surface, 
        player : pl.Player,
    ) -> None:
        '''
        ## Inizializza gli elementi del livello -> None
        '''
        self._getCharacters()
        self._getObjects()
        self._getDialogues()
        screen.blit(self._bg, self._bg_rect)
        player.setPos(
            screen,
            (self._player_start_pos[0]*self._scale_fact[0], 
             self._player_start_pos[1]*self._scale_fact[1]),
        )
        for character in self._characters:
            character["type"].setPos(
                screen, 
                (character["pos"][0]*self._scale_fact[0], 
                 character["pos"][1]*self._scale_fact[1]), 
                character["rot"],
            )
        for object in self._objects:
            object["type"].setPos(
                screen, 
                (object["pos"][0]*self._scale_fact[0], 
                 object["pos"][1]*self._scale_fact[1]),
            )

    def _blitLevel(
        self, 
        screen : pygame.Surface, 
        frame : int,
    ) -> None:
        '''
        ## Rappresenta gli elementi del livello sul frame attuale -> None
        '''
        screen.blit(self._bg, self._bg_rect)

        for character in self._characters:
           character["type"].idle(screen, character["rot"], frame)
        for object in self._objects:
            object["type"].show(screen)

    def _canMove(self, player : pl.Player) -> bool:
        '''
        ## Verifica la possibilità del giocatore di muoversi -> bool
        '''
        if (not self._in_inventory) and (not self._doesBoundMaskOverlap(player)):
            return True
        else:
            return False

    def playLevel(
        self, 
        screen : pygame.Surface,
        player : pl.Player, 
        clock : pygame.Clock, 
        max_fps : int,
    ) -> None:
        '''
        ## Riproduce il sub-gameloop relativo al livello -> None
        '''
        self._setLevel(screen, player)
        frame = 0
        level_passed = False
        self._quit = False
        self._in_inventory = False
        
        while ((not self._quit) 
               and (not level_passed) 
               and (not player.is_dead)
        ):
            
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self._quit = True
                elif (event.type == pygame.KEYDOWN 
                      and (event.key == pygame.K_i)
                    ):
                    self._in_inventory = not self._in_inventory
            

            self._blitLevel(screen, frame)
            
            player.getNextPos(keys)
            
            self._can_move = self._canMove(player)

            if self._can_move:
                player.move(frame)
            else:
                player.idle(frame)

            if self._is_menu:
                level_passed = self._chooseClass(player, keys)

            for character in self._characters:
                if (character["type"].has_collision
                    and player.rect.colliderect(character["type"].rect)
                ):
                    if character["type"].is_hostile:
                        self._playBattle(
                            player, character["type"], clock, max_fps
                        )
                    else:
                        pass

            for object in self._objects:
                if (object["type"].has_collision 
                    and player.rect.colliderect(object["type"].rect)
                ):
                    object["type"].collision()

            # if self._is_menu:
            #     level_passed = self._chooseClass(screen, player)
            # else:
            #     # self.checkCollision()
            #     for character in self._characters:
            #        character[0].idle(self.screen, character[2], frame)
            #     #    if player.rect.colliderect(character[0].rect):
            #     #        if character[0].collision_type == "battle":
            #     #            self._playBattle(character[0])
            #     #            character[0].collision_type = "nobattle"
            
            if self._has_fog:
                self._setFogPos(screen, player.rect.center)
            
            for dialogue in self._dialogues:
                dialogue["box"].show(screen, dialogue["pos"])

            # if keys[pygame.K_i]:
            #     in_inventory = not in_inventory
            
            if self._in_inventory:
                player.inventory.show(screen)

            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)
            
        if not self._quit:
            self.passed = True

    def _playBattle(
        self, 
        player : pl.Player, 
        enemy : ch.Enemy, 
        clock : pygame.Clock, 
        max_fps : int,
    ) -> None:
        '''
        ## Riproduce il sub-gameloop relativo alla lotta -> None
        '''
        frame = 0
        victory = False
        while (not self._quit) and (not victory):
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self._quit = True
            
            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)
    
    def _chooseClass(
        self,  
        player : pl.Player, 
        keys : list[int],
    ) -> bool:
        '''
        ## Verifica la scelta della classe del giocatore -> bool
        '''
        for character in self._characters:
            if (player.rect.colliderect(character["type"].rect)  
                and keys[pygame.K_e]
            ):
                player.setPlayerClass(character["type"])
                return True
        return False