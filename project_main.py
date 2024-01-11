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

while not work_done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter>100000:
        counter = 0

    if counter%(fps//game.level//2) == 0 or pressing_down or pressing_right or pressing_left:
        if game.state == "start":
            if pressing_down:
                game.go_down()
            if pressing_left:
                game.go_left()
            if pressing_right:
                game.go_right()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.rotate()
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True
            if event.key == pygame.K_DOWN:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

    screen.fill(WHITE)
    i=0
    while  i <(game.height):
        j=0
        while  j <(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
            j+=1
        i+=1
    if game.figure is not None:
        i=0
        while i<4:
            j=0
            while j<4:
                p=4*i+j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],[game.x + game.zoom * (j + game.figure.x) + 1,
                                     game.y + game.zoom * (i + game.figure.y) + 1,game.zoom - 2, game.zoom - 2])
                                    
                j+=1
            i+=1                        

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("ROWS COMPLETED :" + str(game.score), True, BLACK)
    text_game_over = font1.render("DEAD END", True, (255, 125, 0))
    screen.blit(text, [0, 0])
    if game.state == "DEAD END":
        screen.blit(text_game_over, [20, 200])
    pygame.display.flip()
    clock.tick(fps)
    
pygame.quit()# for ending the function after the game is complted stop the whole loop  from the teminal