from random import randint
from typing import Literal

import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH
import textboxes as tbx

class Weapon:
	def __init__(
		self, 
		name : str, 
		type : str, 
		damage : int, 
		crit : int,
		max_frames : int,
		frame_mult : int = 8,
		scale_fact : int | float = 1,
	) -> None:
		self.name = name
		self.type = type
		self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
		if isinstance(self, Spell):
			self._path = f"{ASSETS_PATH}/spells"
		else:
			self._path = f"{ASSETS_PATH}/weapons/{self.type}"
		self.damage = damage
		self.crit = crit
		self._max_frames = max_frames
		self._frame_mult = frame_mult
		self._setSprites()
		self._current_frame = 0
	
	def _setSprites(self) -> None:
		if isinstance(self, Spell):
			self._static = pygame.image.load(f"{self._path}/{self.type}/static/static.png")
		else:
			self._static = pygame.image.load(f"{self._path}/static/static.png")
		self._static = pygame.transform.scale_by(self._static, self._scale_fact)
		self._rect = self._static.get_rect()
		self._left_attack = []
		self._right_attack = []
		for i in range(self._max_frames):
			self._left_attack.append(
				pygame.image.load(
					f"{self._path}/left_attack/{i}.png"
				)
			)
			self._left_attack[i] = pygame.transform.scale_by(
				self._left_attack[i], self._scale_fact
			)
			self._right_attack.append(
				pygame.image.load(
					f"{self._path}/right_attack/{i}.png"
				)
			)
			self._right_attack[i] = pygame.transform.scale_by(
				self._right_attack[i], self._scale_fact
			)

	def attackAnim(
		self, 
		screen : pygame.Surface, 
		rot : Literal["left", "right"], 
	) -> None:
		if self._current_frame < (self._frame_mult*self._max_frames):
			if rot == "left":
				self.current_anim = self._left_attack
				self._rect.center = (357*X_RATIO, 224*Y_RATIO)
			else:
				self.current_anim = self._right_attack
				self._rect.center = (154*X_RATIO, 224*Y_RATIO)
			screen.blit(self.current_anim[self._current_frame // self._frame_mult], self._rect)
			self._current_frame += 1
			return True
		else:
			self._current_frame = 0
			return False

	def attack(self) -> int:
		crit_prob = randint(1,100)
		if crit_prob <= self.crit:
			damage = self.damage * 2
			self.critical = True
		else:
			damage = self.damage
			self.critical = False
		return damage

	# def setPos(
	# 	self, 
	# 	screen : pygame.Surface, 
	# 	pos : tuple[int, int],
	# ) -> None:
	# 	self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
	# 	screen.blit(self._static, self._rect)

class PlayerWeapon(Weapon):
	def __init__(
		self, 
		name : str, 
		type : str, 
		damage : int, 
		crit : int,
		max_frames : int,
		frame_mult : int = 8,
		scale_fact : int | float = 1,
	) -> None:
		Weapon.__init__(self, name, type, damage, crit, max_frames, frame_mult, scale_fact)
		self._setBox()

	def _setBox(self) -> None:
		self.box = tbx.Box((128, 48))
		self.name_text = tbx.Text(
			f"{self.name}", align="center", font_size=9
		)
		self._dmg_text = tbx.Text(
			f"Dmg: {self.damage}", align="center", font_size=9
		)
		self.crit_text = tbx.Text(
			f"Crt: {self.crit}%", align="center", font_size=9
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		self.box.show(screen, pos)
		self._showStatic(screen, (pos[0] - 48, pos[1]))
		self.name_text.show(screen, (pos[0]+8, pos[1] - 12))
		self._dmg_text.show(screen, (pos[0]-16, pos[1]+8))
		self.crit_text.show(screen, (pos[0]+32, pos[1]+8))
		
	def _showStatic(
		self,
		screen : pygame.Surface,
		pos : tuple[int, int],
	) -> None:
		self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static, self._rect)

	def getData(self) -> dict:
		data = {
			"name" : self.name,
			"type" : self.type,
			"damage" : self.damage,
			"crit" : self.crit,
			"max_frames" : self._max_frames,
		}
		return data

class Spell(Weapon):
	def __init__(
		self, 
		name : str,
		type : str,
		damage : int, 
		effect : str, 
		mana : int,
		max_frames : int = 4, 
	) -> None:
		Weapon.__init__(self, name, type, damage, 0, max_frames)
		self.effect = effect
		self.mana = mana

class PlayerSpell(Spell):
	def __init__(
		self,
		name : str,
		type : str,
		damage : int, 
		effect : str, 
		mana : int,
		max_frames : int = 4,
	) -> None:
		Spell.__init__(self, name, type, damage, effect, mana, max_frames)
		self._setBox()

	def _setBox(self) -> None:
		self.box = tbx.Box((128, 48))
		self.name_text = tbx.Text(
			f"{self.name}", align="center", font_size=9
		)
		self._dmg_text = tbx.Text(
			f"Dmg: {self.damage}", align="center", font_size=9
		)
		self._mana_text = tbx.Text(
			f"Man: {self.mana}", align="center", font_size=9
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
		battle_size : bool = False,
	) -> None:
		self.box.show(screen, pos)
		self._showStatic(screen, (pos[0] - 48, pos[1]))
		self.name_text.show(screen, (pos[0]+8, pos[1] - 12))
		self._dmg_text.show(screen, (pos[0]-16, pos[1]+8))
		self._mana_text.show(screen, (pos[0]+32, pos[1]+8))

	def _showStatic(
		self,
		screen : pygame.Surface,
		pos : tuple[int, int],
	) -> None:
		self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static, self._rect)

	def getData(self) -> dict:
		data = {
			"name" : self.name,
			"type" : self.type,
			"damage" : self.damage,
			"effect" : self.effect,
			"mana" : self.mana,
		}
		return data

CLASSES = {
	"Weapon" : Weapon,
	"Spell" : Spell,
	"PlayerWeapon" : PlayerWeapon,
	"PlayerSpell" : PlayerSpell,
}

NULL_ATTACK = Weapon("NULL", "null", 0, 0, 0)