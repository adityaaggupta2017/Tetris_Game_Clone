# 2ND FILE FOR DEFINING THE USES OF KEYS IN TETRIS
from project_main import *
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
