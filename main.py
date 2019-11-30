import pygame
import sys
from mic import Microphone
import time
from threading import Thread
from settings import *
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

m = Microphone()
m.start()

FPS = 60
clock = pygame.time.Clock()
dx = 0
speed = 1
penalty = 0
fscreen = [1, 2]
button = False
block = False

WIN_WIDTH, WIN_HEIGHT = 780, 630

OBJ_WIDTH = OBJ_HEIGHT = 30
BTN_WIDTH, BTN_HEIGHT = 220, 60
# MIN_VILUME = OBJ_HEIGHT
x1 = (WIN_WIDTH - OBJ_WIDTH) / 2.0
y1 = (WIN_HEIGHT - OBJ_HEIGHT) / 2.0
yyy = [y1] * 10
returns = [y1]

PLATFORM_WIDTH = PLATFORM_HEIGHT = 30
PLATFORM_COLOR = 'navy'

green = (0, 128, 0)
red = (250, 0, 0)
blue = (0, 0, 250)
white = (255, 255, 255)
BACKGROUND_COLOR = (192, 192, 192)

level = [
    # '-' * int(WIN_WIDTH / PLATFORM_WIDTH),
    '----------------------------------------------------------------------------------------------------------------------------------',
    '-                           -                          --                        ---                                  -          -',
    '-                                                      --                                                       -                -',
    '-                                                                                                                                -',
    '-            --                                                   -                                                              -',
    '-                                                                                                                                -',
    '--                                                                -                                                              -',
    '-                                                                                   ---                                          -',
    '-                                       --                                          ---                                     ---  -',
    '-                                                                                                                                -',
    '-                                                                                                                                -',
    '-                                                                                 -                                              -',
    '-                                                     -                                                                          -',
    '-   --------                                          -                                                                          -',
    '-                                                                                                                  -             -',
    '-                                                                  --                                              -             -',
    '-                   --                                                                                                           -',
    '-                                                                             -                                  --              -',
    '-                                   -          -                             -                                  ---              -',
    '-                                   -                                       -                           -                        -',
    '----------------------------------------------------------------------------------------------------------------------------------']

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Voice Control")
txt = pygame.font.SysFont('Arial', 22, True, False)
text = 'ИГРАТЬ СНОВА ?'
text_pos = txt.size(text)

brick = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
brick.fill(pygame.Color(PLATFORM_COLOR))

object1 = pygame.Surface((OBJ_WIDTH, OBJ_HEIGHT))
object1.fill(green)

btn = pygame.Surface((BTN_WIDTH, BTN_HEIGHT))
btn.fill(green)


def dy():
    while run:
        yyy.append(m.volume_norm)
        del yyy[0]
        y_obj = (WIN_HEIGHT - MIN_VILUME) - sum(yyy) / len(yyy)
        if y_obj < 0:
            y_obj = 0
        returns[0] = y_obj
        time.sleep(0.1)


run = True
Thread(target=dy).start()
while run:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            m.stream = False
            run = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_f:
            fscreen.reverse()
            if fscreen[0] == 1:
                screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            elif fscreen[0] == 2:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif e.type == pygame.MOUSEBUTTONDOWN and button is True:
            if e.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if (
                    mouse_pos[0] > (WIN_WIDTH - BTN_WIDTH) // 2
                    and mouse_pos[0] < (WIN_WIDTH + BTN_WIDTH) // 2
                    and mouse_pos[1] > WIN_HEIGHT // 2
                    and mouse_pos[1] < WIN_HEIGHT // 2 + BTN_HEIGHT
                ):
                    print('[INFO] Кнопка нажата')
                    penalty = 0
                    dx = 0
                    x1 = (WIN_WIDTH - OBJ_WIDTH) / 2.0

    if button is False and block is False:
        pygame.mouse.set_visible(False)
        block = True
    elif button is True and block is True:
        pygame.mouse.set_visible(True)
        block = False

    object1.fill(green)
    screen.fill(BACKGROUND_COLOR)

    y1 = returns[0]
    x = dx
    if dx > -WIN_WIDTH * 4:
        dx -= speed
    else:
        if x1 < WIN_WIDTH - OBJ_WIDTH:
            x1 += speed
    y = 0
    for row in level:
        for col in row:
            if col == '-':
                screen.blit(brick, (x, y))
                if brick.get_rect(center=(x, y)).colliderect(object1.get_rect(center=(x1, y1))):
                    if x1 < WIN_WIDTH - OBJ_WIDTH * 2:
                        object1.fill(red)
                        penalty += 0.1
                    else:
                        object1.fill(blue)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = dx

    if x1 < WIN_WIDTH - OBJ_WIDTH:
        button = False
        screen.blit(object1, (x1, y1))
        screen.blit(
            txt.render(str(round(penalty, 1)), True, white, None),
            ((WIN_WIDTH - txt.size(f'{round(penalty, 1)}')[0]) / 2.0, 4))
    else:
        button = True
        screen.blit(
            txt.render(f'Штрафных очков: {int(penalty)}', True, red, None),
            ((WIN_WIDTH - txt.size(f'Штрафных очков: {int(penalty)}')[0]) / 2.0,
             WIN_HEIGHT // 2 - BTN_HEIGHT))
        screen.blit(btn, ((WIN_WIDTH - BTN_WIDTH) // 2, WIN_HEIGHT // 2))
        screen.blit(
            txt.render(text, True, white, None),
            ((WIN_WIDTH - text_pos[0]) / 2.0, (WIN_HEIGHT + BTN_HEIGHT) // 2
             - text_pos[1] / 2.0))
    pygame.display.update()

sys.exit(0)
