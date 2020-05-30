"""Top level objects describing the Game application."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from pyglet.app import exit as pyglet_exit
from pyglet.clock import schedule_interval, unschedule
from pyglet.graphics import Batch
from pyglet.window import Window, key

from pong.assets import AssetManager

if TYPE_CHECKING:
    from pong.screens import Screen  # pragma: no cover


@dataclass
class Controller:
    """Abstraction over controls for a single player."""

    player_up_key: int
    player_down_key: int
    player_up: bool = False
    player_down: bool = False


class Pong:
    """This application represents the game as a whole. It contains the game window,
    and other objects that elements of a scene might need access to. It can set an
    active screen, and should be passed to each new Screen."""

    def __init__(self, window: Window) -> None:
        self.window = window
        self.keys = key.KeyStateHandler()
        self.asset_manager = AssetManager()
        self.batch = Batch()
        self.controllers = [Controller(key.W, key.S), Controller(key.UP, key.DOWN)]
        self.screen: Optional["Screen"] = None

    def load(self) -> None:
        """Run once on startup to initialize assets and event handlers.
        """

        def on_key_press(symbol: int, _: int) -> None:
            if symbol == key.ESCAPE:
                pyglet_exit()

            for controller in self.controllers:
                if symbol == controller.player_up_key:
                    controller.player_up = True
                elif symbol == controller.player_down_key:
                    controller.player_down = True

        def on_key_release(symbol: int, _: int) -> None:
            for controller in self.controllers:
                if symbol == controller.player_up_key:
                    controller.player_up = False
                elif symbol == controller.player_down_key:
                    controller.player_down = False

        self.window.set_handler("on_key_press", on_key_press)
        self.window.set_handler("on_key_release", on_key_release)
        self.window.push_handlers(self.keys)
        self.window.set_exclusive_mouse()

        self.asset_manager.load(self.window)

    def set_screen(self, next_screen: "Screen") -> None:
        """Change the active screen.

        :param next_screen: The new screen to be active.
        """
        if self.screen:
            self.window.pop_handlers()
            unschedule(self.screen.update)
        self.window.push_handlers(next_screen.on_draw)
        schedule_interval(next_screen.update, 0.01)
        self.screen = next_screen
