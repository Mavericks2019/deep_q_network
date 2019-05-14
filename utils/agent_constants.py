# Hyper Parameters:
FRAME_PER_ACTION = 1
GAMMA = 0.99  # decay rate of past observations
OBSERVE = 100.  # timesteps to observe before training
EXPLORE = 200000.  # frames over which to anneal epsilon
FINAL_EPSILON = 0  # 0.001 # final value of epsilon
INITIAL_EPSILON = 0  # 0.01 # starting value of epsilon
REPLAY_MEMORY = 50000  # number of previous transitions to remember
BATCH_SIZE = 32  # size of minibatch
UPDATE_TIME = 100
