from random import randint
import pygame
from config import X_RATIO, Y_RATIO
import objects as obj
import textboxes as tbx

class Weapon:
	def __init__(
		self, 
		name : str, 
		type : str, 
		damage : int, 
		crit : int,
		max_frames : int,
		frame_mult : int = 4,
	):
		self.name = name
		self.type = type
		self.scale_fact = (1*X_RATIO, 1*Y_RATIO)
		self.path = f"assets/weapons/{self.type}"
		self.damage = damage
		self.crit = crit
		self.max_frames = max_frames
		self.frame_mult = frame_mult
		self.setSprites()
		self.attacked = False
		self.current_frame = 0
	
	def setSprites(self):
		self.static = pygame.image.load(f"{self.path}/static/static.png")
		self.static = pygame.transform.scale_by(self.static, self.scale_fact)
		self.rect = self.static.get_rect()
		self.left_attack = []
		self.right_attack = []
		for i in range(self.max_frames):
			for j in range(self.frame_mult):
				k = (self.frame_mult * i) + j
				self.left_attack.append(
					pygame.image.load(
						f"{self.path}/left_attack/{i%self.max_frames}.png"
					)
				)
				self.left_attack[k] = pygame.transform.scale_by(
					self.left_attack[k], self.scale_fact
				)
				self.right_attack.append(
					pygame.image.load(
						f"{self.path}/right_attack/{i%self.max_frames}.png"
					)
				)
				self.right_attack[k] = pygame.transform.scale_by(
					self.right_attack[k], self.scale_fact
				)

	def attackAnim(
		self, 
		screen : pygame.Surface, 
		rot : str, 
	):
		if self.current_frame < (self.max_frames*self.frame_mult):
			if rot == "left":
				self.current_anim = self.left_attack
			else:
				self.current_anim = self.right_attack
			screen.blit(self.current_anim[self.current_frame], self.rect)
			self.current_frame += 1
		else:
			self.current_frame = 0
			self.attacked = False

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	):
		self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self.static, self.rect)

	def attack(self):
		crit_prob = randint(1,100)
		if crit_prob <= self.crit:
			damage = self.damage * 2
		else:
			damage = self.damage
		self.attacked = True
		return damage
	
	def setBox(self):
		self.box = tbx.Box("weapon", (128, 48))
		self.name_text = tbx.Text(
			f"{self.name}", align = "center", font_size=9
		)
		self.dmg_text = tbx.Text(
			f"Dmg: {self.damage}", align = "center", font_size=9
		)
		self.crit_text = tbx.Text(
			f"Crt: {self.crit}%", align = "center", font_size=9
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	):
		self.setBox()
		self.box.show(screen, pos)
		self.showStatic(screen, (pos[0] - 48, pos[1]))
		self.name_text.show(screen, (pos[0]+8, pos[1] - 12))
		self.dmg_text.show(screen, (pos[0]-16, pos[1]+8))
		self.crit_text.show(screen, (pos[0]+32, pos[1]+8))
		
	def showStatic(
		self,
		screen : pygame.Surface,
		pos : tuple[int, int],
	):
		self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self.static, self.rect)

class Spell(Weapon):
	def __init__(
		self, 
		name : str,
		type : str,
		damage : int, 
		crit : int,
		effect : str, 
		mana : int,
		max_frames : int, 
	):
		Weapon.__init__(self, name, type, damage, crit, max_frames)
		self.effect = effect
		self.mana = mana

	def setBox(self):
		Weapon.setBox(self)
		self.effect_text = tbx.Text(
			f"Effetto: {self.effect}", align = "center"
		)
		self.mana_text = tbx.Text(
			f"Mana: {self.mana}", align = "center"
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	):
		Weapon.showBox(self, screen, pos)
		self.effect_text.show(screen, pos)
		self.mana_text.show(screen, pos)

	# def launch_spell(self, enemy : ch.Enemy):
	# 	phys_dmg = self.attack()
	# 	if self.effect in enemy.weakness:
	# 		return phys_dmg * 2
	# 	else:
	# 		return phys_dmg

class Bow(Weapon):
	def __init__(
		self, 
		name : str,
		damage : int, 
		crit : int,
		max_frames : int,
		frame_mult : int = 4,
	):
		self.type = "bow"
		Weapon.__init__(
			self, name, self.type, damage, crit, max_frames, frame_mult
		)

class Sword(Weapon):
	def __init__(
		self, 
		name : str, 
		type : str,
		damage : int, 
		crit : int, 
		max_frames : int,
		frame_mult : int = 4
	):
		Weapon.__init__(
			self, name, type, damage, crit, max_frames, frame_mult
		)

spade = {
	"ascia" : Sword("Ascia vichinga", "axe", 20, 5, 4),
	"spada" : Sword("Spada semplice", "sword", 20, 10, 8),
	"spadone" : Sword("Spadone lungo", "sword", 40, 10, 8),
	"martello" : Sword("Martello di Thor", "hammer", 50, 1, 4),
	"machete" : Sword("Machete", "machete", 15, 20, 4),
	"pugnale" : Sword("Pugnale", "dagger", 10, 2, 4, 8)
}

archi = {
	"semplice" : Bow("Arco semplice", 25, 10, 5, 5),
	"lungo" : Bow("Arco lungo", 45, 20, 5, 10),
	# "balestra" : Bow("balestra", 60, 5, 15)
}

# incantesimi = {
# 	"fuoco" : Spell("sfera di fuoco", "fire", 40, 13, 7, "fuoco", 20),
# 	"ghiaccio" : Spell("bufera di neve", "ice", 35, 20, 10, "ghiaccio", 25),
# 	"aria" : Spell("vortice", "air", 25, 5, 5, "aria", 5),
# 	"acqua" : Spell("tsunami", "water", 45, 15, 10, "acqua", 30),
# 	"terra" : Spell("frana", "dirt", 30, 15, 4, "terra", 15)
# }

# def main():
# 	for spada in spade:
# 		print(spade[spada], "\n")
# 	for arco in archi:
# 		print(archi[arco], "\n")
# 	for inc in incantesimi:
# 		print(incantesimi[inc], "\n")
# 	return

# if __name__ == "__main__":
# 	main()