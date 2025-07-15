import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH

import weapons as wp

class Chest:
    def __init__(
        self, 
        has_collision : bool,
        scale_fact : int | float = 1,
        items : list = [],
    ) -> None:
        self._path = f"{ASSETS_PATH}/objects/chest"
        self.has_collision = has_collision
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._static = pygame.image.load(f"{self._path}/static.png")
        self._static = pygame.transform.scale_by(self._static, self._scale_fact)
        self.rect = self._static.get_rect()
        self._current = self._static
        self._getItems(items)
        self._opened = pygame.image.load(f"{self._path}/open.png")
        self._opened = pygame.transform.scale_by(
            self._opened, self._scale_fact,
        )

    def _getItems(
        self,
        items : list,
    ) -> None:
        self.items = []
        for item in items:
            self.items.append(
                wp.CLASSES[item["class"]](**(item["args"]))
            )

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

    def collision(self) -> None:
        self.has_collision = False
        self._toOpen()