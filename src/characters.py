import copy
from typing import Literal

import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH
import weapons as wp
import objects as obj
import textboxes as tbx

class Character:
	def __init__(
		self, 
		name : str, 
		type : str,
		max_frames : int,
		level : int = 1,
		frame_mult : int = 4,
		scale_fact : int | float = 1,
		has_collision : bool = True,
		is_hostile : bool = False,
		dialogue : str | None = None
	) -> None:
		self.name = name
		self.type = type
		self.level = level
		self.path = f"{ASSETS_PATH}/sprites/{self.type}"
		self.scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
		self.max_frames = max_frames
		self.frame_mult = frame_mult
		self.has_collision = has_collision
		self.is_hostile = is_hostile
		self.collision_type = ""
		self._setSprites()
		self.rect = self._static_right.get_rect()
		self.name_text = tbx.Text(
		    f"{self.name}",
		    align = "center",
		)
		self.level_text = tbx.Text(
		    f"lv. {self.level}",
		    align = "center",
		)
		if dialogue is not None:
			self.has_dialogue = True
			self._getDialogue(dialogue)
		else:
			self.has_dialogue = False

	def _getDialogue(
		self,
		text : str,
	) -> None:
		dialogues = []
		with open(f"{ASSETS_PATH}/dialogue/{text}.txt") as file:
			words = file.read().split()
		phrase = ''
		for i, word in enumerate(words):
			if i%20 != 19:
				phrase += word + ' '
			else:
				dialogues.append(phrase)
				phrase = ''
		if phrase != '':
			dialogues.append(phrase)
		self._dialogue = [
			tbx.TextBox(
				"dialogue",
				dialogue,
			)  for dialogue in dialogues
		]
		self.page = 0
		self._max_page = len(self._dialogue)

	def blitDialogue(
		self,
		screen : pygame.Surface,
		pos : tuple[int, int],
		) -> None:
		if pos[1] >= 256: 
			dialogue_pos = (256, 128)
		else:
			dialogue_pos = (256, 384)
		if self.page < self._max_page:
			self._dialogue[self.page].show(screen, dialogue_pos)
		else:
			self.page = 0
		

	def _setSprites(self) -> None:
		self._static_right = pygame.image.load(
			f"{self.path}/static/static_r.png"
		)
		self._static_right = pygame.transform.scale_by(
			self._static_right, self.scale_fact
		)
		self._static_left = pygame.image.load(
			f"{self.path}/static/static_l.png"
		)
		self._static_left = pygame.transform.scale_by(
			self._static_left, self.scale_fact
		)
		self._right_idle = []
		self._left_idle = []
		for i in range(self.max_frames):
			self._right_idle.append(
				pygame.image.load(
					f"{self.path}/right_idle/{i}.png"
				)
			)
			self._right_idle[i] = pygame.transform.scale_by(
				self._right_idle[i], self.scale_fact
			)
			self._left_idle.append(
				pygame.image.load(
					f"{self.path}/left_idle/{i}.png"
				)
			)
			self._left_idle[i] = pygame.transform.scale_by(
				self._left_idle[i], self.scale_fact
			)
		self._current_anim = self._right_idle
		self._current_rot = self._static_right

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int], 
		rot : Literal["left", "right"],
	) -> None:
		if rot == "right":
			self._current_rot = self._static_right
		else:
			self._current_rot = self._static_left
		self.rect.center = pos
		screen.blit(self._current_rot, self.rect)
		
	def idle(
		self, 
		screen : pygame.Surface, 
		frame : int,
		rot : Literal["left", "right"], 
	) -> None:
		if rot == "right":
			self._current_anim = self._right_idle
		else:
			self._current_anim = self._left_idle
		
		anim_frame = (frame // self.frame_mult)  % self.max_frames
		
		screen.blit(self._current_anim[anim_frame], self.rect)
	
class NPC(Character):
	def __init__(
		self, 
		name : str, 
		type : str, 
		max_frames : int,
		frame_mult : int = 4,
	) -> None:
		Character.__init__(self, name, type, max_frames, frame_mult)
		self.collision_type = "nobattle"

	# def giveItem(self, player, item):
	# 	player.items.append()
		
class Enemy(Character):
	def __init__(
		self, 
		name : str, 
		type : str,
		max_hp : int,
		max_mana : int,
		level : int,
		max_frames : int,
		frame_mult : int = 4,
		scale_fact : int | float = 1,
		has_collision : bool = True,
		is_hostile : bool = True,
		dialogue : str | None = None, 
		weapons : list = [],
		spells : list = [],
		weakness : list[str] = [],
	) -> None:
		Character.__init__(
			self, name, type, max_frames, level, frame_mult, 
			scale_fact, has_collision, is_hostile, dialogue
		)
		self.max_hp = self.hp = max_hp
		self.max_mana = self.mana = max_mana
		self.weakness = weakness
		self.collision_type = "battle"
		self.weapons : list[wp.Weapon] = [
			wp.CLASSES[weapon["class"]](**weapon["args"]) for weapon in weapons
		]
		self.spells : list[wp.Spell] = [
			wp.CLASSES[spell["class"]](**spell["args"]) for spell in spells
		]
		self.is_dead = False
		# self.setAttackAnimations()

	def getDamage(
		self,
		damage : int,
	) -> None:
		if self.hp > damage:
			self.hp -= damage
		else:
			self.hp = 0
			self.is_dead = True
			self.is_hostile = False

	def cure(self) -> None:
		new_hp = round(self.hp + (self.max_hp * 0.2)) 
		self.hp = min(new_hp, self.max_hp)

	# def setAttackAnimations(self):
	# 	self.attack_anim = []
	# 	for i in range(self.max_frames):
	# 		self.attack_anim.append(pygame.image.load(f"{self.path}/attack/{i}.png"))
	# 		self.attack_anim[i] = pygame.transform.scale_by(self.attack_anim[i], self.scale_fact)
			
class Subplayer(Character):
	def __init__(
		self, 
		name : str, 
		type : str,
		max_hp : int,
		max_mana : int,
		weakness : list[str],
		max_frames : int,
		level : int = 1,
		frame_mult : int = 4,
		scale_fact : int | float = 1,
		has_collision : bool = True,
		is_hostile : bool = False,
		weapons : list = [],
		spells : list = [],
	) -> None:
		Character.__init__(self, name, type, max_frames, level, frame_mult, scale_fact, has_collision, is_hostile)
		self.max_hp = max_hp
		self.max_mana = max_mana
		self.weakness = weakness
		self.weapons = [
			wp.CLASSES[weapon["class"]](**weapon["args"]) for weapon in weapons
		]
		self.spells = [
			wp.CLASSES[spell["class"]](**spell["args"]) for spell in spells
		]

CLASSES = {
	"Character" : Character,
	"Subplayer" : Subplayer,
	"Enemy" : Enemy,
}