import pygame
import config as cfg

X_RATIO = cfg.X_RATIO
Y_RATIO = cfg.Y_RATIO

class Box:
    def __init__(
        self,
        type : str,
        size : tuple[int,int],
    ):
        self.type = type
        self.size = size
        self.scale_fact = (
            (self.size[0]/254)*X_RATIO, (self.size[1]/105)*Y_RATIO
        )
        
        self._setBox()

        
    def _setBox(self):
        if self.type == "inventory":
            self.box = pygame.image.load("assets/dialogue/inventory.png")
            self.box = pygame.transform.scale_by(self.box, (X_RATIO, Y_RATIO))
        else:
            self.box = pygame.image.load("assets/dialogue/static.png")
            self.box = pygame.transform.scale_by(self.box, self.scale_fact)
        self.box_rect = self.box.get_rect()

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ):
        self.box_rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self.box, self.box_rect)

class Text:

    def __init__(
            self,
            text : str,
            from_file : bool = False,
            font_name : str = "pixel",
            font_color : str = "white",
            font_size : int =  10,
            align : str = "left",
            wrap : bool = False,
            scale_fact : int | tuple[int, int] = (X_RATIO, Y_RATIO),
    ):
        text_align = {
            "left" : pygame.FONT_LEFT,
            "center" : pygame.FONT_CENTER,
            "right" : pygame.FONT_RIGHT,
        }
        pygame.font.init()
        if from_file:
            self.path = text
            self.text = self._setText()
        else:
            self.text = text
        self.font = pygame.font.Font(f"assets/font/{font_name}.ttf")
        self.font.align = text_align[align]
        self.font.point_size = font_size
        if wrap:
            self.surface = self.font.render(
                self.text, False, font_color, wraplength = 242
            )
        else:
            self.surface = self.font.render(self.text, False, font_color)
        self.surface = pygame.transform.scale_by(self.surface, scale_fact)
        self.rect = self.surface.get_rect()


    def _setText(self):
        text_file = open(f"assets/dialogue/{self.path}.txt")
        text = text_file.read()
        text_file.close()
        return text
    
    def show(
        self,
        screen : pygame.Surface,
        pos : tuple[int, int],
    ):
        self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self.surface, self.rect)


class TextBox(Box):
    def __init__(
        self,
        type : str,
        text_path : str,
        size : tuple[int,int],
        font_name : str = "pixel",
        font_color : str = "white",
        font_size : int = 10,
        align : str = "left",
    ):
        Box.__init__(self, type, size)
        self.text = Text(
            text_path, 
            from_file=True, 
            font_name=font_name, 
            font_color=font_color, 
            font_size=font_size, 
            align=align, 
            wrap=True, 
            scale_fact=self.scale_fact,
        )

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ):
        Box.show(self, screen, pos)
        self.text.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self.text.surface, self.text.rect)

test_dialogue = TextBox("window", "testo0", (300, 100))
