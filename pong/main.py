"""Entry point for the application."""
from pyglet.app import run
from pyglet.window import Window

from pong.game import Pong
from pong.screens import TitleScreen


def main() -> None:
    """Create the game object and starts the event loop."""
    pong = Pong(Window(width=1024, height=768))
    pong.load()
    pong.set_screen(TitleScreen(pong))
    run()


if __name__ == "__main__":
    main()  # pragma: no cover
