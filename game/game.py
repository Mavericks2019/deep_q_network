import pygame
from game.pipe import Pipe
from game.player import Player
from game.base import Base
from utils.game_constants import PLAYER_HEIGHT, PLAYER_WIDTH, PIPE_WIDTH, PLAYER_INDEX_GEN, BASEY, SCREEN, IMAGE, \
    FPSCLOCK, FPS
from utils.functions import check_cresh


class Game(Pipe, Player, Base):
    def __init__(self):
        Pipe.__init__(self)
        Player.__init__(self)
        Base.__init__(self)
        self.score = self.playerIndex = self.loopIter = 0

    def frame_step(self, input_actions):
        pygame.event.pump()
        reward = 0.1
        terminal = False
        self.input_check(input_actions)
        reward = self.score_check(reward)
        self.change_player_index()
        self.player_move()
        self.pipe_move()
        terminal, reward = self.check_crash(terminal, reward)
        self.draw_scripts()
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # print self.upperPipes[0]['y'] + PIPE_HEIGHT - int(BASEY * 0.2)
        return image_data, reward, terminal

    def input_check(self, input_actions):
        # check input actions
        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')
        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: flap the bird
        if input_actions[1] == 1:
            if self.playery > -2 * PLAYER_HEIGHT:
                self.playerVelY = self.playerFlapAcc
                self.playerFlapped = True
                # SOUNDS['wing'].play()

    def score_check(self, reward):
        # check for score
        player_mid_pos = self.playerx + PLAYER_WIDTH / 2
        for pipe in self.upperPipes:
            pipe_mid_pos = pipe['x'] + PIPE_WIDTH / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                self.score += 1
                # SOUNDS['point'].play()
                reward = 1
        return reward

    def change_player_index(self):
        # playerIndex basex change
        if (self.loopIter + 1) % 3 == 0:
            self.playerIndex = next(PLAYER_INDEX_GEN)
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % self.baseShift)

    def player_move(self):
        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
        self.playery += min(self.playerVelY, BASEY - self.playery - PLAYER_HEIGHT)
        if self.playery < 0:
            self.playery = 0

    def pipe_move(self):
        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX
        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upperPipes[0]['x'] < 5:
            new_pipe = Pipe.get_random_pipe()
            self.upperPipes.append(new_pipe[0])
            self.lowerPipes.append(new_pipe[1])
        # remove first pipe if its out of the screen
        if self.upperPipes[0]['x'] < -PIPE_WIDTH:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

    def check_crash(self, terminal, reward):
        # check if crash here
        is_crash = check_cresh({'x': self.playerx, 'y': self.playery,
                               'index': self.playerIndex},
                               self.upperPipes, self.lowerPipes)
        if is_crash:
            # SOUNDS['hit'].play()
            # SOUNDS['die'].play()
            terminal = True
            self.__init__()
            reward = -1
            return terminal, reward
        else:
            return terminal, reward

    def draw_scripts(self):
        # draw sprites
        SCREEN.blit(IMAGE['background'], (0, 0))
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            SCREEN.blit(IMAGE['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGE['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGE['base'], (self.basex, BASEY))
        # print score so player overlaps the score
        # showScore(self.score)
        SCREEN.blit(IMAGE['player'][self.playerIndex],
                    (self.playerx, self.playery))
