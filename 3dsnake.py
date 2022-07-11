from base64 import urlsafe_b64decode
from turtle import position
from ursina import *
from game_objects import *
import os


MaxScore = 0
Score = 0
class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.borderless = False
        # window.fullscreen_size = 1920, 1080
        # window.fullscreen = True
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57

    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.black)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = Apple(self.MAP_SIZE, model='sphere', color=color.red)
        self.snake = Snake(self.MAP_SIZE)

    def input(self, key):
        if key == '2':
            camera.rotation_x = 0
            camera.position = (self.MAP_SIZE // 2, self.MAP_SIZE // 2, -50)
        elif key == '3':
            camera.position = (self.MAP_SIZE // 2, -20.5, -20)
            camera.rotation_x = -57
        super().input(key)
        

    def check_apple_eaten(self):
        if self.snake.segment_positions[-1] == self.apple.position:
            self.snake.add_segment()
            self.apple.new_position()
            global Score
            Score+=1
            for element in self.snake.segment_positions:
                if self.apple.position == element:
                    self.apple.new_position

    def check_game_over(self):
        snake = self.snake.segment_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)):
                return
        
        
        global Score,MaxScore
        if Score>MaxScore:
            with open('maxscore.txt','w') as f:
                f.write(str(Score))
        #print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        
        invoke(self.new_game, delay=1)

    def update(self):
        print_on_screen(f'Score: {self.snake.score}', position=(-0.85, 0.45), scale=3, duration=1 / 20)
        self.check_apple_eaten()
        self.check_game_over()
        try:
            sky_texture = load_texture('sky.jpg')
            sky = Sky()
        except:
            pass
        self.snake.run()
    def CheckForSave(self):
        if os.path.isfile('maxscore.txt'):
            global MaxScore
            try:
                with open('maxscore.txt','r') as f:
                    MaxScore = int(f.read)
                    f.close()
            except:
                with open('maxscore.txt','w') as f:
                    f.write('0')
                    MaxScore = 0
                    f.close()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.CheckForSave()
    game.run()
    