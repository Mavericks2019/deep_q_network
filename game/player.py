from utils.game_constants import SCREENHEIGHT, SCREENWIDTH, PLAYER_HEIGHT


class Player:
    def __init__(self):
        self.playerx = int(SCREENWIDTH * 0.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.playerVelY = 0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerFlapAcc = -7  # players speed on flapping
        self.playerFlapped = False  # True when player flaps
