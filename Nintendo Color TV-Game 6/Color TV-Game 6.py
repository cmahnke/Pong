import sys
import pygame.freetype
import pygame
import random
import ctypes
import math
import time
from pygame.locals import *


def left_score():
    global left_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning
    left_points += 1
    ballMoving = False
    ball.center = (width + 50, 300)
    dirchoice = 1
    scored = True
    leftMoving = False
    ballSpawning = True
    score_sound.play()


def right_score():
    global right_points, ballMoving, ball_speed, dirchoice, scored, leftMoving, ballSpawning
    right_points += 1
    ballMoving = False
    ball.center = (-50, 300)
    dirchoice = 0
    score_sound.play()
    leftMoving = True
    ballSpawning = True
    scored = True


def paddle_collision(ball, paddle):
    global vx, vy, ball_speed, direction, leftMoving, game
    alpha = 50
    c_point = ball.center[1] - paddle.center[1]
    c_point = c_point / (paddle_height / 2)
    if c_point < -1:
        ball.bottom = paddle.top
        c_point = -1
    elif c_point > 1:
        ball.top = paddle.bottom
        c_point = 1
    angle = c_point * alpha
    if paddle == left_paddle or paddle == left_paddle2:
        if c_point != -1 and c_point != 1:
            ball.left = paddle.right
        if angle < 0:
            direction = 360 + angle
        else:
            direction = angle
        leftMoving = False
        if game != 3:
            pygame.mouse.set_pos([width / 2, right_paddle.y])
    else:
        if c_point != -1 and c_point != 1:
            ball.right = paddle.left
        if angle == 0:
            direction = 180
        else:
            direction = 180 - angle
        leftMoving = True
        if game != 3:
            pygame.mouse.set_pos([width / 2, left_paddle.y])
    if 181 <= direction <= 185:
        direction = 180
    elif 355 <= direction <= 359:
        direction = 0
    vx = ball_speed * math.cos(math.radians(direction))
    vy = ball_speed * math.sin(math.radians(direction))
    ball.x += vx
    ball.y += vy
    paddle_hit_sound.play()
    return ball


def ball_movement(ball):
    global vx, vy, ballSpawning, game
    if ball.right >= width:
        left_score()
    elif ball.left <= 0:
        right_score()
    elif ballSpawning and 100 <= ball.centerx <= 1200:
        ballSpawning = False
    else:
        if ball.top <= 12:
            ball.top = 12
            vy *= -1
            wall_hit_sound.play()
        elif ball.bottom >= height - 12:
            ball.bottom = height - 12
            vy *= -1
            wall_hit_sound.play()
        elif game == 2:
            if ball.left <= 30 and not 210 <= ball.top <= 750 - ball_height:
                ball.left = 30
                vx *= -1
                wall_hit_sound.play()
            elif ball.right >= width - 30 and not 210 <= ball.top <= 750 - ball_height:
                ball.right = width - 30
                vx *= -1
                wall_hit_sound.play()
        elif game == 3 and ball.left <= 30:
            ball.left = 30
            vx *= -1
            wall_hit_sound.play()
        ball.x += vx * dt
        ball.y += vy * dt
    return ball


def move_up(paddle):
    if paddle.top <= -70:
        paddle.top = -70
        return paddle
    paddle.y -= paddle_speed * dt
    return paddle


def move_down(paddle):
    if paddle.bottom >= height + 70:
        paddle.bottom = height + 70
        return paddle
    paddle.y += paddle_speed * dt
    return paddle


def draw_net():
    for i in range(6):
        pygame.draw.rect(screen, (255, 255, 255), (485, 35 + (i * 130), 30, 65))
    # for i in range(15):
    #     pygame.draw.rect(screen, (red, green, blue), (623, i * 68, 3, 34))
    # pixel = 0
    # for h in range(193, 199, 2):
    #     for i in range(15):
    #         pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 4, 34))
    #     pixel += 4
    #     for i in range(15):
    #         pygame.draw.rect(screen, (red, green, blue), (625 + pixel, i * 68, 5, 34))
    #     pixel += 5


