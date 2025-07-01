import pygame

import config as cfg

X_RATIO = cfg.X_RATIO
Y_RATIO = cfg.Y_RATIO

class Object:
    def __init__(
        self, 
        name : str, 
        path : str, 
        has_collision : bool = False,
    ):
        self.name = name
        self.path = path
        self.has_collision = has_collision
        self.scale_fact = (1*X_RATIO, 1*Y_RATIO)
        self.static = pygame.image.load(f"{self.path}/static.png")
        self.static = pygame.transform.scale_by(self.static, self.scale_fact)
        self.rect = self.static.get_rect()
        self.current = self.static

    def setPos(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ):
        self.rect.center = pos
        screen.blit(self.current, self.rect)
    
    def show(
        self, 
        screen : pygame.Surface,
    ):
        screen.blit(self.current, self.rect)

    def collision(self):
        pass

class Item:
    pass

class Chest(Object):
    def __init__(
        self, 
        items : list[Item] = [],
    ):
        path = "assets/objects/chest"
        name = "chest"
        Object.__init__(self, name, path, has_collision = True)
        self.items = items
        self.opened = pygame.image.load(f"{self.path}/open.png")
        self.opened = pygame.transform.scale_by(self.opened, self.scale_fact)

    def _toOpen(self):
        self.current = self.opened

    def collision(self):
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


chest = Chest("chest")

