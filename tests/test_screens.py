import math

from pyglet.window import Window, key

import pytest
from pong.game import Pong
from pong.game_objects import Ball
from pong.screens import GameScreen, TitleScreen


@pytest.fixture(scope="function")
def game():
    game = Pong(Window(visible=False))
    game.load()
    return game


def test_title_screen_construction(game):
    s = TitleScreen(game)
    s.on_draw()
    s.update(0.01)


def test_game_screen_construction(game):
    s = GameScreen(game)
    s.on_draw()
    s.update(0.01)


def test_title_to_game_screen_switch(game):
    game.set_screen(TitleScreen(game))
    game.keys[key.ESCAPE] = True
    game.screen.update(0.01)
    assert isinstance(game.screen, GameScreen)


def test_left_side_scores(game):
    s = GameScreen(game)
    assert s.left_score == 0
    assert s.right_score == 0
    ball = [obj for obj in s.game_objects if isinstance(obj, Ball)][0]
    # Remove paddles
    s.game_objects.clear()
    s.game_objects.append(ball)
    ball.direction = 0
    for i in range(100):
        s.update(0.01)
    assert s.left_score == 1
    assert s.right_score == 0


def test_right_side_scores(game):
    s = GameScreen(game)
    assert s.left_score == 0
    assert s.right_score == 0
    ball = [obj for obj in s.game_objects if isinstance(obj, Ball)][0]
    # Remove paddles
    s.game_objects.clear()
    s.game_objects.append(ball)
    ball.direction = math.pi
    for i in range(100):
        s.update(0.01)
    assert s.left_score == 0
    assert s.right_score == 1


def test_collision_handling(game):
    s = GameScreen(game)
    ball = [obj for obj in s.game_objects if isinstance(obj, Ball)][0]
    # Should hit right-side paddle
    ball.direction = 0
    for i in range(100):
        s.update(0.01)
    assert ball.direction == math.pi
