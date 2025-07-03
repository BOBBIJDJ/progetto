import copy
from math import sqrt

import pygame

from config import X_RATIO, Y_RATIO, MAX_RATIO
import characters as ch
import objects as obj
import textboxes as tbx
import weapons as wp

class Player:
	
	def __init__(
		self, 
		screen : pygame.Surface, 
		max_frames : int,
		frame_mult : int = 4,
		walk_speed : int | float = 2,
		max_hp : int = 10,
		max_mana : int = 0,
		scale_fact : int | float = 1,
	) -> None:
		self.name = "???"
		self._path = "assets/sprites/default"
		self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
		self._walk_speed = walk_speed*MAX_RATIO
		self._screen = screen
		self._max_frames = max_frames
		self.weapons = list()
		self.spells = list()
		self.items = list()
		self._frame_mult = frame_mult
		self._setSprites()
		self.rect = self._static.get_rect()
		self.is_dead = False
		self.max_hp = self.hp = max_hp
		self.max_mana = self.mana = max_mana
		self.inventory = Inventory(self)
		
	def showStatic(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		tmp_rect = copy.deepcopy(self.rect)
		tmp_rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static_right, tmp_rect)

	def restore(
		self, 
		potion : obj.Item,
	) -> None:
		if potion["type"] == "hp":
			if potion["value"] >= self.max_hp-self.hp:
				self.hp = self.max_hp
			else:
				self.hp += potion["value"]
		else:
			if potion["value"] >= self.max_mana-self.mana:
				self.mana = self.max_mana
			else:
				self.mana += potion["value"]

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
				
		self._setRotation("right")

	def setPlayerClass(
		self, 
		player_class : ch.Subplayer,
	) -> None:
		self.name = player_class.name
		self.type = player_class.type
		self._path = player_class.path
		self._scale_fact = player_class.scale_fact
		self._max_frames = player_class.max_frames
		self._frame_mult = player_class.frame_mult
		self.weapons = player_class.weapons
		self.spells = player_class.spells
		self.items = player_class.items
		self.max_hp = player_class.max_hp
		self.hp = self.max_hp
		self.max_mana = player_class.max_mana
		self.mana = self.max_mana
		self._setSprites()
		tmp_rect_pos = self.rect.center
		self.rect = player_class.rect
		self.rect.center = tmp_rect_pos

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

	def addItem(
		self,
		key : str,
		item : obj.Item,
	) -> None:
		self.items[key] = item

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		self.rect.center = pos
		screen.blit(self._static, self.rect)

	def _setRotation(
		self, 
		rot : str,
	) -> None:
		if rot == "left":
			self._current_walk = self._left_walk
			self._current_idle = self._left_idle
			self._static = self._static_left
			self.mask = self._left_mask
		else:
			self._current_walk = self._right_walk
			self._current_idle = self._right_idle
			self._static = self._static_right
			self.mask = self._right_mask

	def idle(
		self, 
		frame : int,
	) -> None:
		anim_frame = frame % (self._max_frames * self._frame_mult)
		self._screen.blit(self._current_idle[anim_frame], self.rect)

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
		frame : int,
	) -> None:
		if self._movement == [0,0]:
			self.idle(frame)
			return 

		anim_frame = frame % (self._max_frames * self._frame_mult)

		self.rect = self.rect.move(self._movement)
		self._screen.blit(self._current_walk[anim_frame], self.rect)


class Inventory:
	def __init__(self, player : Player) -> None:
		self._box = tbx.Box("inventory", (475, 197))
		self._player = player
		self._weapons_text = tbx.Text("Armi", align = "center")
		self._spells_text = tbx.Text("Incantesimi", align = "center")
		self._update()

	def _update(self) -> None:
		self._name = tbx.Text(
			f"{self._player.name}", 
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
		self._box.show(screen, (256, 256))
		self._player.showStatic(screen, (73, 113))
		self._name.show(screen, (73, 214))
		self._hp.show(screen, (73, 307))
		self._mana.show(screen, (73, 400))
		self._weapons_text.show(screen, (218, 113))
		self._spells_text.show(screen, (400, 113))
		if self._player.weapons:
			for weapon, i in zip(
				self._player.weapons, 
				range(len(self._player.weapons)),
			):
				weapon.showBox(screen, (218, 203+(69*i)))
		if self._player.spells:
			for spell, j in zip(
				self._player.spells, 
				range(len(self._player.spells)),
			):
				spell.showBox(screen, (400, 203+(69*j)))
