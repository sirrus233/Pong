import math

from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import key

import pytest
from pong.game import Controller
from pong.game_objects import Ball, Paddle, Wall

BALL_SPRITE = Sprite(load("assets/ball.png").get_texture())
WALL_SPRITE = Sprite(load("assets/ball.png").get_texture())
PADDLE_SPRITE = Sprite(load("assets/ball.png").get_texture())


@pytest.fixture(scope="function")
def ball():
    return Ball(BALL_SPRITE)


@pytest.fixture(scope="function")
def paddle():
    return Paddle(PADDLE_SPRITE, Controller(key.UP, key.DOWN))


@pytest.fixture(scope="function")
def wall():
    return Wall(WALL_SPRITE)


def test_ball_motion(ball):
    pos1 = ball.sprite.x, ball.sprite.y
    ball.update()
    pos2 = ball.sprite.x, ball.sprite.y
    assert pos1 != pos2


def test_ball_bounces_off_paddle_straight(ball, paddle):
    ball.direction = 0
    ball.collisions.append(paddle)
    ball.update()
    assert ball.direction == math.pi


def test_ball_bounces_off_paddle_at_angle(ball, paddle):
    ball.direction = math.pi / 4
    ball.collisions.append(paddle)
    ball.update()
    assert ball.direction == 3 * math.pi / 4


def test_ball_bounces_off_wall(ball, wall):
    ball.direction = math.pi / 4
    ball.collisions.append(wall)
    ball.update()
    assert ball.direction == -math.pi / 4


def test_ball_speed_changes_after_paddle_hit(ball, paddle):
    start_speed = ball.speed
    ball.collisions.append(paddle)
    ball.update()
    assert ball.speed > start_speed


def test_ball_speed_same_after_wall_hit(ball, wall):
    start_speed = ball.speed
    ball.collisions.append(wall)
    ball.update()
    assert ball.speed == start_speed


def test_ball_reset(ball, paddle):
    position = ball.sprite.x, ball.sprite.y
    speed = ball.speed
    direction = ball.direction
    ball.update()
    ball.collisions.append(paddle)
    ball.update()
    assert ball.sprite.x, ball.sprite.y != position
    assert ball.speed != speed
    assert ball.direction != direction
    ball.reset()
    assert ball.sprite.x, ball.sprite.y == position
    assert ball.speed == speed
    assert ball.direction == direction


def test_paddle_controls(paddle):
    start_y = paddle.sprite.y
    paddle.controller.player_up = True
    paddle.update()
    assert paddle.sprite.y > start_y
    paddle.controller.player_up = False
    paddle.controller.player_down = True
    paddle.update()
    assert paddle.sprite.y == start_y


def test_wall_blocks_paddle_up(paddle, wall):
    start_y = paddle.sprite.y
    wall.sprite.update(wall.sprite.x, start_y + 1)
    paddle.collisions.append(wall)

    paddle.controller.player_up = True
    paddle.update()
    assert paddle.sprite.y == start_y
    paddle.controller.player_up = False
    paddle.controller.player_down = True
    paddle.update()
    assert paddle.sprite.y < start_y


def test_wall_blocks_paddle_down(paddle, wall):
    start_y = paddle.sprite.y
    wall.sprite.update(wall.sprite.x, start_y - 1)
    paddle.collisions.append(wall)

    paddle.controller.player_down = True
    paddle.update()
    assert paddle.sprite.y == start_y
    paddle.controller.player_down = False
    paddle.controller.player_up = True
    paddle.update()
    assert paddle.sprite.y > start_y