def draw_walls():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 20))
    pygame.draw.rect(screen, (255, 255, 255), (0, height-20, width, 20))
    # pygame.draw.rect(screen, (255, 255, 255), (0, 0, 20, 12))
    # pygame.draw.rect(screen, (255, 255, 255), (0, height - 12, 20, 12))
    # for i in range(36):
    #     pygame.draw.rect(screen, (255, 255, 255), (30 + i * 35, 0, 25, 12))
    #     pygame.draw.rect(screen, (255, 255, 255), (30 + i * 35, height - 12, 25, 12))


def draw_hockey_walls():
    for i in range(96):
        if 21 <= i < 75:
            continue
        pygame.draw.rect(screen, (255, 255, 255), (0, i*10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (0, (i * 10) + 8, 30, 2))
        pygame.draw.rect(screen, (255, 255, 255), (width - 30, i * 10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (width - 30, (i * 10) + 8, 30, 2))


def draw_handball_wall():
    for i in range(96):
        pygame.draw.rect(screen, (255, 255, 255), (0, i*10, 30, 8))
        pygame.draw.rect(screen, (0, 0, 0), (0, (i * 10) + 8, 30, 2))


def make_score():
    score_screen.fill(TENNISORANGE)
    if left_points < 10:
        if left_points == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points), fgcolor=(255, 255, 255))
    else:
        scoreFont.render_to(score_screen, (30, 0), 'l', fgcolor=(255, 255, 255))
        if left_points - 10 == 1:
            scoreFont.render_to(score_screen, (144, 0), str(left_points - 10), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (70, 0), str(left_points - 10), fgcolor=(255, 255, 255))
    if right_points < 10:
        if right_points == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points), fgcolor=(255, 255, 255))
    else:
        scoreFont.render_to(score_screen, (728, 0), 'l', fgcolor=(255, 255, 255))
        if right_points - 10 == 1:
            scoreFont.render_to(score_screen, (844, 0), str(right_points - 10), fgcolor=(255, 255, 255))
        else:
            scoreFont.render_to(score_screen, (770, 0), str(right_points - 10), fgcolor=(255, 255, 255))
    write_score()


def write_score():
    global game
    if game == 3:
        handball_screen.blit(score_screen, (0, 0))
        pygame.draw.rect(handball_screen, (0, 0, 0), (724, 0, 200, 200))
        screen.blit(handball_screen, (50, 32))
    else:
        screen.blit(score_screen, (50, 100))


def new_game(type):
    screen.fill((0, 0, 0))
    global left_points, right_points, leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, \
        gameStarted, ball, ballTimer, ballMoving, dirchoice, leftMoving
    if type == 0:
        gameStarted = False
    else:
        dirchoice = random.choice([0, 1])
        if dirchoice == 0:
            leftMoving = True
        else:
            leftMoving = False
        ball.center = (ballx, bally)
        left_points = 0
        right_points = 0
        ballTimer = 0
        leftMovingUp = False
        leftMovingDown = False
        rightMovingUp = False
        rightMovingDown = False
        ballMoving = False
        gameStarted = True


def tennis():
    global scored, scoreTime, ballMoving, ballTimer, ball, vx, vy, left_paddle, right_paddle, controls, \
        leftMovingUp, leftMovingDown, rightMovingUp, rightMovingDown, gameStarted, ballSpawning, rightx
    right_paddle.x = rightx
    if controls == 'Key':
        if leftMovingUp and not leftMovingDown:
            left_paddle = move_up(left_paddle)
        elif leftMovingDown and not leftMovingUp:
            left_paddle = move_down(left_paddle)
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
    if gameStarted and not ballSpawning and ball.colliderect(left_paddle):
        ball = paddle_collision(ball, left_paddle)
    elif gameStarted and not ballSpawning and ball.colliderect(right_paddle):
        ball = paddle_collision(ball, right_paddle)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    draw_walls()
    write_score()
    draw_net()
    # pygame.draw.rect(screen, (255, 255, 255), net)
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)


