import pygame
import copy
import weapons as wp
from config import X_RATIO, Y_RATIO

class Character:
	def __init__(
		self, 
		name : str, 
		type : str,
		max_frames : int,
		frame_mult : int = 4,
	):
		self.name = name
		self.type = type
		self.path = f"assets/sprites/{self.type}"
		self.scale_fact = (1*X_RATIO, 1*Y_RATIO)
		self.max_frames = max_frames
		self.collision_type = ""
		self.frame_mult = frame_mult
		self.setSprites()
		self.rect = self.static_right.get_rect()

	def setSprites(self):
		self.static_right = pygame.image.load(
			f"{self.path}/static/static_r.png"
		)
		self.static_right = pygame.transform.scale_by(
			self.static_right, self.scale_fact
		)
		self.static_left = pygame.image.load(
			f"{self.path}/static/static_l.png"
		)
		self.static_left = pygame.transform.scale_by(
			self.static_left, self.scale_fact
		)
		self.right_idle = []
		self.left_idle = []
		for i in range(self.max_frames):
			for j in range(self.frame_mult):
				k = (self.frame_mult * i) + j
				self.right_idle.append(
					pygame.image.load(
						f"{self.path}/right_idle/{i%self.max_frames}.png"
					)
				)
				self.right_idle[k] = pygame.transform.scale_by(
					self.right_idle[k], self.scale_fact
				)
				self.left_idle.append(
					pygame.image.load(
						f"{self.path}/left_idle/{i%self.max_frames}.png"
					)
				)
				self.left_idle[k] = pygame.transform.scale_by(
					self.left_idle[k], self.scale_fact
				)
		self.current_anim = self.right_idle
		self.current_rot = self.static_right

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int], 
		rot : str,
	):
		if rot == "right":
			self.current_rot = self.static_right
		else:
			self.current_rot = self.static_left
		self.rect.center = pos
		screen.blit(self.current_rot, self.rect)
		
	def idle(
		self, 
		screen : pygame.Surface, 
		rot : str, 
		frame : int,
	):
		if rot == "right":
			self.current_anim = self.right_idle
		else:
			self.current_anim = self.left_idle
		
		anim_frame = frame % (self.max_frames * self.frame_mult)
		
		screen.blit(self.current_anim[anim_frame], self.rect)

	
class NPC(Character):
	def __init__(
		self, 
		name : str, 
		type : str, 
		max_frames : int,
		frame_mult : int = 4,
	):
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
		weakness : list[str],
		max_frames : int,
		frame_mult : int = 4,
	):
		Character.__init__(self, name, type, max_frames, frame_mult)
		self.max_hp = max_hp
		self.max_mana = max_mana
		self.weakness = weakness
		self.collision_type = "battle"
		self.setAttackAnimations()
	
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
		max_frames : int,
		weapons : list[wp.Weapon] = [],
		spells : list[wp.Spell] = [],
		frame_mult : int = 4,
	):
		Character.__init__(self, name, type, max_frames, frame_mult)
		self.max_hp = max_hp
		self.max_mana = max_mana
		self.weapons = weapons
		self.spells = spells

	def setSpells(
		self, 
		spells : dict[str, wp.Spell],
	):
		self.spells = copy.deepcopy(spells)

# nemico = Enemy("Mostro", 150, {"fire", "ice"}, 15, 10)
# print(nemico)

# mago = Character("Diego", 200, {"water"}, 20, 5)
# print(mago)

# knight = Subplayer("Cavaliere errante", "knight", "assets/knight1", 3, 8)
# knight.setWeapons()
#ecc

# player_classes = [
# 	knight
# ]

# orc = NPC("Orco ripugnante", "orc", 4)
mage = Subplayer("Mago Merlino", "mage", 100, 30, 4)
mage.setWeapons({
	"ascia" : wp.spade["ascia"],
	"arco" : wp.archi["semplice"]
})
# princess = NPC("Principessa", "princess", 4)
knight = Subplayer("Cavaliere", "knight", 100, 30, 4)
archer = Subplayer("Robin Hood", "archer", 100, 30, 4)
