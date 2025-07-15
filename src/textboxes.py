from typing import Literal

import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH

pygame.font.init()
FONT = pygame.font.Font(f"{ASSETS_PATH}/font/pixel.ttf")

TEXT_ALIGN = {
    "left" : pygame.FONT_LEFT,
    "center" : pygame.FONT_CENTER,
    "right" : pygame.FONT_RIGHT,
}

class Box:
    def __init__(
        self,
        size : tuple[int,int],
        scale_fact : int | float = 1
    ) -> None:
        self._size = size
        self._scale_fact = (
            scale_fact*(self._size[0]/254)*X_RATIO, scale_fact*(self._size[1]/105)*Y_RATIO
        )
        self._setBox()
        
    def _setBox(self) -> None:
        self._box = pygame.image.load(f"{ASSETS_PATH}/dialogue/static.png")
        self._box = pygame.transform.scale_by(self._box, self._scale_fact)
        self.rect = self._box.get_rect()

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._box, self.rect)

class Text:

    def __init__(
        self,
        text : str,
        from_file : bool = False,
        font_color : str = "white",
        font_size : int =  10,
        align : Literal["left", "center", "right"] = "left",
        scale_fact : int | float = 1,
        wrap : bool = False,
    ) -> None:
        if from_file:
            self._path = text
            self.text = self._getText()
        else:
            self.text = text
        FONT.align = TEXT_ALIGN[align]
        FONT.point_size = font_size
        if wrap:
            self._wrap_length = 242
        else:
            self._wrap_length = 0
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._surface = FONT.render(self.text, False, font_color, wraplength=self._wrap_length)
        self._size = self._surface.get_rect().size
        self._surface = pygame.transform.scale_by(self._surface, self._scale_fact)
        self.rect = self._surface.get_rect()

    def changeColor(
        self,
        new_color : str,
    ) -> None:
        self._surface = FONT.render(self.text, False, new_color, wraplength=self._wrap_length)
        self._surface = pygame.transform.scale_by(self._surface, self._scale_fact)

    def _getText(self) -> str:
        with open(f"{ASSETS_PATH}/dialogue/{self._path}.txt") as text_file:
            text = text_file.read()
        return text
    
    def show(
        self,
        screen : pygame.Surface,
        pos : tuple[int, int],
    ) -> None:
        self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._surface, self.rect)


class TextBox(Text):
    def __init__(
        self,
        text : str,
        from_file : bool = False,
        font_color : str = "white",
        font_size : int = 10,
        align : Literal["left", "center", "right"] = "left",
        scale_fact : int | float = 1,
    ) -> None:
        Text.__init__(
            self, text, from_file, font_color, 
            font_size, align, scale_fact, wrap=True
        )
        box_size = (self._size[0]+16, self._size[1]+16)
        self._box = Box(box_size)

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        self._box.show(screen, pos)
        self.rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._surface, self.rect)

# test_dialogue = TextBox("window", "testo0", (300, 100))

CLASSES = {
    "TextBox" : TextBox,
    "Box" : Box,
    "Text" : Text,
}