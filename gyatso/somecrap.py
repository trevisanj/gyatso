__all__ = ["get_defaultfont", "render_lines"]

import pygame, pygame.freetype, gyatso


def get_defaultfont():
    return pygame.freetype.SysFont(gyatso.FONTFAMILY, gyatso.FONTSIZE)


def render_lines(surf, lines, color, padding=10, linespacing=10, font=None):
    """Renders text as if the whole screen could be taken with this text"""
    if font is None: font = get_defaultfont()
    fontheight = font.render("test8#TAIpy", (0, 0, 0))[1].height

    y = padding
    if not isinstance(lines, list):
        lines = lines.split("\n")
    for line in lines:
        ot, _ = font.render(line, color)
        surf.blit(ot, (padding, y))
        y += fontheight+linespacing