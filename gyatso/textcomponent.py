__all__ = ["TextComponent"]

from pygame.locals import *
import gyatso

class TextComponent(gyatso.Component):
    def __init__(self, *args, color=(0,255,0), bgcolor=(0,0,0), **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.bgcolor = bgcolor
        self.__top = 0  # first line of text to be drawn

    # ABSTRACT =========================================================================================================

    def _get_lines(self):
        raise NotImplementedError()

    # OVERRIDE =========================================================================================================

    def do_handle_event(self, event):
        ret = False
        if event.type == KEYDOWN:
            key = event.key

            if key == K_UP:
                self.__top = self.__top-1 if self.__top > 0 else self.__top  # I know this is ugly but can't be bothered
                ret = self.game.redraw()

            elif key == K_DOWN:
                self.__top = self.__top+1 if self.__top < self.__get_count()-1 else self.__top
                ret = self.game.redraw()
        return ret

    def do_draw(self, surf):
        # game = self.game
        lines = self._get_lines()
        surf.fill(self.bgcolor)
        gyatso.render_lines(surf, lines[self.__top:], self.color)

    # PRIVATE ==========================================================================================================

    def __get_count(self):
        # This is a default, slow, implementation
        return len(self._get_lines())
