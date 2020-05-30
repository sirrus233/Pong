from unittest import mock
from unittest.mock import MagicMock

from pyglet import app
from pyglet.window import Window, key

import pytest
from pong.game import Pong
from pong.main import main


@pytest.fixture(scope="function")
def game():
    game = Pong(Window(visible=False))
    game.load()
    return game


@mock.patch("pong.main.Window")
@mock.patch("pong.main.run", new=MagicMock())
def test_game_startup(window_mock):
    window_mock.return_value = Window(visible=False)
    main()


def test_game_exit(game: Pong):
    assert not app.event_loop.has_exit
    game.window._allow_dispatch_event = True
    game.window.dispatch_event("on_key_press", key.ESCAPE, 0)
    assert app.event_loop.has_exit


def test_controllers(game: Pong):
    game.window._allow_dispatch_event = True
    game.window.dispatch_event("on_key_press", key.UP, 0)
    game.window.dispatch_event("on_key_press", key.DOWN, 0)
    assert game.controllers[1].player_up
    assert game.controllers[1].player_down
    game.window.dispatch_event("on_key_release", key.UP, 0)
    game.window.dispatch_event("on_key_release", key.DOWN, 0)
    assert not game.controllers[1].player_up
    assert not game.controllers[1].player_down
