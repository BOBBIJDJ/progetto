import pygame

from config import X_RATIO, Y_RATIO

class Object:
    def __init__(
        self, 
        name : str, 
        path : str, 
        has_collision : bool = False,
        scale_fact : int | float = 1,
    ) -> None:
        self._name = name
        self._path = path
        self.has_collision = has_collision
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._static = pygame.image.load(f"{self._path}/static.png")
        self._static = pygame.transform.scale_by(self._static, self._scale_fact)
        self.rect = self._static.get_rect()
        self._current = self._static

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

    def collision(self):
        pass

class Item:
    pass

class Chest(Object):
    def __init__(
        self, 
        items : list[Item] = [],
    ) -> None:
        path = "assets/objects/chest"
        name = "chest"
        Object.__init__(self, name, path, has_collision = True)
        self.items = items
        self._opened = pygame.image.load(f"{self._path}/open.png")
        self._opened = pygame.transform.scale_by(
            self._opened, self._scale_fact,
        )

    def _toOpen(self) -> None:
        self._current = self._opened

    def collision(self) -> None:
        self.has_collision = False
        self._toOpen()
        # dà al giocatore un deterimanto oggetto
        # player.addItem(item)
        # dove item = {"name" : "pozione", "tipo" : obj.Item} 
        # che sarà qualcosa del tipo:
        # if  item["name"] in self.items:
        #       self.items["pozione"]["quantity"] += 1
        # else:
        #       self.items[item["name"]] = {"tipo" : copy.deepcopy(item["tipo"]), "quantity" = 1} 

CLASSES = {
    "Chest" : Chest,
    "Object" : Object,
}

items = {}