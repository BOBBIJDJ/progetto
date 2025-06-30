import pygame
import player as pl
import characters as ch
import weapons as wp
import objects as obj
import textboxes as tbx
import copy
from config import X_RATIO, Y_RATIO

class Level:
    def __init__(
        self, 
        name : str, 
        path : str,
        start_pos : tuple[int,int] = (256, 256), 
        characters_ref : list[dict[str, ch.Character | tuple[int, int] | str]] = [], 
        objects_ref : list[dict[str, obj.Object | tuple[int,int]]] = [],
        dialogue_box_ref : list[dict[str, tbx.TextBox | tuple[int, int]]] = [],
        has_fog : bool = False,
        has_bound_mask : bool = False,
        is_menu : bool = False,
    ):
        self.name = name
        self.path = path
        self.scale_fact = (1*X_RATIO, 1*Y_RATIO)
        self.bg = pygame.image.load(f"{self.path}/bg.png")
        self.bg = pygame.transform.scale_by(self.bg, self.scale_fact)
        self.bg_rect = self.bg.get_rect()
        self.player_start_pos = start_pos
        self.characters_ref = characters_ref # lista di dict: [{NPC1, (x,y), rot}, {NPC2, (x,y), rot}, ...]
        self.objects_ref = objects_ref # lista di dict: [{obj1, (x,y)}, {obj2, (x,y)}, ...] 
        self.dialogue_boxes_ref = dialogue_box_ref
        self.passed = False
        self.is_menu = is_menu
        self.has_fog = has_fog
        if self.has_fog:
            self.setFog()
        self.has_bound_mask = has_bound_mask
        if self.has_bound_mask:
            self.setBoundMask()

    def setBoundMask(self):
        mask_surface = pygame.image.load(f"{self.path}/mask.png")
        mask_surface = pygame.transform.scale_by(mask_surface, self.scale_fact)
        self.mask = pygame.mask.from_surface(mask_surface)

    def doesBoundMaskOverlap(
        self, 
        player : pl.Player, 
        player_pos : tuple[int, int],
    ):
        overlap = self.mask.overlap(player.mask, player_pos)
        if overlap:
            return True
        else:
            return False
    
    def setFog(self):
        self.fog_bg = pygame.image.load("assets/fog/fog.png")
        self.fog_bg = pygame.transform.scale_by(self.fog_bg, self.scale_fact)
        fog_circle = pygame.image.load("assets/fog/circle.png")
        fog_circle = pygame.transform.scale_by(fog_circle, self.scale_fact)
        self.fog_circle_mask = pygame.mask.from_surface(fog_circle)

    def setFogPos(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ):
        self.fog_mask = pygame.mask.from_surface(self.fog_bg)
        self.fog_mask.erase(self.fog_circle_mask, (pos[0] - 64, pos[1] - 64))
        self.fog_mask.invert()
        self.fog_mask_surf = self.fog_mask.to_surface()
        self.fog_mask_surf.set_colorkey((255,255,255))
        screen.blit(self.fog_mask_surf, self.bg_rect)

    def setLevel(
        self, 
        screen : pygame.Surface, 
        player : pl.Player,
    ):
        self.characters = copy.deepcopy(self.characters_ref)
        self.objects = copy.deepcopy(self.objects_ref)
        self.dialogue_boxes = self.dialogue_boxes_ref
        screen.blit(self.bg, self.bg_rect)
        player.setPos(
            screen,
            (self.player_start_pos[0]*self.scale_fact[0], 
             self.player_start_pos[1]*self.scale_fact[1]),
        )
        for character in self.characters:
            character["type"].setPos(
                screen, 
                (character["pos"][0]*self.scale_fact[0], 
                 character["pos"][1]*self.scale_fact[1]), 
                character["rot"],
            )
        for object in self.objects:
            object["type"].setPos(
                screen, 
                (object["pos"][0]*self.scale_fact[0], 
                 object["pos"][1]*self.scale_fact[1]),
            )

    def blitLevel(
        self, 
        screen : pygame.Surface, 
        frame : int,
    ):
        screen.blit(self.bg, self.bg_rect)

        for character in self.characters:
           character["type"].idle(screen, character["rot"], frame)
        for object in self.objects:
            object["type"].show(screen)

    def playLevel(
        self, 
        screen : pygame.Surface,
        player : pl.Player, 
        clock : pygame.Clock, 
        max_fps : int,
    ):
        self.setLevel(screen, player)
        frame = 0
        level_passed = False
        self.quit = False
        in_inventory = False
        
        while ((not self.quit) 
               and (not level_passed) 
               and (not player.is_dead)
        ):
            
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit = True
                elif (event.type == pygame.KEYDOWN 
                      and (event.key == pygame.K_i)
                    ):
                    in_inventory = not in_inventory
            

            self.blitLevel(screen, frame)
            
            player_next_pos = player.getNextPos(keys)

            if (in_inventory 
                or (self.has_bound_mask 
                    and self.doesBoundMaskOverlap(player, player_next_pos))
                ):
                player.idle(frame)
            else:
                player.move(frame)

            if self.is_menu:
                level_passed = self.chooseClass(player, keys)
            else:
                for object in self.objects:
                    if (object["type"].has_collision 
                        and player.rect.colliderect(object["type"].rect)
                    ):
                        object["type"].collision()
            # if self.is_menu:
            #     level_passed = self.chooseClass(screen, player)
            # else:
            #     # self.checkCollision()
            #     for character in self.characters:
            #        character[0].idle(self.screen, character[2], frame)
            #     #    if player.rect.colliderect(character[0].rect):
            #     #        if character[0].collision_type == "battle":
            #     #            self.playBattle(character[0])
            #     #            character[0].collision_type = "nobattle"
            
            if self.has_fog:
                self.setFogPos(screen, player.rect.center)
            
            for dialogue in self.dialogue_boxes:
                dialogue["box"].show(screen, dialogue["pos"])

            # if keys[pygame.K_i]:
            #     in_inventory = not in_inventory
            
            if in_inventory:
                player.inventory.show(screen)

            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)
        if not self.quit:
            self.passed = True

    def playBattle(
        self, 
        player : pl.Player, 
        enemy : ch.Enemy, 
        clock : pygame.Clock, 
        max_fps : int
    ):
        frame = 0
        victory = False
        while (not self.quit) and (not victory):
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit = True
            
            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)
    
    def chooseClass(
        self,  
        player : pl.Player, 
        keys : list[int]
    ):
        for character in self.characters:
            if (player.rect.colliderect(character["type"].rect) 
                and (player.name != character["type"].name) 
                and keys[pygame.K_e]
            ):
                player.setPlayerClass(character["type"])
                return True

