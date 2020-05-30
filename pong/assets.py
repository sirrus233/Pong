"""This module contains the main AssetManager object, along with the data structures
and helpers required to serve assets like textures and music to the game."""
from enum import Enum, auto
from typing import Dict

from pyglet.image import Texture, load
from pyglet.window import Window


class AssetTag(Enum):
    """Names of the accessible assets in the manager."""

    BALL = auto()
    BAR = auto()
    WALL = auto()


class AssetManager:
    """The AssetManager serves as a container for all the application's assets. A single
    instance of the class should be constructed when the game is loaded, and then
    persist for the lifetime of the application. Each asset is loaded only once (at
    startup), and then can be accessed directly.
    """

    def __init__(self) -> None:
        self.textures: Dict[AssetTag, Texture] = {}

    def load(self, window: Window) -> None:
        """Performs the actual loading of the assets into memory. Should be called
        exactly once, when the application starts."

        :param window: Game window.
        """
        self.textures[AssetTag.BALL] = load("assets/ball.png").get_texture()

        bar_img = load("assets/bar.png")
        bar_img.width = int(0.025 * window.width)
        bar_img.height = int(0.15 * window.height)
        self.textures[AssetTag.BAR] = bar_img.get_texture()

        wall_img = load("assets/bar.png")
        wall_img.width = window.width
        wall_img.height = int(0.025 * window.height)
        self.textures[AssetTag.WALL] = wall_img.get_texture()

    def get_asset(self, tag: AssetTag) -> Texture:
        """Retrieve an asset from the manager.

        :param tag: Name of the asset to retrieve.
        :return: The asset.
        """
        return self.textures[tag]
