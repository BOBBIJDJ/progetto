from typing import Literal

import pygame

from config import X_RATIO, Y_RATIO, ASSETS_PATH

TEXT_ALIGN = {
    "left" : pygame.FONT_LEFT,
    "center" : pygame.FONT_CENTER,
    "right" : pygame.FONT_RIGHT,
}

class Box:
    def __init__(
        self,
        type : str,
        size : tuple[int,int],
        scale_fact : int | float = 1
    ) -> None:
        self._type = type
        self._size = size
        self._scale_fact = (
            scale_fact*(self._size[0]/254)*X_RATIO, scale_fact*(self._size[1]/105)*Y_RATIO
        )
        self._setBox()

        
    def _setBox(self) -> None:
        if self._type == "inventory":
            self._box = pygame.image.load(f"{ASSETS_PATH}/dialogue/inventory.png")
            self._box = pygame.transform.scale_by(self._box, (X_RATIO, Y_RATIO))
        else:
            self._box = pygame.image.load(f"{ASSETS_PATH}/dialogue/static.png")
            self._box = pygame.transform.scale_by(self._box, self._scale_fact)
        self._box_rect = self._box.get_rect()

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        self._box_rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._box, self._box_rect)

class Text:

    def __init__(
        self,
        text : str,
        from_file : bool = False,
        font_name : str = "pixel",
        font_color : str = "white",
        font_size : int =  10,
        align : Literal["left", "center", "right"] = "left",
        wrap : bool = False,
        scale_fact : int | float = 1,
    ) -> None:
        pygame.font.init()
        if from_file:
            self._path = text
            self._text = self._getText()
        else:
            self._text = text
        self._font = pygame.font.Font(f"{ASSETS_PATH}/font/{font_name}.ttf")
        self._font.align = TEXT_ALIGN[align]
        self._font.point_size = font_size
        if wrap:
            self._surface = self._font.render(
                self._text, False, font_color, wraplength = 242,
            )
        else:
            self._surface = self._font.render(self._text, False, font_color)
        self._scale_fact = (scale_fact*X_RATIO, scale_fact*Y_RATIO)
        self._surface = pygame.transform.scale_by(self._surface, self._scale_fact)
        self._rect = self._surface.get_rect()


    def _getText(self) -> str:
        text_file = open(f"{ASSETS_PATH}/dialogue/{self._path}.txt")
        text = text_file.read()
        text_file.close()
        return text
    
    def show(
        self,
        screen : pygame.Surface,
        pos : tuple[int, int],
    ) -> None:
        self._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._surface, self._rect)


class TextBox(Box):
    def __init__(
        self,
        type : str,
        text_path : str,
        size : tuple[int,int],
        font_name : str = "pixel",
        font_color : str = "white",
        font_size : int = 10,
        align : Literal["left", "center", "right"] = "left",
        scale_fact : int | float = 1,
    ) -> None:
        Box.__init__(self, type, size, scale_fact)
        self._text = Text(
            text_path, 
            from_file=True, 
            font_name=font_name, 
            font_color=font_color, 
            font_size=font_size, 
            align=align, 
            wrap=True, 
            scale_fact=scale_fact,
        )

    def show(
        self, 
        screen : pygame.Surface, 
        pos : tuple[int, int],
    ) -> None:
        Box.show(self, screen, pos)
        self._text._rect.center = (pos[0]*X_RATIO, pos[1]*Y_RATIO)
        screen.blit(self._text.surface, self._text.rect)

# test_dialogue = TextBox("window", "testo0", (300, 100))

CLASSES = {
    "TextBox" : TextBox,
    "Box" : Box,
    "Text" : Text,
}