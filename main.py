import cv2
import numpy as np
from game.game import Game
from utils.img_functions import reshape
from agent.agent import Agent


def _play(game, action):
    # action[0] == 1: do nothing
    # action[1] == 1: flap the bird
    image_data, reward, terminal = game.frame_step(action)
    image_data = reshape(image_data)
    return image_data, reward, terminal


def play():
    # Step 1: init BrainDQN
    actions = 2
    agent = Agent(actions)
    game = Game()
    # Step 3: play game
    # Step 3.1: obtain init state
    action_init = np.array([1, 0])  # do nothing
    image_data, reward, terminal = _play(game, action_init)
    ret, image_data = cv2.threshold(image_data, 1, 255, cv2.THRESH_BINARY)
    agent.set_init_state(image_data)
    while True:
        action = agent.get_action()
        image_data, reward, terminal = _play(game, action)
        agent.set_perception(image_data, action, reward, terminal)


def main():
    play()


if __name__ == '__main__':
    main()
