import pygame
import random
colors = [
    (0, 0, 0),
    (109, 130, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
class Figure:
    x,y=0,0
    figures = [
        [[1, 5, 9, 12], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2  
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        i=0
        while i<height:
            new_line = []
            j=0
            while j<width:
                new_line.append(0)
                j+=1
            self.field.append(new_line)
            i+=1

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        i=0
        while i<4:
            j=0
            while j<4:
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i+self.figure.y][j+self.figure.x] > 0:
                        intersection = True
                j+=1
            i+=1
        return intersection

    def break_lines(self):
        lines = 0
        i=1
        while i<self.height:
            zeros = 0
            j=0
            while j<self.width:
                if self.field[i][j] == 0:
                    zeros += 1
                j+=1
            i+=1
            if zeros == 0:
                lines += 1
                k=i
                while k>1:
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
                    k-=1
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        i=0
        while i<4:
            j=0
            while j<4:
                if (4*i+j) in self.figure.image():
                    self.field[i+self.figure.y][j+self.figure.x]=self.figure.color
                j+=1
            i+=1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state="gameover"

    def go_side(self, dx):
        old_x=self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def go_left(self):
        dx=-1
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
        
    def go_right(self):
        dx=1
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (600, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")
work_done=False
clock = pygame.time.Clock()
fps = 40
game = Tetris(30, 20)
counter = 0

pressing_down = True
pressing_right=False
pressing_left=False