def hockey():
    global scored, gameStarted, scoreTime, ball, controls, left_paddle, right_paddle, left_paddle2, right_paddle2
    controls = 'Key'
    left_paddle2.y = left_paddle.y
    right_paddle2.y = right_paddle.y
    right_paddle.x = rightx
    if controls == 'Key':
        if leftMovingUp and not leftMovingDown:
            left_paddle = move_up(left_paddle)
            left_paddle2 = move_up(left_paddle2)
        elif leftMovingDown and not leftMovingUp:
            left_paddle = move_down(left_paddle)
            left_paddle2 = move_down(left_paddle2)
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
            right_paddle2 = move_up(right_paddle2)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
            right_paddle2 = move_down(right_paddle2)
    if gameStarted and not ballSpawning:
        if ball.colliderect(left_paddle):
            ball = paddle_collision(ball, left_paddle)
        elif ball.colliderect(left_paddle2):
            ball = paddle_collision(ball, left_paddle2)
        elif ball.colliderect(right_paddle):
            ball = paddle_collision(ball, right_paddle)
        elif ball.colliderect(right_paddle2):
            ball = paddle_collision(ball, right_paddle2)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    # write_score()
    draw_walls()
    draw_hockey_walls()
    draw_net()
    # pygame.draw.rect(screen, (255, 255, 255), net)
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)
    pygame.draw.rect(screen, (255, 255, 255), left_paddle2)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle2)


def handball():
    global controls, rightMovingUp, rightMovingDown, right_paddle, scored, gameStarted, scoreTime, leftMoving, ball
    right_paddle.x = 925
    leftMoving = False
    if controls == 'Key':
        if rightMovingUp and not rightMovingDown:
            right_paddle = move_up(right_paddle)
        elif rightMovingDown and not rightMovingUp:
            right_paddle = move_down(right_paddle)
    if gameStarted and not ballSpawning and ball.colliderect(right_paddle):
        ball = paddle_collision(ball, right_paddle)
    if scored:
        scored = False
        if gameStarted:
            make_score()
        scoreTime = time.time()
        if left_points == 15 or right_points == 15:
            new_game(0)
    # write_score()
    draw_handball_wall()
    draw_walls()
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
height = 810
width = 1000
display = pygame.display.set_mode((1280, 960))
display.fill((0, 0, 255))
screen = pygame.Surface((width, height))
score_screen = pygame.Surface((width, 255))
handball_screen = pygame.Surface((width, 255))
pygame.display.set_caption('Color TV-Game 6')
scoreFont = pygame.freetype.Font('text/nintendo.ttf', 132)
wall_hit_sound = pygame.mixer.Sound('sounds/wallhit.wav')
score_sound = pygame.mixer.Sound('sounds/score.wav')
paddle_hit_sound = pygame.mixer.Sound('sounds/paddlehit.wav')

FPS = 60
fpsClock = pygame.time.Clock()

paddle_height = 130
paddle_width = 30
ball_height = 20
ball_width = 26
leftx = 50
lefty = height // 2
rightx = width - 50 - paddle_width
righty = height // 2
ballx = -50
bally = -50
paddle_speed = 20.0
ball_speed = 15.0

TENNISORANGE = (169, 115, 93)

topWall = pygame.Rect(0, 0, width, 12)
bottomWall = pygame.Rect(0, height-12, width, 12)
# net = pygame.Rect(633, 0, paddle_width, height)
ball = pygame.Rect(ballx, bally, ball_width, ball_height)
left_paddle = pygame.Rect(leftx, lefty, paddle_width, paddle_height)
left_paddle2 = pygame.Rect(930, lefty, paddle_width, paddle_height)
right_paddle = pygame.Rect(rightx, righty, paddle_width, paddle_height)
right_paddle2 = pygame.Rect(320, righty, paddle_width, paddle_height)


