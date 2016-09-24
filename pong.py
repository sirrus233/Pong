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
    def __init__(self, batch):
        self.velocity = Velocity()
        self.acceleration = 0
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["BALL"], batch=batch)
    
    def update(self):
        x = self.x + self.velocity.speed * math.cos(self.velocity.direction) 
        y = self.y + self.velocity.speed * math.sin(self.velocity.direction) 
        self.set_position(x, y)

class Paddle(GameObject):
    def __init__(self, batch, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key
        self.speed = 10
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["BAR"], batch=batch)

    def update(self, ball, top_wall, bottom_wall):
        if self.collision(ball):
            ball.velocity.direction = -ball.velocity.direction + math.pi
            ball.velocity.speed += ball.acceleration

        if keys[self.up_key] and not self.collision(top_wall):
            self.set_position(self.x, self.y+self.speed)
        elif keys[self.down_key] and not self.collision(bottom_wall):
            self.set_position(self.x, self.y-self.speed)
            
class Wall(GameObject):
    def __init__(self, batch):
        self.sprite = pyglet.sprite.Sprite(AssetManager.textures["WALL"], batch=batch)

    def update(self, ball):
        if self.collision(ball):
            ball.velocity.direction = -ball.velocity.direction

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

class Screen:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        window.push_handlers(self.on_draw)
        pyglet.clock.schedule_interval(self.update, 0.01)

    def on_draw(self):
        window.clear()
        self.batch.draw()
    
    def update(self, dt):
        pass

    def set_screen(self, screen):
        window.pop_handlers() 
        pyglet.clock.unschedule(self.update)
        screen()

class TitleScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        title_label = pyglet.text.Label(
                'Pyglet Pong',
                font_name='Times New Roman',
                font_size=36,
                x=window.width//2, y=window.height//2,
                anchor_x='center', anchor_y='center',
                batch=self.batch)

        start_label = pyglet.text.Label(
                'Press any key to start',
                font_name='Times New Roman',
                font_size=16,
                x=window.width//2, y=window.height//2 - 60,
                anchor_x='center', anchor_y='center',
                batch=self.batch)

    def update(self, dt):
        if True in keys.values():
            self.set_screen(GameScreen)
        

class GameScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        # Game object construction 
        self.ball = Ball(self.batch)
        self.left_paddle = Paddle(self.batch, key.W, key.S)
        self.right_paddle = Paddle(self.batch, key.UP, key.DOWN)
        self.top_wall = Wall(self.batch)
        self.bottom_wall = Wall(self.batch)

        self.top_wall.set_position(0, window.height-self.top_wall.sprite.height)
        self.bottom_wall.set_position(0, 0)
        
        self.left_score = 0
        self.right_score = 0
        
        self.left_score_label = pyglet.text.Label(
                str(self.left_score),
                font_name='Times New Roman',
                font_size=25,
                x=window.width//2 - 40, y=window.height - 50,
                anchor_x='center', anchor_y='center',
                batch=self.batch)

        self.right_score_label = pyglet.text.Label(
                str(self.right_score),
                font_name='Times New Roman',
                font_size=25,
                x=window.width//2 + 40, y=window.height - 50,
                anchor_x='center', anchor_y='center',
                batch=self.batch)

        self.reset()

    def reset(self):
        # Game object initialization
        self.ball.set_position(window.width//2, window.height//2)
        self.ball.velocity.speed = 5
        self.ball.velocity.direction = math.pi/4
        self.ball.acceleration = 1

        paddle_offset = 20
        self.left_paddle.set_position(paddle_offset, window.height//2)
        self.right_paddle.set_position(window.width-paddle_offset-self.right_paddle.sprite.width , window.height//2)

        self.left_score_label.text = str(self.left_score)
        self.right_score_label.text = str(self.right_score)

    def update(self, dt):
        self.ball.update()
        self.left_paddle.update(self.ball, self.top_wall, self.bottom_wall)
        self.right_paddle.update(self.ball, self.top_wall, self.bottom_wall)
        self.top_wall.update(self.ball)
        self.bottom_wall.update(self.ball)
        
        # Ball goes off screen
        if self.ball.x < 0:
            self.right_score += 1
            self.reset()
        elif self.ball.x > window.width:
            self.left_score += 1
            self.reset()
   
 
# Window and game setup
window = pyglet.window.Window(width=1024, height=768)
window.set_exclusive_mouse()
keys = key.KeyStateHandler()
AssetManager.load()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        pyglet.app.exit()
    
window.push_handlers(keys)

def main():
    TitleScreen()
    pyglet.app.run()

if __name__ == "__main__":
    main()


