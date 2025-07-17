import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH

import weapons as wp
import textboxes as tbx

class Chest:
    def __init__(
        self, 
        item : dict,
        has_collision : bool = True,
        is_large : bool = False,
        scale_fact : int | float = 1,
    ) -> None:
        self._path = f"{ASSETS_PATH}/objects/{"large_chest" if is_large else "chest"}"
        self.has_collision = has_collision
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._static = pygame.image.load(f"{self._path}/static.png")
        self._static = pygame.transform.scale_by(self._static, self._scale_fact)
        self.rect = self._static.get_rect()
        self._current = self._static
        self._getItems(item)
        self.has_item = True
        self._opened = pygame.image.load(f"{self._path}/open.png")
        self._opened = pygame.transform.scale_by(
            self._opened, self._scale_fact,
        )
        self._box = tbx.Box((160,96))
        self._text = tbx.Text(
            "Hai ottenuto:"
        )

    def _showItem(
        self,
        screen : pygame.Surface,
        pos : tuple[int, int],
    ) -> None:
        if pos[1] >= 256: 
            box_pos = (256, 128)
        else:
            box_pos = (256, 384)
        text_pos = (box_pos[0], box_pos[1]-24)
        item_pos = (box_pos[0], box_pos[1]+8)
        self._box.show(screen, box_pos)
        self._text.show(screen, text_pos)
        self.item.showBox(screen, item_pos)

    def _getItems(
        self,
        item : list,
    ) -> None:
        self.item = wp.CLASSES[item["class"]](**(item["args"]))

    def setPos(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        self.rect.center = pos
        screen.blit(self._current, self.rect)
    
    def show(
        self, 
        screen : pygame.Surface,
    ) -> None:
        screen.blit(self._current, self.rect)

    def _toOpen(self) -> None:
        self._current = self._opened

    def collision(
        self,
        screen : pygame.Surface,
        ) -> None:
        self.has_item = False
        self._toOpen()
        self._showItem(screen, self.rect.center)