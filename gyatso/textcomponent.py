__all__ = ["TextComponent"]

from pygame.locals import *
import gyatso, math, pygame

# How many lines to walk up/down using the mouse wheel
WHEELINCREMENT = 3

class TextComponent(gyatso.Component):
    def __init__(self, *args, color=(0,255,0), bgcolor=(0,0,0), textstyle=None, padding=10, linespacing=10, scrollbarwidth=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.bgcolor = bgcolor
        self.textstyle = textstyle if textstyle is not None else gyatso.TextStyle()
        self.linespacing = linespacing
        self.padding = padding
        self.scrollbarwidth = scrollbarwidth
        self.__top = 0  # first line of text to be drawn
        self.__mode = "from_bottom"
        self.__flag_first = True
        self.__lines = []
        self.__numcoords = None

    # ABSTRACT =========================================================================================================

    def _get_lines(self):
        raise NotImplementedError()

    # OVERRIDE =========================================================================================================

    def do_handle_event(self, event):
        def respond_to_mouse_scrollbar(h, y):
            numlines = len(self.__lines)
            n = self.__get_num_visible_lines()
            self.__top = max(0, int(y / h * numlines - n / 2))
            self.__mode = "from_top"
            return self.game.redraw()

        ret = False
        if event.type == KEYDOWN:
            key = event.key

            if key == K_UP:
                self.__top = self.__top-1 if self.__top > 0 else self.__top  # I know this is ugly but can't be bothered
                self.__mode = "from_top"
                ret = self.game.redraw()

            elif key == K_DOWN:
                self.__top = self.__top+1 if self.__top < self.__get_count()-1 else self.__top
                self.__mode = "from_top"
                ret = self.game.redraw()

            elif key == K_PAGEUP:
                count = self.__get_count()
                if self.__numcoords is not None and self.__numcoords < count:
                    self.__top = max(0, self.__top-(self.__numcoords-1))
                    self.__mode = "from_top"
                    ret = self.game.redraw()

            elif key == K_PAGEDOWN:
                count = self.__get_count()
                if self.__numcoords is not None and self.__numcoords < count:
                    self.__top = min(count-1, self.__top+(self.__numcoords-1))
                    self.__mode = "from_top"
                    ret = self.game.redraw()

            elif key == K_HOME and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.__top = 0
                self.__mode = "from_top"
                ret = self.game.redraw()

            elif key == K_END and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.__top = self.__get_count()-1
                self.__mode = "from_top"
                ret = self.game.redraw()

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                x, y = event.pos
                w, h = self.game.screen.get_size()
                if x > w - self.scrollbarwidth:
                    ret = respond_to_mouse_scrollbar(h, y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                w, h = self.game.screen.get_size()
                if x > w-self.scrollbarwidth:
                    ret = respond_to_mouse_scrollbar(h, y)

            if event.button == 4:  # wheel up
                self.__top = max(0, self.__top-WHEELINCREMENT)
                self.__mode = "from_top"
                ret = self.game.redraw()
            elif event.button == 5: # wheel down
                self.__top = min(self.__get_count()-1, self.__top+WHEELINCREMENT)
                self.__mode = "from_top"
                ret = self.game.redraw()
        return ret


    def do_draw(self, surf):
        def build_ycoords():
            # n*fontheight+(n-1)*linespacing+padding >= height
            n = self.__get_num_visible_lines()
            fh = self.textstyle.fontheight
            y1 = height-1-self.padding-fh
            step = fh+self.linespacing
            ycoords = [y1-i*step for i in range(n)]
            return ycoords

        width, height = surf.get_size()
        ycoords = build_ycoords()
        self.__numcoords = numcoords = len(ycoords)
        lines = self.__lines = self._get_lines()
        surf.fill(self.bgcolor)

        numlines = len(lines)
        if numlines <= numcoords: self.__mode = "from_bottom"  # invalidates otherwise
        if self.__mode == "from_bottom":
            iline = numlines-1
        else:
            if self.__top+numcoords > numlines:
                self.__top = numlines-numcoords
            iline = self.__top+numcoords-1
        if iline == numlines-1: self.__mode = "from_bottom"

        icoord = 0
        lastline = iline
        while icoord < numcoords and iline >= 0:
            line = lines[iline]
            y = ycoords[icoord]
            ot, _ = self.textstyle.font.render(line, self.textstyle.color)
            surf.blit(ot, (self.padding, y))
            self.__top = firstline = iline
            icoord += 1
            iline -= 1

        # "Scrollbar" (non-responsive though, but TODO one could store the coordinates from this drawing to make it responsive)

        x0 = width-self.scrollbarwidth
        # x1 = width-1
        y0 = 0
        y1 = height-1
        f_rect = lambda c, w: pygame.draw.rect(surf, color=c, rect=(x0, y0, self.scrollbarwidth, y1-y0+1), width=w)
        f_rect(self.bgcolor, 0)
        f_rect(self.color, 1)
        if numlines > 0:
            lastline1 = lastline+1
            a = (y1-y0+1)/numlines
            b = y0
            ybox0 = a*firstline+b
            ybox1 = a*lastline1+b
            pygame.draw.rect(surf, self.color, (x0, ybox0, self.scrollbarwidth, ybox1-ybox0+1), width=0)

    # PRIVATE ==========================================================================================================


    def __get_count(self):
        # This is a default, slow, implementation
        return len(self._get_lines())

    def __get_num_visible_lines(self):
        height = self.game.screen.get_size()[1]
        fh = self.textstyle.fontheight
        n = math.ceil((height + self.linespacing - self.padding) / (fh + self.linespacing))
        return n