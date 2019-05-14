import sys
import pygame
from itertools import cycle
from utils.img_functions import get_hitmask

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
PLAYER_PATH = (
    'assets/sprites/redbird-upflap.png',
    'assets/sprites/redbird-midflap.png',
    'assets/sprites/redbird-downflap.png'
)
# path of background
BACKGROUND_PATH = 'assets/sprites/background-black.png'
# path of pipe
PIPE_PATH = 'assets/sprites/pipe-green.png'
# sounds

PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])

PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
FPSCLOCK = pygame.time.Clock()

if 'win' in sys.platform:
    soundExt = '.wav'
else:
    soundExt = '.ogg'


def load():
    pygame.init()
    images, sounds, hitmasks = {}, {}, {}
    # numbers sprites for score display
    images['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    # base (ground) sprite
    images['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    sounds['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    sounds['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    sounds['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
    sounds['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    sounds['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    # select random background sprites
    images['background'] = pygame.image.load(BACKGROUND_PATH).convert()

    # select random player sprites
    images['player'] = (
        pygame.image.load(PLAYER_PATH[0]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[1]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[2]).convert_alpha(),
    )

    # select random pipe sprites
    images['pipe'] = (
        pygame.transform.rotate(
            pygame.image.load(PIPE_PATH).convert_alpha(), 180),
        pygame.image.load(PIPE_PATH).convert_alpha(),
    )

# hismask for pipes
    hitmasks['pipe'] = (
        get_hitmask(images['pipe'][0]),
        get_hitmask(images['pipe'][1]),
    )

    # hitmask for player
    hitmasks['player'] = (
        get_hitmask(images['player'][0]),
        get_hitmask(images['player'][1]),
        get_hitmask(images['player'][2]),
    )

    return images, sounds, hitmasks


def load_game_constants():
    images, sound, hitmasks = load()
    BACKGROUND_WIDTH = images['background'].get_width()
    PIPE_WIDTH = images['pipe'][0].get_width()
    PIPE_HEIGHT = images['pipe'][0].get_height()
    U_HIT_MASK = hitmasks['pipe'][0]
    I_HIT_MASK = hitmasks['pipe'][1]
    BASE_WIDTH = images['base'].get_width()
    PLAYER_WIDTH = images['player'][0].get_width()
    PLAYER_HEIGHT = images['player'][0].get_height()
    return BACKGROUND_WIDTH, PIPE_WIDTH, PIPE_HEIGHT, U_HIT_MASK, I_HIT_MASK, BASE_WIDTH, PLAYER_WIDTH,\
           PLAYER_HEIGHT, images, sound, hitmasks


BACKGROUND_WIDTH, PIPE_WIDTH, PIPE_HEIGHT, U_HIT_MASK, I_HIT_MASK, BASE_WIDTH, PLAYER_WIDTH, \
 PLAYER_HEIGHT, IMAGE, SOUND, HITMASKS = load_game_constants()
