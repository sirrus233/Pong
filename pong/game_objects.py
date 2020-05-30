"""Any object representable by a Sprite in the game world is in this module."""
import math
from abc import abstractmethod
from typing import List

from pyglet.sprite import Sprite

from pong.game import Controller


class GameObject:
    """Base class. An object representable by a Sprite in the game world. At a minimum,
    this will consist of a Sprite and a list of other GameObjects with which this
    object is colliding. Subclasses may extend this behavior to hold more gameplay
    related attributes."""

    def __init__(self, sprite: Sprite) -> None:
        self.sprite = sprite
        self.collisions: List[GameObject] = []

    @abstractmethod
    def update(self) -> None:
        """Called when the game screen updates."""

    @abstractmethod
    def reset(self) -> None:
        """Called when the game screen resets."""

    def collision(self, obj: "GameObject") -> bool:
        """Determine whether another object is colliding with this one.

        :param obj: Other object to test for collision.
        :return:
        """
        self_right = self.sprite.x + self.sprite.width
        self_left = self.sprite.x
        self_top = self.sprite.y + self.sprite.height
        self_bottom = self.sprite.y
        obj_right = obj.sprite.x + obj.sprite.width
        obj_left = obj.sprite.x
        obj_top = obj.sprite.y + obj.sprite.height
        obj_bottom = obj.sprite.y

        separate = (
            self_right < obj_left
            or self_left > obj_right
            or self_top < obj_bottom
            or self_bottom > obj_top
        )
        return not separate


class Ball(GameObject):
    """The game ball."""

    initial_speed: int = 5
    initial_direction: float = math.pi / 4
    initial_acceleration: int = 1

    def __init__(self, sprite: Sprite) -> None:
        super().__init__(sprite)
        self.start_x: int = self.sprite.x
        self.start_y: int = self.sprite.y
        self.speed: int = Ball.initial_speed
        self.direction: float = Ball.initial_direction
        self.acceleration: int = Ball.initial_acceleration

    def reset(self) -> None:
        """Reset this object."""
        self.sprite.update(self.start_x, self.start_y)
        self.speed = Ball.initial_speed
        self.direction = Ball.initial_direction
        self.acceleration = Ball.initial_acceleration

    def update(self) -> None:
        """Update the object."""
        # Paddle collisions
        if any(isinstance(obj, Paddle) for obj in self.collisions):
            self.direction = -self.direction + math.pi
            self.speed += self.acceleration

        # Wall collisions
        if any(isinstance(obj, Wall) for obj in self.collisions):
            self.direction = -self.direction

        self.sprite.update(
            self.sprite.x + self.speed * math.cos(self.direction),
            self.sprite.y + self.speed * math.sin(self.direction),
        )


class Paddle(GameObject):
    """A player-controlled paddle."""

    def __init__(self, sprite: Sprite, controller: Controller) -> None:
        super().__init__(sprite)
        self.start_x: int = self.sprite.x
        self.start_y: int = self.sprite.y
        self.controller = controller
        self.speed: int = 10

    def reset(self) -> None:
        """Reset this object"""

    def update(self) -> None:
        """Update the object."""
        if self.controller.player_up and not any(
            isinstance(obj, Wall) and obj.sprite.y > self.sprite.y
            for obj in self.collisions
        ):
            self.sprite.update(self.sprite.x, self.sprite.y + self.speed)

        if self.controller.player_down and not any(
            isinstance(obj, Wall) and obj.sprite.y < self.sprite.y
            for obj in self.collisions
        ):
            self.sprite.update(self.sprite.x, self.sprite.y - self.speed)


class Wall(GameObject):
    """Wall that forms one of the boundaries of the play area."""

    def __init__(self, sprite: Sprite) -> None:
        super().__init__(sprite)
        self.start_x: int = self.sprite.x
        self.start_y: int = self.sprite.y

    def reset(self) -> None:
        """Reset this object"""

    def update(self) -> None:
        """Update the object."""
