import pygame
import copy
import characters as ch
import objects as obj
import textboxes as tbx
import weapons as wp
from math import sqrt
from config import MAX_RATIO, X_RATIO, Y_RATIO
	
class Player:
	
	def __init__(
		self, 
		screen : pygame.Surface, 
		max_frames : int,
	):
		self.name = "???"
		self.path = "assets/sprites/default"
		self.scale_factor = (1*X_RATIO, 1*Y_RATIO)
		self.walk_speed = 2*MAX_RATIO
		self.screen = screen
		self.max_frames = max_frames
		self.weapons = list()
		self.spells = list()
		self.items = list()
		self.frame_mult = 4
		self._setSprites()
		self.rect = self.static_right.get_rect()
		self.is_dead = False
		self.max_hp = self.hp = 10
		self.max_mana = self.mana = 0 
		self.inventory = Inventory(self)
		
	def showStatic(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	):
		tmp_rect = copy.deepcopy(self.rect)
		tmp_rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self.static_right, tmp_rect)

	def restore(
		self, 
		potion : obj.Item,
	):
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

	def _setMask(self):
		self.left_mask = pygame.mask.from_surface(self.static_left)
		self.right_mask = pygame.mask.from_surface(self.static_right)

	def _setSprites(self):
		self.static_right = pygame.image.load(
			f"{self.path}/static/static_r.png"
		)
		self.static_right = pygame.transform.scale_by(
			self.static_right, self.scale_factor
		)
		self.static_left = pygame.image.load(
			f"{self.path}/static/static_l.png"
		)
		self.static_left = pygame.transform.scale_by(
			self.static_left, self.scale_factor
		)
		self._setMask()
		# WALK
		self.right_walk = []
		self.left_walk = []
		# IDLE
		self.right_idle = []
		self.left_idle = []
		for i in range(self.max_frames):
			for j in range(self.frame_mult):
				k = (self.frame_mult * i) + j
				# WALK:
				# right
				self.right_walk.append(
					pygame.image.load(
						f"{self.path}/right_walk/{i%self.max_frames}.png"
					)
				)
				self.right_walk[k] = pygame.transform.scale_by(
					self.right_walk[k], self.scale_factor
				)
				# left
				self.left_walk.append(
					pygame.image.load(
						f"{self.path}/left_walk/{i%self.max_frames}.png"
					)
				)
				self.left_walk[k] = pygame.transform.scale_by(
					self.left_walk[k], self.scale_factor
				)
				# IDLE:
				# right
				self.right_idle.append(
					pygame.image.load(
						f"{self.path}/right_idle/{i%self.max_frames}.png"
					)
				)
				self.right_idle[k] = pygame.transform.scale_by(
					self.right_idle[k], self.scale_factor
				)
				# left
				self.left_idle.append(
					pygame.image.load(
						f"{self.path}/left_idle/{i%self.max_frames}.png"
					)
				)
				self.left_idle[k] = pygame.transform.scale_by(
					self.left_idle[k], self.scale_factor
				)
				
		self._setRotation("right")

	def setPlayerClass(
		self, 
		player_class : ch.Subplayer,
	):
		self.name = player_class.name
		self.type = player_class.type
		self.path = player_class.path
		self.weapons = copy.deepcopy(player_class.weapons)
		self.spells = copy.deepcopy(player_class.spells)
		self.items = copy.deepcopy(player_class.items)
		self.max_hp = player_class.max_hp
		self.hp = self.max_hp
		self.max_mana = player_class.max_mana
		self.mana = self.max_mana
		self._setSprites()
		tmp_rect_pos = self.rect.center
		self.rect = copy.deepcopy(player_class.rect)
		self.rect.center = tmp_rect_pos

	def addWeapon(
		self, 
		key : str, 
		weapon : wp.Weapon,
	):
		self.weapons[key] = weapon
	
	def addSpell(
		self, 
		key : str, 
		spell : wp.Spell,
	):
		self.spells[key] = spell

	def addItem(
		self,
		key : str,
		item : obj.Item,
	):
		self.items[key] = item

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	):
		self.rect.center = pos
		screen.blit(self.static, self.rect)

	def _setRotation(
		self, 
		rot : str,
	):
		if rot == "left":
			self.current_walk = self.left_walk
			self.current_idle = self.left_idle
			self.static = self.static_left
			self.mask = self.left_mask
		else:
			self.current_walk = self.right_walk
			self.current_idle = self.right_idle
			self.static = self.static_right
			self.mask = self.right_mask

	def idle(
		self, 
		frame : int,
	):
		anim_frame = frame % (self.max_frames * self.frame_mult)
		self.screen.blit(self.current_idle[anim_frame], self.rect)

	def _normalize_movement(self):
		norm = sqrt(sum((comp**2) for comp in self.movement))
		if norm != 0:
			self.movement = [
				(comp/norm)*self.walk_speed for comp in self.movement
			]
	def getNextPos(
		self, 
		keys : list[int],
	):
		self.movement = [0,0]
		if keys[pygame.K_a]:
			self._setRotation("left")
			self.movement[0] += -1
		if keys[pygame.K_d]:
			self._setRotation("right")
			self.movement[0] += 1
		if keys[pygame.K_s]:
			self.movement[1] += 1
		if keys[pygame.K_w]:
			self.movement[1] += -1
		self._normalize_movement()
		next_pos = (
			self.rect.topleft[0]+self.movement[0], 
			self.rect.topleft[1]+self.movement[1]
		)
		return next_pos

	def move(
		self, 
		frame : int,
	):
		if self.movement == [0,0]:
			self.idle(frame)
			return

		anim_frame = frame % (self.max_frames * self.frame_mult)

		self.rect = self.rect.move(self.movement)
		self.screen.blit(self.current_walk[anim_frame], self.rect)


class Inventory:
	def __init__(self, player : Player):
		self.box = tbx.Box("inventory", (475, 197))
		self.player = player
		self.weapons_text = tbx.Text("Armi", align = "center")
		self.spells_text = tbx.Text("Incantesimi", align = "center")
		self._update()

	def _update(self):
		self.name = tbx.Text(
			f"{self.player.name}", 
			align = "center",
		)
		self.hp = tbx.Text(
			f" PV: {self.player.hp}/{self.player.max_hp}", 
			align = "center",
		)
		self.mana = tbx.Text(
			f"Mana: {self.player.mana}/{self.player.max_mana}", 
			align = "center",
		)

	def show(
		self, 
		screen : pygame.Surface,
	):
		self._update()
		self.box.show(screen, (256, 256))
		self.player.showStatic(screen, (73, 113))
		self.name.show(screen, (73, 214))
		self.hp.show(screen, (73, 307))
		self.mana.show(screen, (73, 400))
		self.weapons_text.show(screen, (218, 113))
		self.spells_text.show(screen, (400, 113))
		if self.player.weapons:
			for weapon, i in zip(
				self.player.weapons, 
				range(len(self.player.weapons)),
			):
				weapon.showBox(screen, (218, 203+(69*i)))
		if self.player.spells:
			for spell, j in zip(
				self.player.spells, 
				range(len(self.player.spells)),
			):
				spell.showBox(screen, (400, 203+(69*j)))
		
