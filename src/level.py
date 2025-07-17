import pygame

import player as pl
import characters as ch
import weapons as wp
import objects as obj
import textboxes as tbx

from config import (
    X_RATIO, Y_RATIO, ASSETS_PATH, LOADED, 
    default_levels_data, loaded_levels_data
)

MESSAGES = {
    "vittoria" : "Nemico sconfitto! +1 livello, (premere INVIO)",
    "rigenerato" : "Ti sei rigenerato",
    "critico" : "Colpo critico!",
    "super" : "Colpo superefficace!",
    "morto" : "Sei morto! (premere INVIO)",
    "nemico_rigenerato" : "si è rigenerato",
    "nemico_critico" : "è un colpo critico!",
    "nemic_super" : "è superefficace!",
}

pygame.mixer.init()
SFX = {
    "attack" : pygame.mixer.Sound(f"{ASSETS_PATH}/SFX/attack.ogg"),
    "chest" : pygame.mixer.Sound(f"{ASSETS_PATH}/SFX/chest.ogg"),
    "start" : pygame.mixer.Sound(f"{ASSETS_PATH}/SFX/start.ogg"),
}

class PrimitiveLevel:
    def __init__(
        self,
        name : str,
        start_pos : tuple[int, int], 
        music : str | None = None,
        scale_fact : int | float = 1,
        characters : list = [],
        objects : list = [],
    ) -> None:
        self._name = name
        self._path = f"{ASSETS_PATH}/levels/{self._name}"
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._bg = pygame.image.load(f"{self._path}/bg.png")
        self._bg = pygame.transform.scale_by(self._bg, self._scale_fact)
        self._bg_rect = self._bg.get_rect()
        self._player_start_pos = start_pos
        self._characters_ref = characters 
        self._objects_ref = objects
        self.passed = False
        if music is not None:
            self._music_path = f"{ASSETS_PATH}/music/{music}.ogg"
        else:
            self._music_path = None
        self._setBoundMask()

    def _getCharacters(self) -> None:
        self._characters = []
        for character in self._characters_ref:
            class_ = character["type"]["class"]
            kwargs = character["type"]["args"]
            self._characters.append({
                "type" : ch.CLASSES[class_](**kwargs),
                "pos" : character["pos"],
                "rot" : character["rot"],
            })

    def _getObjects(self) -> None:
        self._objects = []
        for object in self._objects_ref:
            kwargs = object["type"]["args"]
            self._objects.append({
                "type" : obj.Chest(**kwargs),
                "pos" : object["pos"],
            })

    def _setBoundMask(self) -> None:
        mask_surface = pygame.image.load(f"{self._path}/mask.png")
        mask_surface = pygame.transform.scale_by(mask_surface, self._scale_fact)
        self._mask = pygame.mask.from_surface(mask_surface)

    def _doesBoundMaskOverlap(
        self, 
        player : pl.Player, 
    ) -> bool:
        overlap = self._mask.overlap(player.mask["last"], player.next_pos)
        if overlap is None:
            return False
        else:
            return True

    def _setLevel(
        self, 
        screen : pygame.Surface, 
        player : pl.Player,
    ) -> None:
        self._getCharacters()
        self._getObjects()
        screen.blit(self._bg, self._bg_rect)
        player.setPos(
            screen,
            (self._player_start_pos[0]*self._scale_fact[0], 
             self._player_start_pos[1]*self._scale_fact[1]),
        )
        player.regenerate()
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
        screen.blit(self._bg, self._bg_rect)

        for character in self._characters:
           character["type"].idle(screen, frame, character["rot"])
        for object in self._objects:
            object["type"].show(screen)

    def _canMove(self, player : pl.Player) -> bool:
        if (not self._in_inventory) and (not self._doesBoundMaskOverlap(player)):
            return True
        else:
            return False
        
    def _checkEvents(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self._in_inventory = not self._in_inventory
                elif event.key == pygame.K_RETURN:
                    self._next_page = not self._next_page

    def _playMusic(self) -> None:
        if self._music_path is not None:
            pygame.mixer.music.load(self._music_path)
            pygame.mixer.music.play(loops=-1, fade_ms=2000)

class Level(PrimitiveLevel):
    def __init__(
        self,
        name : str,
        exit_point : tuple[int, int],
        start_pos : tuple[int, int],
        music : str | None = None,
        has_fog : bool = False,
        scale_fact : int | float = 1,
        characters : list = [],
        objects : list = [],
    ) -> None:
        PrimitiveLevel.__init__(
            self, name, start_pos, music, scale_fact, characters, objects
        )
        self._battle_bg = pygame.image.load(f"{self._path}/battle.png")
        self._battle_bg = pygame.transform.scale_by(self._battle_bg, self._scale_fact)
        self._battle_bg_rect = self._bg_rect
        self._hp_bar = pygame.image.load(f"{ASSETS_PATH}/hp/hp.png")
        self._hp_bar = pygame.transform.scale_by(self._hp_bar, self._scale_fact)
        self._has_fog = has_fog
        self._exit_point = ( 
            (exit_point[0]*X_RATIO, 
             exit_point[1]*Y_RATIO) 
            if exit_point is not None else None                    
        )
        if self._has_fog:
            self._setFog()

    def _checkExit(
        self,
        player : pl.Player,
    ) -> bool:
        if ((self._exit_point is not None)
            and player.rect.collidepoint(self._exit_point)):
            return True
        else:
            return False

    def _setFog(self) -> None:
        self._fog_bg = pygame.image.load(f"{ASSETS_PATH}/fog/fog.png")
        self._fog_bg = pygame.transform.scale_by(self._fog_bg, self._scale_fact)
        fog_circle = pygame.image.load(f"{ASSETS_PATH}/fog/circle.png")
        fog_circle = pygame.transform.scale_by(fog_circle, self._scale_fact)
        self.fog_circle_mask = pygame.mask.from_surface(fog_circle)

    def _setFogPos(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        self._fog_mask = pygame.mask.from_surface(self._fog_bg)
        self._fog_mask.erase(self.fog_circle_mask, (pos[0] - 64, pos[1] - 64))
        self._fog_mask.invert()
        self._fog_mask_surf = self._fog_mask.to_surface()
        self._fog_mask_surf.set_colorkey((255,255,255))
        screen.blit(self._fog_mask_surf, self._bg_rect)

    def _showHpBar(
        self,
        screen : pygame.Surface,
        entity : pl.Player | ch.Enemy,
    ) -> None:
        if entity.hp >= 0:
            hp_ratio = entity.hp / entity.max_hp
        else:
            hp_ratio = 0
        hp_bar = pygame.transform.scale_by(
            self._hp_bar, 
            (hp_ratio, 1)
        )
        hp_bar_rect = hp_bar.get_rect()
        if isinstance(entity, pl.Player):
            pos = (47, 82)
        else:
            pos = (304, 82)
        hp_bar_rect.midleft = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(hp_bar, hp_bar_rect)

    def _setBattle(
        self,
        screen : pygame.Surface,
        player : pl.Player,
        enemy : ch.Enemy,
    ) -> None:
        screen.blit(self._battle_bg, self._battle_bg_rect)

        player.setPos(
            screen,
            (128*self._scale_fact[0], 224*self._scale_fact[1]),
            "right",
        )
        enemy.setPos(
            screen,
            (384*self._scale_fact[0], 224*self._scale_fact[1]),
            "left",
        )

        self._sections : list[dict[str, tbx.Text | list[wp.PlayerWeapon | wp.PlayerSpell] | function]] = [
            {
                "text" : tbx.Text("ARMI", align="center"),
                "attacks" : player.weapons,
                "func" : self._blitWeapons,
            },
            {
                "text" : tbx.Text("INCANTESIMI", align="center"),
                "attacks" : player.spells,
                "func" : self._blitSpells,
            },
        ]

    def _getEnemyAttack(
        self,
        player : pl.Player,
        enemy : ch.Enemy,
    ) -> tuple[wp.Weapon, int, bool]:
        best_attack = wp.NULL_ATTACK
        best_damage = 0
        player_is_weak = False
        level_factor = 1 + (0.25 * ((enemy.level - player.level) // 5))
        level_factor = max(0.25, min(2, level_factor))
        for weapon in enemy.weapons:
            if weapon.damage >= player.hp:
                best_attack = weapon
                break
            potential_damage = (
                weapon.damage 
                * (1 + (weapon.crit /100)) 
                * level_factor
            )
            if potential_damage > best_damage:
                best_attack = weapon
                best_damage = potential_damage

        for spell in enemy.spells:
            if enemy.mana >= spell.mana:
                is_weak = spell.effect in player.weakness
                spell_damage = (
                    spell.damage
                    * (1.5 if is_weak else 1)
                    * level_factor
                )
                if (spell_damage >= player.hp
                    or ((spell.type == "cure")
                        and enemy.hp <= (enemy.max_hp * 0.2))):
                    best_attack = spell
                    player_is_weak = is_weak
                    break
                if spell_damage > best_damage:
                    best_attack = spell
                    best_damage = spell_damage
                    player_is_weak = is_weak
        
        if best_attack.type == "cure":
                enemy.cure()
                damage = 0
        else:
            damage = round(
                best_attack.attack()
                * level_factor
                * (1.5 if player_is_weak else 1)
            )

        if isinstance(best_attack, wp.Spell):
            enemy.mana -= best_attack.mana
            
        return (best_attack, damage, player_is_weak)

    def _blitSection(
        self,
        screen : pygame.Surface,
        player : pl.Player,
        mouse_pos : tuple[int,int],
        mouse_click : bool,
    ) -> None:
        for i, section in enumerate(self._sections):
            if section is self._current_section:
                section["text"].changeColor("blue")
            else:
                section["text"].changeColor("white")
            section["text"].show(screen, (74, 390+(33*i)))
            if (section["text"].rect.collidepoint(mouse_pos)
                and mouse_click):
                self._current_section = section
        self._current_section["func"](screen, player)
        

    def _playBattle(
        self, 
        screen : pygame.Surface,
        player : pl.Player, 
        enemy : ch.Enemy, 
        clock : pygame.Clock, 
        max_fps : int,
    ) -> None:
        self._setBattle(screen, player, enemy)

        frame = 0
        victory = False
        self.gameover = False
        player_attacking = False
        enemy_attacking = False

        self._current_section = self._sections[0]

        message = ""

        while (not self.quit) and (not victory) and (not self.gameover):

            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit = True

            screen.blit(self._battle_bg, self._battle_bg_rect)
            self._blitStatus(screen, player, enemy, message)

            self._blitSection(screen, player, mouse_pos, mouse_buttons[0])

            # ottenere l'attacco del giocatore
            if ((not player_attacking)
                and (not enemy_attacking) 
                and (not player.is_dead) 
                and (not enemy.is_dead)):
                for attack in self._current_section["attacks"]:
                    if (attack.box.rect.collidepoint(mouse_pos)
                        and mouse_buttons[0]):
                        if (isinstance(attack, wp.Spell)
                            and player.mana < attack.mana):
                            message = "Non hai abbastanza mana"
                        else:
                            message = ""
                            player_damage, enemy_is_weak = (
                                player.getAttackDamage(attack, enemy)
                            )
                            player_attack = attack

                            enemy_attack, enemy_damage, player_is_weak = (
                                self._getEnemyAttack(player, enemy)
                            )

                            enemy_inflicted = False
                            player_inflicted = False
                            player_attacking = True
                            break

            if player_attacking:
                player_attacking = player_attack.attackAnim(screen, "right")
                if not enemy_inflicted:
                    enemy.getDamage(player_damage)
                    SFX["attack"].play()
                    enemy_inflicted = True
                message = (
                    MESSAGES["vittoria"] if enemy.is_dead else (
                        MESSAGES["rigenerato"] if player_attack.type == "cure" else (
                            MESSAGES["critico"] if player_attack.critical else (
                                MESSAGES["super"] if enemy_is_weak else ""
                            )
                        )
                    )
                )    
                enemy_attacking = not player_attacking

            if ((not enemy.is_dead) 
                and enemy_attacking 
                and (not pygame.mixer.get_busy())):
                enemy_attacking = enemy_attack.attackAnim(screen, "left")
                if not player_inflicted:
                    player.getDamage(enemy_damage)
                    SFX["attack"].play()
                    player_inflicted = True
                message = (
                    f"{enemy.name} ha usato {enemy_attack.name}, " 
                    + (MESSAGES["morto"] if player.is_dead else (
                        MESSAGES["nemico_rigenerato"] if enemy_attack.type == "cure" else (
                            MESSAGES["nemico_critico"] if enemy_attack.critical else (
                                MESSAGES["nemic_super"] if player_is_weak else ""
                            )
                        )
                    )
                ))

            if keys[pygame.K_RETURN]:
                if enemy.is_dead:
                    player.levelUp()
                    victory = True
                elif player.is_dead:
                    self.gameover = True

            player.idle(screen, frame, "right")
            enemy.idle(screen, frame, "left")

            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)

    def _blitWeapons(
        self,
        screen : pygame.Surface,
        player : pl.Player,
    ) -> None:
        for i, weapon in enumerate(player.weapons):
            weapon.showBox(screen, (220+((i%2)*180), 390+((i//2)*67)))

    def _blitSpells(
        self,
        screen : pygame.Surface,
        player : pl.Player,
    ) -> None:
        for i, spell in enumerate(player.spells):
            spell .showBox(screen, (220+((i%2)*180), 390+((i//2)*67)))
    
    def _blitStatus(
        self,
        screen : pygame.Surface,
        player : pl.Player,
        enemy : ch.Enemy,
        message : str,
    ) -> None:
        player_hp = tbx.Text(
            f"{player.hp}/{player.max_hp}",
            align = "center",
        )
        player_mana = tbx.Text(
            f"Man: {player.mana}/{player.max_mana}",
            align = "center"
        )
        player_level = tbx.Text(
            f"lv. {player.level}",
            align =  "center"
        )
        
        enemy_hp = tbx.Text(
            f"{enemy.hp}/{enemy.max_hp}",
            align = "center",
        )

        message_text = tbx.Text(
            f"{message}",
            align = "left"
        )

        message_text.show(screen, (256, 339))

        player.name_text.show(screen, (128, 41))
        player_hp.show(screen, (207, 82))
        player_level.show(screen, (47, 41))
        self._showHpBar(screen, player)
        player_mana.show(screen, (74, 456))
        
        enemy.name_text.show(screen, (384, 41))
        enemy_hp.show(screen, (465, 82))
        enemy.level_text.show(screen, (304, 41))
        self._showHpBar(screen, enemy)

    def playLevel(
        self, 
        screen : pygame.Surface,
        player : pl.Player, 
        clock : pygame.Clock, 
        max_fps : int,
    ) -> None:
        self._setLevel(screen, player)
        frame = 0
        self.quit = False
        self._in_inventory = False
        self._next_page = False
        last_page = False
        
        self._playMusic()

        player.saveState()

        while ((not self.quit) 
               and (not self.passed) 
        ):
            if player.is_dead:
                self._setLevel(screen, player)
                player.reset()
            
            keys = pygame.key.get_pressed()
            self._checkEvents()

            self._blitLevel(screen, frame)
            
            player.getNextPos(keys)
            
            self._can_move = self._canMove(player)

            if self._can_move:
                player.move(screen, frame)
            else:
                player.idle(screen, frame)

            for character in self._characters:
                if (character["type"].has_collision
                    and player.rect.colliderect(character["type"].collision_rect)
                ):
                    if character["type"].is_hostile:
                        player_last_pos = player.rect.center
                        enemy_pos = character["type"].rect.center
                        self._playBattle(
                            screen, player, character["type"], clock, max_fps
                        )
                        player.setPos(screen, player_last_pos)
                        character["type"].setPos(
                            screen, enemy_pos, character["rot"]
                        )
                    elif character["type"].has_dialogue:
                        character["type"].blitDialogue(screen, character["pos"])
                        if self._next_page != last_page:
                            character["type"].page += 1
                            last_page = self._next_page

            for object in self._objects:
                if (object["type"].has_collision 
                    and player.rect.colliderect(object["type"].rect)
                ):
                    if object["type"].has_item:
                        player.addItem(object["type"].item)
                    object["type"].collision(screen)
                    SFX["chest"].play()
            
            if self._has_fog:
                self._setFogPos(screen, player.rect.center)

            if self._in_inventory:
                player.inventory.show(screen)

            if self._checkExit(player):
                self.passed = True

            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)
    
class ClassSelection(PrimitiveLevel):
    def __init__(
        self,
        name : str,
        start_pos : tuple[int, int],
        music : str | None = None,
        scale_fact : int | float = 1,
        characters : list = [],
    ) -> None:
        PrimitiveLevel.__init__(
            self, name, start_pos, music, scale_fact, characters
        )

    def playLevel(
        self, 
        screen : pygame.Surface,
        player : pl.Player, 
        clock : pygame.Clock, 
        max_fps : int,
    ) -> None:
        self._setLevel(screen, player)
        frame = 0
        self.quit = False
        self._in_inventory = False

        self._playMusic()
        
        player.saveState()

        while ((not self.quit) 
               and (not self.passed) 
        ):
            
            keys = pygame.key.get_pressed()
        
            self._checkEvents()

            self._blitLevel(screen, frame)
            
            player.getNextPos(keys)
            
            self._can_move = self._canMove(player)

            if self._can_move:
                player.move(screen, frame)
            else:
                player.idle(screen, frame,)

            self.passed = self._chooseClass(player, keys)

            if self._in_inventory:
                player.inventory.show(screen)

            pygame.display.flip()
            frame += 1
            clock.tick(max_fps)

    def _chooseClass(
        self,  
        player : pl.Player, 
        keys : list[int],
    ) -> bool:
        for character in self._characters:
            if (player.rect.colliderect(character["type"].rect)  
                and keys[pygame.K_e]
            ):
                player.setPlayerClass(character["type"])
                return True
        return False
    
class StartMenu:
    def __init__(
        self,
        scale_fact : int | float = 1,
    ) -> None:
        self._path = f"{ASSETS_PATH}/start_menu"
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._bg = pygame.image.load(f"{self._path}/bg.png")
        self._bg = pygame.transform.scale_by(self._bg, self._scale_fact)
        self._bg_rect = self._bg.get_rect()
        self._options = [
            {
                "text" : tbx.Text("Nuovo gioco", font_size=14),
                "levels" : default_levels_data,
                "has_collision" : True,
            },
            {
                "text" : tbx.Text(
                    "Carica Salvataggio", 
                    font_size=14,
                    font_color=("grey" if not LOADED else "white")
                ),
                "levels" : loaded_levels_data,
                "has_collision" : (True if LOADED else False),
            }
        ]
        self.quit = False

    def getLevels(
        self,
        screen : pygame.Surface,
    ) -> None:
        running = True
        while running:
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit = True
                    return None

            screen.blit(self._bg, self._bg_rect)

            for i, option in enumerate(self._options):
                option["text"].show(screen, (256, 355+(i*54)))
                if option["has_collision"]:
                    if option["text"].rect.collidepoint(mouse_pos):
                        option["text"].changeColor("blue")
                        if mouse_buttons[0]:
                            self._levels = option["levels"]
                            SFX["start"].play()
                            running = False
                            break
                    else:
                        option["text"].changeColor("white")
            
            pygame.display.flip()

        return self._levels


CLASSES = {
    "Level" : Level,
    "ClassSelection" : ClassSelection,
    "StartMenu" : StartMenu,
}