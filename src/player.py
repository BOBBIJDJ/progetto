import copy
from math import sqrt
from typing import Literal

import pygame

from config import X_RATIO, Y_RATIO, MAX_RATIO, ASSETS_PATH
import characters as ch
import objects as obj
import textboxes as tbx
import weapons as wp

Rotation = Literal["left", "right"]

class Player:
	
	def __init__(
		self, 
		max_frames : int,
		frame_mult : int = 4,
		walk_speed : int | float = 2,
		max_hp : int = 10,
		max_mana : int = 0,
		scale_fact : int | float = 1,
	) -> None:
		self.name = "???"
		self.level = 0
		self._path = f"{ASSETS_PATH}/sprites/default"
		self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
		self._walk_speed = walk_speed*MAX_RATIO
		self._max_frames = max_frames
		self.weapons = list()
		self.spells = list()
		self._frame_mult = frame_mult
		self._setSprites()
		self.rect = self._static["last"].get_rect()
		self.is_dead = False
		self.max_hp = self.hp = max_hp
		self.max_mana = self.mana = max_mana
		self.inventory = Inventory(self)
		
	def showStatic(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
		rot : Literal["left", "right", "last"] = "last",
	) -> None:
		tmp_rect = copy.deepcopy(self.rect)
		tmp_rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static[rot], tmp_rect)

	def _setMask(self) -> None:
		self._left_mask = pygame.mask.from_surface(self._static_left)
		self._right_mask = pygame.mask.from_surface(self._static_right)

	def _setSprites(self) -> None:
		self._static_right = pygame.image.load(
			f"{self._path}/static/static_r.png"
		)
		self._static_right = pygame.transform.scale_by(
			self._static_right, self._scale_fact
		)
		self._static_left = pygame.image.load(
			f"{self._path}/static/static_l.png"
		)
		self._static_left = pygame.transform.scale_by(
			self._static_left, self._scale_fact
		)
		self._setMask()
		# WALK
		self._right_walk = []
		self._left_walk = []
		# IDLE
		self._right_idle = []
		self._left_idle = []
		for i in range(self._max_frames):
			for j in range(self._frame_mult):
				k = (self._frame_mult * i) + j
				# WALK:
				# right
				self._right_walk.append(
					pygame.image.load(
						f"{self._path}/right_walk/{i%self._max_frames}.png"
					)
				)
				self._right_walk[k] = pygame.transform.scale_by(
					self._right_walk[k], self._scale_fact
				)
				# left
				self._left_walk.append(
					pygame.image.load(
						f"{self._path}/left_walk/{i%self._max_frames}.png"
					)
				)
				self._left_walk[k] = pygame.transform.scale_by(
					self._left_walk[k], self._scale_fact
				)
				# IDLE:
				# right
				self._right_idle.append(
					pygame.image.load(
						f"{self._path}/right_idle/{i%self._max_frames}.png"
					)
				)
				self._right_idle[k] = pygame.transform.scale_by(
					self._right_idle[k], self._scale_fact
				)
				# left
				self._left_idle.append(
					pygame.image.load(
						f"{self._path}/left_idle/{i%self._max_frames}.png"
					)
				)
				self._left_idle[k] = pygame.transform.scale_by(
					self._left_idle[k], self._scale_fact
				)
				
		self._static = {
			"left" : self._static_left,
			"right" : self._static_right,
		}
		self._idle = {
			"left" : self._left_idle,
			"right" : self._right_idle,
		}
		self._walk = {
			"left" : self._left_walk,
			"right" : self._right_walk,
		}
		self.mask = {
			"left" : self._left_mask,
			"right" : self._right_mask,
		}
		self._setRotation("right")

	def setPlayerClass(
		self, 
		player_class : ch.Subplayer,
	) -> None:
		self.name = player_class.name
		self.type = player_class.type
		self.level = player_class.level
		self._path = player_class.path
		self._scale_fact = player_class.scale_fact
		self._max_frames = player_class.max_frames
		self._frame_mult = player_class.frame_mult
		self.weapons = player_class.weapons
		self.spells = player_class.spells
		self.weakness = player_class.weakness
		self.hp = self.max_hp = player_class.max_hp
		self.mana = self.max_mana = player_class.max_mana
		self._setSprites()
		tmp_rect_pos = self.rect.center
		self.rect = player_class.rect
		self.rect.center = tmp_rect_pos
		self.name_text = tbx.Text(
			    f"{self.name}",
		    align = "center"
		)
		self.level_text = tbx.Text(
			    f"lv. {self.level}",
		    align = "center"
		)

	def addWeapon(
		self, 
		key : str, 
		weapon : wp.Weapon,
	) -> None:
		self.weapons[key] = weapon
	
	def addSpell(
		self, 
		key : str, 
		spell : wp.Spell,
	) -> None:
		self.spells[key] = spell

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
		rot : Literal["left", "right", "last"] = "last",
	) -> None:
		self.rect.center = pos
		screen.blit(self._static[rot], self.rect)

	def _setRotation(
		self, 
		rot : Literal["left", "right"],
	) -> None:
		for anim in [self._static, self._idle, self._walk, self.mask]:
			anim["last"] = anim[rot]

	def idle(
		self, 
		screen : pygame.Surface,
		frame : int,
		rot : Literal["left", "right", "last"] = "last",
	) -> None:
		anim_frame = frame % (self._max_frames * self._frame_mult)
		screen.blit(self._idle[rot][anim_frame], self.rect)

	def _normalize_movement(self) -> None:
		norm = sqrt(sum((comp**2) for comp in self._movement))
		if norm != 0:
			self._movement = [
				(comp/norm)*self._walk_speed for comp in self._movement
			]

	def getNextPos(
		self, 
		keys : list[int],
	) -> None:
		self._movement = [0,0]
		if keys[pygame.K_a]:
			self._setRotation("left")
			self._movement[0] += -1
		if keys[pygame.K_d]:
			self._setRotation("right")
			self._movement[0] += 1
		if keys[pygame.K_s]:
			self._movement[1] += 1
		if keys[pygame.K_w]:
			self._movement[1] += -1
		self._normalize_movement()
		self.next_pos = (
			self.rect.topleft[0]+self._movement[0], 
			self.rect.topleft[1]+self._movement[1]
		)

	def move(
		self, 
		screen : pygame.Surface,
		frame : int,
	) -> None:
		if self._movement == [0,0]:
			self.idle(screen, frame)
			return 

		anim_frame = frame % (self._max_frames * self._frame_mult)

		self.rect = self.rect.move(self._movement)
		screen.blit(self._walk["last"][anim_frame], self.rect)

	def getAttackDamage(
		self,
		attack : wp.Weapon,
		enemy : ch.Enemy,
	) -> int:
		if (isinstance(attack, wp.Spell)
			and (attack.effect in enemy.weakness)):
			enemy_is_weak = True
		else:
			enemy_is_weak = False
		if attack.type == "cure":
			self._cure()
			damage = 0
		else:
			damage = round(
			    attack.attack() 
			    * (self.level / enemy.level)
			    * (2 if enemy_is_weak else 1)
			)
		return damage
	
	def _cure(self) -> None:
		new_hp = self.hp + (self.max_hp * 0.2) 
		self.hp = min(new_hp, self.max_hp)


