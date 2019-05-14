import random
from utils.game_constants import SCREENWIDTH, PIPE_HEIGHT, PIPEGAPSIZE, BASEY


class Pipe:
    def __init__(self):
        self.pipeVelX = -4
        new_pipe1 = Pipe.get_random_pipe()
        new_pipe2 = Pipe.get_random_pipe()
        self.upperPipes = [
            {'x': SCREENWIDTH, 'y': new_pipe1[0]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': new_pipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH, 'y': new_pipe1[1]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': new_pipe2[1]['y']},
        ]

    @staticmethod
    def get_random_pipe():
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gap_ys = [20, 30, 40, 50, 60, 70, 80, 90]
        index = random.randint(0, len(gap_ys) - 1)
        gap_y = gap_ys[index]

        gap_y += int(BASEY * 0.2)
        pipe_x = SCREENWIDTH + 10

        return [
            {'x': pipe_x, 'y': gap_y - PIPE_HEIGHT},  # upper pipe
            {'x': pipe_x, 'y': gap_y + PIPEGAPSIZE},  # lower pipe
        ]
