__all__ = ["Component"]

import serverlib as sl

class Component(sl.Intelligence):
    """
    Base class to structure the application flow, because it is becoming hard to concentrate the logic in a single class.

    The model gets away with draw() and handle_key() only. Accordingly, you, the implementor of descendant classes, will
    implement _draw() and _handle_event().
    """

    @property
    def game(self):
        return self.server

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.needs_draw = True
        self.suck_key = False

    # INHERITABLES =====================================================================================================

    # It is initialize() async def do_init(self):
    #     """This method is supposed to do things while the app is showing a splash screen."""

    def do_think(self):
        pass

    def do_draw(self, surf):
        return

    def do_draw_mousepos(self):
        """Returning False causes the game to draw its default"""
        return False

    def do_handle_event(self, event):
        return False

    def do_reset(self):
        pass

    # INTERFACE ========================================================================================================

    # async def init(self):
    #     await self.do_init()

    def think(self):
        self.do_think()

    def draw_mousepos(self):
        return self.do_draw_mousepos()

    def draw(self, surf):
        self.do_draw(surf)
        self.needs_draw = False

    def handle_event(self, event):
        return self.do_handle_event(event)

    def reset(self):
        self.game.set_status("")
        self.do_reset()
