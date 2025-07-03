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
		scale_fact : int | float = 1,
	) -> None:
		self._name = name
		self._type = type
		self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
		self._path = f"assets/weapons/{self._type}"
		self._damage = damage
		self._crit = crit
		self._max_frames = max_frames
		self._frame_mult = frame_mult
		self._setSprites()
		self._attacked = False
		self._current_frame = 0
	
	def _setSprites(self) -> None:
		self._static = pygame.image.load(f"{self._path}/static/static.png")
		self._static = pygame.transform.scale_by(self._static, self._scale_fact)
		self._rect = self._static.get_rect()
		self._left_attack = []
		self._right_attack = []
		for i in range(self._max_frames):
			for j in range(self._frame_mult):
				k = (self._frame_mult * i) + j
				self._left_attack.append(
					pygame.image.load(
						f"{self._path}/left_attack/{i%self._max_frames}.png"
					)
				)
				self._left_attack[k] = pygame.transform.scale_by(
					self._left_attack[k], self._scale_fact
				)
				self._right_attack.append(
					pygame.image.load(
						f"{self._path}/right_attack/{i%self._max_frames}.png"
					)
				)
				self._right_attack[k] = pygame.transform.scale_by(
					self._right_attack[k], self._scale_fact
				)

	def attackAnim(
		self, 
		screen : pygame.Surface, 
		rot : str, 
	) -> None:
		if self._current_frame < (self._max_frames*self._frame_mult):
			if rot == "left":
				self.current_anim = self._left_attack
			else:
				self.current_anim = self._right_attack
			screen.blit(self.current_anim[self._current_frame], self._rect)
			self._current_frame += 1
		else:
			self._current_frame = 0
			self._attacked = False

	def setPos(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static, self._rect)

	def attack(self) -> int:
		crit_prob = randint(1,100)
		if crit_prob <= self._crit:
			damage = self._damage * 2
		else:
			damage = self._damage
		self._attacked = True
		return damage
	
	def _setBox(self) -> None:
		self._box = tbx.Box("weapon", (128, 48))
		self._name_text = tbx.Text(
			f"{self._name}", align = "center", font_size=9
		)
		self._dmg_text = tbx.Text(
			f"Dmg: {self._damage}", align = "center", font_size=9
		)
		self._crit_text = tbx.Text(
			f"Crt: {self._crit}%", align = "center", font_size=9
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		self._setBox()
		self._box.show(screen, pos)
		self._showStatic(screen, (pos[0] - 48, pos[1]))
		self._name_text.show(screen, (pos[0]+8, pos[1] - 12))
		self._dmg_text.show(screen, (pos[0]-16, pos[1]+8))
		self._crit_text.show(screen, (pos[0]+32, pos[1]+8))
		
	def _showStatic(
		self,
		screen : pygame.Surface,
		pos : tuple[int, int],
	) -> None:
		self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
		screen.blit(self._static, self._rect)

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
	) -> None:
		Weapon.__init__(self, name, type, damage, crit, max_frames)
		self._effect = effect
		self._mana = mana

	def _setBox(self) -> None:
		Weapon._setBox(self)
		self._effect_text = tbx.Text(
			f"Effetto: {self._effect}", align = "center"
		)
		self._mana_text = tbx.Text(
			f"Mana: {self._mana}", align = "center"
		)

	def showBox(
		self, 
		screen : pygame.Surface, 
		pos : tuple[int, int],
	) -> None:
		Weapon.showBox(self, screen, pos)
		self._effect_text.show(screen, pos)
		self._mana_text.show(screen, pos)

	# def launch_spell(self, enemy : ch.Enemy):
	# 	phys_dmg = self.attack()
	# 	if self._effect in enemy.weakness:
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
	) -> None:
		type = "bow"
		Weapon.__init__(
			self, name, type, damage, crit, max_frames, frame_mult
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
	) -> None:
		Weapon.__init__(
			self, name, type, damage, crit, max_frames, frame_mult
		)

weapons = {
	"spada" : {
		"ascia" : Sword("Ascia vichinga", "axe", 20, 5, 4),
		"semplice" : Sword("Spada semplice", "sword", 20, 10, 8),
		"spadone" : Sword("Spadone lungo", "sword", 40, 10, 8),
		"martello" : Sword("Martello di Thor", "hammer", 50, 1, 4),
		"machete" : Sword("Machete", "machete", 15, 20, 4),
		"pugnale" : Sword("Pugnale", "dagger", 10, 2, 4, 8)
	},
	"arco" : {
		"semplice" : Bow("Arco semplice", 25, 10, 5, 5),
		"lungo" : Bow("Arco lungo", 45, 20, 5, 10),
		# "balestra" : Bow("balestra", 60, 5, 15)
	}
}

spells = {}

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