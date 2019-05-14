import pygame
from utils.game_constants import PLAYER_WIDTH, PIPE_HEIGHT, BASEY, PIPE_WIDTH, U_HIT_MASK, I_HIT_MASK, HITMASKS, \
    PLAYER_HEIGHT


def check_cresh(player, up_pipes, low_pipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = PLAYER_WIDTH
    player['h'] = PLAYER_HEIGHT

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return True
    else:

        player_rect = pygame.Rect(player['x'], player['y'],
                                  player['w'], player['h'])

        for uPipe, lPipe in zip(up_pipes, low_pipes):
            # upper and lower pipe rects
            up_pipe_rect = pygame.Rect(uPipe['x'], uPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            low_pipe_rect = pygame.Rect(lPipe['x'], lPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)

            # player and upper/lower pipe hitmasks
            p_hit_mask = HITMASKS['player'][pi]
            u_hit_mask = U_HIT_MASK
            l_hit_mask = I_HIT_MASK

            # if bird collided with upipe or lpipe
            up_collide = pixel_collision(player_rect, up_pipe_rect, p_hit_mask, u_hit_mask)
            low_collide = pixel_collision(player_rect, low_pipe_rect, p_hit_mask, l_hit_mask)

            if up_collide or low_collide:
                return True
    return False


def pixel_collision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False