# class Menu(Level):
#     def __init__(
#         self, 
#         name : str,
#         path : str, 
#         win_rect : pygame.Rect, 
#         scale_fact : int, 
#         player_classes : list[ch.Subplayer]
#     ):
#         Level.__init__(self, name, path, win_rect, scale_fact, characters_ref = player_classes)
#         self.player_start_pos = (32, 32)
#         self.is_menu = True
levels = [ 
    Level(
        "Start Menu", 
        "assets/levels/menu", 
        start_pos = (32,32), 
        is_menu = True, 
        characters_ref = [
            {
                "type" : copy.deepcopy(ch.knight), 
                "pos" : (256, 240), 
                "rot" : "left",
            },
            {
                "type" : copy.deepcopy(ch.mage), 
                "pos" : (336,240), 
                "rot" : "left",
            },
            {
                "type" : copy.deepcopy(ch.archer), 
                "pos" : (176, 240), 
                "rot" : "left",
            },
        ],
    ),
    Level(
        "Maze", 
        "assets/levels/maze", 
        start_pos = (256, 480), 
        has_fog = False, 
        has_bound_mask = True,
        characters_ref = [
            {
                "type" : copy.deepcopy(ch.knight), 
                "pos" : (256, 240), 
                "rot" : "left",
            },
            {
                "type" : copy.deepcopy(ch.mage), 
                "pos" : (336,240), 
                "rot" : "left",
            },
            {
                "type" : copy.deepcopy(ch.archer), 
                "pos" : (176, 240), 
                "rot" : "left",
            },
        ],
        objects_ref = [
            {
                "type" : copy.deepcopy(obj.chest), 
                "pos" : (400, 400),
            },
        ],
        dialogue_box_ref = [
            {
                "box" : tbx.test_dialogue, 
                "pos" : (256,256),
            },
        ],
    ),
]