from pyglet.image import Texture
from pyglet.window import Window

from pong.assets import AssetManager, AssetTag


def test_asset_loading():
    am = AssetManager()
    am.load(Window(visible=False))
    for tag in AssetTag:
        assert isinstance(am.get_asset(tag), Texture)
