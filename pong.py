import pyglet
from pyglet.window import key
import math

class GameObject:
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.sprite.set_position(x, y)

    def collision(self, obj):
        self_right = self.x + self.sprite.width
        self_left = self.x
        self_top = self.y + self.sprite.height
        self_bottom = self.y
        obj_right = obj.x + obj.sprite.width
        obj_left = obj.x
        obj_top = obj.y + obj.sprite.height
        obj_bottom = obj.y

        separate = self_right < obj_left or self_left > obj_right or self_top < obj_bottom or self_bottom > obj_top 
        return not separate

class Velocity:
    def __init__(self):
        self.speed = 0
        self.direction = 0

class Ball(GameObject):
    def __init__(self):
        self.velocity = Velocity()
        self.acceleration = 0
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["BALL"], batch=batch)
    
    def update(self, dt):
        if self.collision(top_wall) or self.collision(bottom_wall):
            self.velocity.direction = -self.velocity.direction

        if self.collision(left_paddle) or self.collision(right_paddle):
            self.velocity.direction = -self.velocity.direction + math.pi
            self.velocity.speed += self.acceleration

        x = self.x + self.velocity.speed * math.cos(self.velocity.direction) 
        y = self.y + self.velocity.speed * math.sin(self.velocity.direction) 
        self.set_position(x, y)

class Paddle(GameObject):
    def __init__(self, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key
        self.speed = 10
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["BAR"], batch=batch)

    def update(self, dt):
        if keys[self.up_key] and not self.collision(top_wall):
            self.set_position(self.x, self.y+self.speed)
        elif keys[self.down_key] and not self.collision(bottom_wall):
            self.set_position(self.x, self.y-self.speed)
            
class Wall(GameObject):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["WALL"], batch=batch)

class AssetManager:
    textures = dict()

    def load():
        AssetManager.textures["BALL"] = pyglet.image.load("ball.png").get_texture()

        bar_img = pyglet.image.load("bar.png")
        bar_img.width = 25
        bar_img.height = 120
        AssetManager.textures["BAR"] = bar_img.get_texture()

        wall_img = pyglet.image.load("bar.png")
        wall_img.width = window.width 
        wall_img.height = 20
        AssetManager.textures["WALL"] = wall_img.get_texture()

# Window and game setup
window = pyglet.window.Window(width=1024, height=768)
keys = key.KeyStateHandler()
batch = pyglet.graphics.Batch()
AssetManager.load()

# Game object initialization
ball = Ball()
left_paddle = Paddle(key.W, key.S)
right_paddle = Paddle(key.UP, key.DOWN)
top_wall = Wall()
bottom_wall = Wall()

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        pyglet.app.exit()
    
window.push_handlers(keys)

def main():
    ball.set_position(window.width//2, window.height//2)
    ball.velocity.speed = 5
    ball.velocity.direction = math.pi/4
    ball.acceleration = 1
    
    paddle_offset = 20
    left_paddle.set_position(paddle_offset, window.height//2)
    right_paddle.set_position(window.width-paddle_offset-right_paddle.sprite.width , window.height//2)

    top_wall.set_position(0, window.height-top_wall.sprite.height)
    bottom_wall.set_position(0, 0)

    pyglet.clock.schedule_interval(ball.update, 0.01)
    pyglet.clock.schedule_interval(left_paddle.update, 0.01)
    pyglet.clock.schedule_interval(right_paddle.update, 0.01)
    pyglet.app.run()

if __name__ == "__main__":
    main()
