import pygame
from pygame import gfxdraw
import sys
from mic import Microphone
import time
from threading import Thread
from settings import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{10},{30}'

m = Microphone()
m.start()

SPEED = 1
FPS = 60
clock = pygame.time.Clock()
dx = 0
penalty = 0
fscreen = [1, 2]
button = False
block = False

WIN_WIDTH, WIN_HEIGHT = 780, 630

BRICK_WIDTH = BRICK_HEIGHT = 30
BTN_WIDTH, BTN_HEIGHT = 220, 60
OBJ_SIZE = 40
ICON_SIZE = 32
# MIN_VILUME = OBJ_SIZE

BRICK_COLOR = (0, 0, 128)
BRICK_BD_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (192, 192, 192)
GREEN = (0, 128, 0, 200)
RED = (250, 0, 0, 200)
BLUE = (0, 0, 255, 200)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
obj_color = GREEN

level = [
    # '-' * int(WIN_WIDTH / BRICK_WIDTH),
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
icon = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
icon.fill(WHITE)
pygame.draw.circle(
    icon, pygame.Color('red'), [ICON_SIZE // 2, ICON_SIZE // 2], ICON_SIZE // 2)
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Voice Control")

txt = pygame.font.SysFont('Arial', 22, True, False)
text = 'ИГРАТЬ СНОВА ?'
text_pos = txt.size(text)

btn = pygame.Surface((BTN_WIDTH, BTN_HEIGHT))
btn.fill(GREEN)

obj = pygame.Surface((OBJ_SIZE + 1, OBJ_SIZE + 1), pygame.SRCALPHA)
# obj.set_colorkey((0, 0, 0))
obj_rect = obj.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
yyy = [obj_rect.center[1]] * 10
returns = [obj_rect.center[1]]


def face(color):
    pygame.gfxdraw.aacircle(  # контур лица
        obj, OBJ_SIZE // 2, OBJ_SIZE // 2, OBJ_SIZE // 2, color)
    pygame.gfxdraw.filled_circle(  # лицо
        obj, OBJ_SIZE // 2, OBJ_SIZE // 2, OBJ_SIZE // 2, color)
    pygame.gfxdraw.aacircle(  # глаз
        obj, OBJ_SIZE // 2 - OBJ_SIZE // 5, OBJ_SIZE // 2 - OBJ_SIZE // 8,
        OBJ_SIZE // 13, GOLD)
    pygame.gfxdraw.aacircle(  # глаз
        obj, OBJ_SIZE // 2 + OBJ_SIZE // 5, OBJ_SIZE // 2 - OBJ_SIZE // 8,
        OBJ_SIZE // 13, GOLD)
    pygame.gfxdraw.arc(  # рот
        obj, OBJ_SIZE // 2, OBJ_SIZE // 2, OBJ_SIZE // 2 - OBJ_SIZE // 5, 30, 150, GOLD)


def dy():
    while run:
        yyy.append(m.volume_norm)
        del yyy[0]
        y_obj = (WIN_HEIGHT - MIN_VILUME) - sum(yyy) / len(yyy)
        if y_obj < 0:
            y_obj = 0
        returns[0] = y_obj
        time.sleep(0.1)


face(obj_color)
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
                    print('[INFO] Кнопка нажата, новая игра')
                    penalty = 0
                    dx = 0
                    obj_rect.center = WIN_WIDTH // 2, WIN_HEIGHT // 2
                    yyy = [obj_rect.center[1]] * 10
                    returns = [obj_rect.center[1]]
                    obj_color = GREEN
                    face(obj_color)

    if button is False and block is False:
        pygame.mouse.set_visible(False)
        block = True
    elif button is True and block is True:
        pygame.mouse.set_visible(True)
        block = False

    obj_rect.y = returns[0]
    x = dx
    y = 0
    if dx > -WIN_WIDTH * 4:
        dx -= SPEED
    else:
        if obj_rect.x < WIN_WIDTH - OBJ_SIZE:
            obj_rect.x += SPEED

    if obj_color == RED:
        obj_color = GREEN
        face(obj_color)

    screen.fill(BACKGROUND_COLOR)
    for row in level:
        for col in row:
            if col == '-':
                brick = pygame.draw.rect(screen, BRICK_COLOR, [x, y, BRICK_WIDTH, BRICK_HEIGHT])
                pygame.draw.rect(screen, BRICK_BD_COLOR, [x, y, BRICK_WIDTH, BRICK_HEIGHT], 1)
                if brick.colliderect(obj_rect):
                    if obj_rect.x < WIN_WIDTH - OBJ_SIZE * 2:
                        penalty += 0.1
                        if obj_color == GREEN:
                            obj_color = RED
                            face(obj_color)
                    else:
                        obj_color = BLUE
                        face(obj_color)
            x += BRICK_WIDTH
        y += BRICK_HEIGHT
        x = dx

    if obj_rect.x < WIN_WIDTH - OBJ_SIZE:
        button = False
        screen.blit(obj, obj_rect)
        screen.blit(
            txt.render(str(round(penalty, 1)), True, WHITE, None),
            ((WIN_WIDTH - txt.size(f'{round(penalty, 1)}')[0]) / 2.0, 4))
    else:
        button = True
        screen.blit(
            txt.render(f'Штрафных очков: {int(penalty)}', True, RED, None),
            ((WIN_WIDTH - txt.size(f'Штрафных очков: {int(penalty)}')[0]) / 2.0,
             WIN_HEIGHT // 2 - BTN_HEIGHT))
        screen.blit(btn, ((WIN_WIDTH - BTN_WIDTH) // 2, WIN_HEIGHT // 2))
        screen.blit(
            txt.render(text, True, WHITE, None),
            ((WIN_WIDTH - text_pos[0]) / 2.0, (WIN_HEIGHT + BTN_HEIGHT) // 2
             - text_pos[1] / 2.0))
    pygame.display.update()

sys.exit(0)
