__all__ = ["get_defaultfont", "render_lines", "TextStyle"]

import pygame, pygame.freetype, gyatso, os


def get_defaultfont():
    # return pygame.freetype.SysFont(gyatso.FONTFAMILY, gyatso.FONTSIZE)
    filename = os.path.join(os.path.split(__file__)[0], "3270Medium.otf")
    return pygame.freetype.Font(filename, gyatso.FONTSIZE)


def render_lines(surf, lines, style=None, padding=10, linespacing=10):
    """Renders text as if the whole screen could be taken with this text"""
    if style is None: style = TextStyle()

    y = padding
    if not isinstance(lines, list):
        lines = lines.split("\n")
    for line in lines:
        ot, _ = style.font.render(line, style.color)
        surf.blit(ot, (padding, y))
        y += style.fontheight+linespacing


class TextStyle:
    @property
    def font(self):
        self.__init_font()
        return self.__font

    @font.setter
    def font(self, value):
        self.__font = value

    @property
    def fontheight(self):
        self.__init_font()
        return self.__fontheight

    @property
    def fontwidth(self):
        self.__init_font()
        return self.__fontwidth

    def __init__(self, font=None, color=(0, 255, 0)):
        self.font = font
        self.__fontwidth = None
        self.__fontheight = None
        self.color = color

    def __init_font(self):
        if self.__font is None:
            self.__font = gyatso.get_defaultfont()
            o = self.__font.render("▒", (0, 0, 0))[1]
            self.__fontwidth, self.__fontheight = o.width, o.height
