"""Application screen objects.

A Screen is a logical collection of objects and business logic that work together to
form one "scene" of the game. A screen must construct its objects, and contain rules
for drawing and updating them each time the application ticks.

Screens can be switched on the fly by the main application object, to which each Screen
has a reference.
"""
from abc import abstractmethod
from itertools import combinations
from typing import TYPE_CHECKING

from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.text import Label

from pong.assets import AssetTag
from pong.game_objects import Ball, Paddle, Wall

if TYPE_CHECKING:
    from pong.game import Pong  # pragma: no cover


class Screen:
    """Abstract base class for other Screens."""

    def __init__(self, game: "Pong") -> None:
        self.game = game
        self.batch = Batch()

    def on_draw(self) -> None:
        """Called every frame, so that the application can draw itself."""
        self.game.window.clear()
        self.batch.draw()

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Called every frame, used to update all objects on the screen.

        :param delta_time: Real time passed between this frame and the last frame.
        :return:
        """


class TitleScreen(Screen):
    """Title screen of the game."""

    def __init__(self, game: "Pong") -> None:
        super().__init__(game)
        Label(
            "Pyglet Pong",
            font_name="Times New Roman",
            font_size=36,
            x=game.window.width // 2,
            y=game.window.height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        Label(
            "Press any key to start",
            font_name="Times New Roman",
            font_size=16,
            x=game.window.width // 2,
            y=game.window.height // 2 - 60,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

    def update(self, _: float) -> None:
        """Update this screen. Called each tick."""
        if True in self.game.keys.values():
            self.game.set_screen(GameScreen(self.game))


class GameScreen(Screen):
    """Main game screen. Holds the objects and business logic of core gameplay loop."""

    def __init__(self, game: "Pong") -> None:
        super().__init__(game)

        # Game object construction
        self.game_objects = [
            Ball(
                Sprite(
                    game.asset_manager.get_asset(AssetTag.BALL),
                    self.game.window.width // 2,
                    self.game.window.height // 2,
                    batch=self.batch,
                )
            ),
            Paddle(
                Sprite(
                    game.asset_manager.get_asset(AssetTag.BAR),
                    20,
                    self.game.window.height // 2,
                    batch=self.batch,
                ),
                self.game.controllers[0],
            ),
            Paddle(
                Sprite(
                    game.asset_manager.get_asset(AssetTag.BAR),
                    self.game.window.width
                    - 20
                    - game.asset_manager.get_asset(AssetTag.BAR).width,
                    self.game.window.height // 2,
                    batch=self.batch,
                ),
                self.game.controllers[1],
            ),
            Wall(
                Sprite(
                    game.asset_manager.get_asset(AssetTag.WALL),
                    0,
                    game.window.height
                    - game.asset_manager.get_asset(AssetTag.WALL).height,
                    batch=self.batch,
                )
            ),
            Wall(
                Sprite(
                    game.asset_manager.get_asset(AssetTag.WALL), 0, 0, batch=self.batch
                )
            ),
        ]

        self.left_score = 0
        self.right_score = 0

        self.left_score_label = Label(
            str(self.left_score),
            font_name="Times New Roman",
            font_size=25,
            x=game.window.width // 2 - 40,
            y=game.window.height - 50,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        self.right_score_label = Label(
            str(self.right_score),
            font_name="Times New Roman",
            font_size=25,
            x=game.window.width // 2 + 40,
            y=game.window.height - 50,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        self.reset()

    def reset(self) -> None:
        """Reset this screen. Useful for when a player has scored."""
        # Game object initialization
        for obj in self.game_objects:
            obj.reset()

        self.left_score_label.text = str(self.left_score)
        self.right_score_label.text = str(self.right_score)

    def update(self, _: float) -> None:
        """Update this screen. Called each tick."""
        for obj1, obj2 in combinations(self.game_objects, 2):
            if obj1.collision(obj2):
                obj1.collisions.append(obj2)
                obj2.collisions.append(obj1)

        for obj in self.game_objects:
            obj.update()
            obj.collisions.clear()

            if isinstance(obj, Ball):
                # Ball goes off screen
                if obj.sprite.x < 0:
                    self.right_score += 1
                    self.reset()
                elif obj.sprite.x > self.game.window.width:
                    self.left_score += 1
                    self.reset()