class Inventory:
	def __init__(self, player : Player) -> None:
		self._box = pygame.image.load(f"{ASSETS_PATH}/inventory/static.png")
		self._box = pygame.transform.scale_by(self._box, (X_RATIO, Y_RATIO))
		self._rect = self._box.get_rect()
		self._rect.center = (256*X_RATIO, 256*Y_RATIO)
		self._player = player
		self._weapons_text = tbx.Text("Armi", align = "center")
		self._spells_text = tbx.Text("Incantesimi", align = "center")
		self._update()

	def _update(self) -> None:
		self._name = tbx.Text(
			f"{self._player.name}", 
			align = "center",
		)
		self._level = tbx.Text(
			f"lv. {self._player.level}",
			align = "center",
		)
		self._hp = tbx.Text(
			f" PV: {self._player.hp}/{self._player.max_hp}", 
			align = "center",
		)
		self._mana = tbx.Text(
			f"Mana: {self._player.mana}/{self._player.max_mana}", 
			align = "center",
		)

	def show(
		self, 
		screen : pygame.Surface,
	) -> None:
		self._update()
		screen.blit(self._box, self._rect)
		self._player.showStatic(screen, (73, 113))
		for i, text in enumerate([self._name, self._level, self._hp, self._mana]):
			text.show(screen, (74, 224+(i*55)))
		self._weapons_text.show(screen, (218, 113))
		self._spells_text.show(screen, (400, 113))
		if self._player.weapons:
			for i, weapon in enumerate(self._player.weapons):
				weapon.showBox(screen, (218, 180+(69*i)))
		if self._player.spells:
			for j, spell in enumerate(self._player.spells):
				spell.showBox(screen, (400, 180+(69*j)))
