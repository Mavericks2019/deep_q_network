import random
import numpy as np
import tensorflow as tf
from collections import deque
from agent.networks import Network
from utils.agent_constants import INITIAL_EPSILON, FRAME_PER_ACTION, FINAL_EPSILON, OBSERVE, EXPLORE, REPLAY_MEMORY, \
    BATCH_SIZE, GAMMA, UPDATE_TIME


class Agent:
    def __init__(self, actions):
        # init replay memory
        self.replayMemory = deque()
        # init some parameters
        self.time_step = 0
        self.epsilon = INITIAL_EPSILON
        self.actions = actions

        self.q_network = Network(actions)
        self.target_q_network = Network(actions)

        self.action_input, self.y_input, self.q_action, self.cost, self.train_step = self.create_training_method()

        self.session = tf.InteractiveSession()
        self.session.run(tf.initialize_all_variables())

        self.__copy_target_q_network()
        self.saver = tf.train.Saver()

        self.__saving_and_loading_networks()
        self.current_state = None

    def __copy_target_q_network(self):
        copy_target_q_network_operation = [self.target_q_network.w_conv1.assign(self.q_network.w_conv1),
                                           self.target_q_network.b_conv1.assign(self.q_network.b_conv1),
                                           self.target_q_network.w_conv2.assign(self.q_network.w_conv2),
                                           self.target_q_network.b_conv2.assign(self.q_network.b_conv2),
                                           self.target_q_network.w_conv3.assign(self.q_network.w_conv3),
                                           self.target_q_network.b_conv3.assign(self.q_network.b_conv3),
                                           self.target_q_network.w_fc1.assign(self.q_network.w_fc1),
                                           self.target_q_network.b_fc1.assign(self.q_network.b_fc1),
                                           self.target_q_network.w_fc2.assign(self.q_network.w_fc2),
                                           self.target_q_network.b_fc2.assign(self.q_network.b_fc2)]
        self.session.run(copy_target_q_network_operation)

    def __saving_and_loading_networks(self):
        self.session.run(tf.initialize_all_variables())
        checkpoint = tf.train.get_checkpoint_state("saved_networks")
        if checkpoint and checkpoint.model_checkpoint_path:
            self.saver.restore(self.session, checkpoint.model_checkpoint_path)
            print("Successfully loaded:", checkpoint.model_checkpoint_path)
        else:
            print("Could not find old network weights")

    def create_training_method(self):
        action_input = tf.placeholder("float", [None, self.actions])
        y_input = tf.placeholder("float", [None])
        q_action = tf.reduce_sum(tf.multiply(self.q_network.QValue, action_input), reduction_indices=1)
        cost = tf.reduce_mean(tf.square(y_input - q_action))
        train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)
        return action_input, y_input, q_action, cost, train_step

    def get_action(self):
        q_value = self.q_network.QValue.eval(feed_dict={self.q_network.stateInput: [self.current_state]})[0]
        action = np.zeros(self.actions)

        action_index = 0
        if self.time_step % FRAME_PER_ACTION == 0:
            if random.random() <= self.epsilon:
                action_index = random.randrange(self.actions)
                action[action_index] = 1
            else:
                action_index = np.argmax(q_value)
                action[action_index] = 1
        else:
            action[action_index] = 1  # do nothing
        # change episilon
        if self.epsilon > FINAL_EPSILON and self.time_step > OBSERVE:
            self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        return action

    def set_init_state(self, ing_data):
        self.current_state = np.stack((ing_data, ing_data, ing_data, ing_data), axis=2)

    def set_perception(self, image_data, action, reward, terminal):
        new_state = np.append(self.current_state[:, :, 1:], image_data, axis=2)
        self.replayMemory.append((self.current_state, action, reward, new_state, terminal))
        if len(self.replayMemory) > REPLAY_MEMORY:
            self.replayMemory.popleft()
        if self.time_step > OBSERVE:
            # Train the network
            self.train()
        if self.time_step <= OBSERVE:
            state = "observe"
        elif OBSERVE < self.time_step <= OBSERVE + EXPLORE:
            state = "explore"
        else:
            state = "train"
        print("TIMESTEP", self.time_step, "/ STATE", state, "/ EPSILON", self.epsilon)
        self.current_state = new_state
        self.time_step += 1

    def train(self):
        # Step 1: obtain random minibatch from replay memory
        mini_batch = random.sample(self.replayMemory, BATCH_SIZE)
        state_batch = [data[0] for data in mini_batch]
        action_batch = [data[1] for data in mini_batch]
        reward_batch = [data[2] for data in mini_batch]
        next_state_batch = [data[3] for data in mini_batch]
        # Step 2: calculate Y
        y_batch = []
        q_value_batch = self.target_q_network.QValue.eval(
            feed_dict={self.target_q_network.stateInput: next_state_batch})
        for i in range(0, BATCH_SIZE):
            terminal = mini_batch[i][4]
            if terminal:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + GAMMA * np.max(q_value_batch[i]))

        self.train_step.run(feed_dict={
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.q_network.stateInput: state_batch
        })
        # save network every 100000 iteration
        if self.time_step % 10000 == 0:
            self.saver.save(self.session, 'saved_networks/' + 'network' + '-dqn', global_step=self.time_step)

        if self.time_step % UPDATE_TIME == 0:
            self.__copy_target_q_network()
