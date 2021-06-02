import pygame
import random
import sys
import Data

pygame.init()
screen_w = 500
screen_h = 400
mainWindow = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption('flappy bird')

white = (255, 255, 255)
black = (0, 0, 0)
red = "#b61827"
blue = "#0077c2"

clock = pygame.time.Clock()

wall_top = pygame.Rect(800, 0, 40, 120)
wall_bottom = pygame.Rect(800, 280, 40, 120)
bird = pygame.Rect(80, 150, 50, 50)
v_wall = -10
v_bird = 5
a_bird = 1

background_img = pygame.image.load('photos/background.png')
background_img_resized = pygame.transform.scale(background_img, (500, 400))

bird1_img = pygame.image.load('photos/bird1.png')
bird1_img = pygame.transform.scale(bird1_img, (50, 50))

bird2_img = pygame.image.load('photos/bird2.png')
bird2_img = pygame.transform.scale(bird2_img, (50, 50))

bird3_img = pygame.image.load('photos/bird3.png')
bird3_img = pygame.transform.scale(bird3_img, (50, 50))

bird4_img = pygame.image.load('photos/bird4.png')
bird4_img = pygame.transform.scale(bird4_img, (50, 50))

bird_images = [bird1_img, bird1_img, bird1_img, bird1_img,
               bird2_img, bird2_img, bird2_img, bird2_img,
               bird3_img, bird3_img, bird3_img, bird3_img,
               bird4_img, bird4_img, bird4_img, bird4_img]

wall_top_img = pygame.image.load('photos/wall.png')
wall_top_img = pygame.transform.scale(wall_top_img, (40, 120))

wall_bottom_img = pygame.image.load('photos/wall.png')
wall_bottom_img = pygame.transform.scale(wall_bottom_img, (40, 120))

i_bird = 0
score = 0
myfont_1 = pygame.font.Font('Font/calibrib.ttf', 90)
myfont_2 = pygame.font.Font('Font/calibrib.ttf', 30)
pause_text = myfont_1.render('Pause', True, red)
gameover_text = myfont_1.render('Gameover', True, red)

score_text = myfont_2.render(f'Score : {score}', True, blue)
best_score_text = myfont_2.render(f"Best Score : {Data.get_best_score()}", True, blue)

state = "start"
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Data.con.close()
            pygame.quit()
            sys.exit()

    mainWindow.blit(background_img_resized, (0, 0))
    mainWindow.blit(bird_images[i_bird], (bird.x, bird.y))
    mainWindow.blit(wall_top_img, (wall_top.x, wall_top.y))
    mainWindow.blit(wall_bottom_img, (wall_bottom.x, wall_bottom.y))
    mainWindow.blit(score_text, (0, 0))
    mainWindow.blit(best_score_text, (250, 0))
    score_text = myfont_2.render(f'Score : {score}', True, blue)
    best_score_text = myfont_2.render(f"Best Score : {Data.get_best_score()}", True, blue)
    Data.con.commit()
    if state == "playing":

        i_bird += 1
        if i_bird == len(bird_images):
            i_bird = 0
        if bird.x == (wall_top.x or wall_top.x):
            score += 1
        wall_top.x += v_wall
        wall_bottom.x += v_wall
        if bird.y < 0 and bird.x == wall_top.x:
            state = "gameover"
        bird.y += v_bird
        v_bird += a_bird

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            v_bird = -7
        if bird.y > 350:
            state = "gameover"
        if key_pressed[pygame.K_p]:
            state = "pause"
        if wall_top.x <= -40:
            wall_top.x = 800
            wall_bottom.x = 800
            wall_top.h = random.randint(20, 220)
            wall_bottom.h = 400 - wall_top.h - 160
            wall_bottom.y = wall_top.h + 160
            wall_top_img = pygame.transform.scale(wall_top_img, (40, wall_top.h))
            wall_bottom_img = pygame.transform.scale(wall_top_img, (40, wall_bottom.h))

        if bird.colliderect(wall_top) or bird.colliderect(wall_bottom):
            state = "add_data"

    if state == "add_data":
        Data.insert_score(score)
        Data.con.commit()
        state = "gameover"
    if state == "gameover":
        mainWindow.blit(gameover_text, (60, 150))
        if not bird.y > 360:
            bird.y += 5
    if state == "start":
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            state = "playing"
    if state == "pause":
        mainWindow.blit(pause_text, (120, 150))
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            state = "playing"
    pygame.display.update()
    clock.tick(30)