left_points = 9
right_points = 9
ballTimer = 0
dt = 0
game = 1

controls = 'Mouse'
leftMovingUp = False
leftMovingDown = False
rightMovingUp = False
rightMovingDown = False
ballMoving = False
scored = False
gameStarted = True
ballSpawning = False

make_score()
dirchoice = random.choice([0, 1])
if dirchoice == 0:
    leftMoving = True
else:
    leftMoving = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.mouse.set_pos([0, 0])
scoreTime = time.time()
lastTime = time.time()
while True:
    dt = time.time() - lastTime
    dt *= FPS
    lastTime = time.time()
    screen.fill(TENNISORANGE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and event.key == K_LSHIFT:
            if controls == 'Mouse':
                controls = 'Key'
            else:
                controls = 'Mouse'
        elif event.type == KEYUP and event.key == K_SPACE:
            new_game(1)
            scoreTime = time.time()
            make_score()
        elif event.type == KEYUP and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and event.key == K_KP1:
            game = 1
        elif event.type == KEYUP and event.key == K_KP2:
            game = 2
        elif event.type == KEYUP and event.key == K_KP3:
            game = 3
        elif event.type == KEYUP and event.key == K_1:
            ball_speed = 15.0
            paddle_height = 150
            left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            left_paddle2 = pygame.Rect(930, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle2 = pygame.Rect(320, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
        elif event.type == KEYUP and event.key == K_2:
            ball_speed = 15.0
            paddle_height = 75
            left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            left_paddle2 = pygame.Rect(930, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle2 = pygame.Rect(320, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
        elif event.type == KEYUP and event.key == K_3:
            ball_speed = 29.0
            paddle_height = 150
            left_paddle = pygame.Rect(leftx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle = pygame.Rect(rightx, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            left_paddle2 = pygame.Rect(930, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
            right_paddle2 = pygame.Rect(320, pygame.mouse.get_pos()[1], paddle_width, paddle_height)
        if controls == 'Mouse':
            if event.type == MOUSEMOTION:
                position = pygame.mouse.get_pos()
                pygame.mouse.set_pos(width / 2, position[1])
                if leftMoving:
                    left_paddle.y = position[1]
                else:
                    right_paddle.y = position[1]
        elif controls == 'Key':
            if event.type == KEYUP:
                if event.key == K_w:
                    leftMovingUp = False
                elif event.key == K_s:
                    leftMovingDown = False
                elif event.key == K_UP:
                    rightMovingUp = False
                elif event.key == K_DOWN:
                    rightMovingDown = False
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    leftMovingUp = True
                elif event.key == K_s:
                    leftMovingDown = True
                elif event.key == K_UP:
                    rightMovingUp = True
                elif event.key == K_DOWN:
                    rightMovingDown = True
    if not ballMoving and ballTimer >= 1:
        ballMoving = True
        ball.y = random.randint(66, height-84)
        if dirchoice == 0:
            ball.x = width - 35
            quadrant = random.choice([2, 3])
            if quadrant == 2:
                direction = random.randint(91, 180)
            else:
                direction = random.randint(186, 269)
        else:
            ball.x = 35
            quadrant = random.choice([1, 4])
            if quadrant == 1:
                direction = random.randint(0, 84)
            else:
                direction = random.randint(276, 354)
        vx = ball_speed * math.cos(math.radians(direction))
        vy = ball_speed * math.sin(math.radians(direction))
        ballTimer = 0
    if ballMoving:
        ball = ball_movement(ball)
    if game == 1:
        tennis()
    elif game == 2:
        hockey()
    else:
        handball()
    if not ballMoving:
        ballTimer = time.time() - scoreTime
    pygame.draw.rect(screen, (255, 255, 255), ball)
    display.blit(screen, (140, 65))
    pygame.display.update()
    fpsClock.tick(FPS)