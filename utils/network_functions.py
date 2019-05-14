import numpy as np
import tensorflow as tf


def set_init_state(self, observation):
    self.currentState = np.stack((observation, observation, observation, observation), axis=2)


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.01, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding="SAME")


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


def create_network_weights(actions):
    w_conv1 = weight_variable([8, 8, 4, 32])
    w_conv2 = weight_variable([4, 4, 32, 64])
    w_conv3 = weight_variable([3, 3, 64, 64])
    w_fc1 = weight_variable([1600, 512])
    w_fc2 = weight_variable([512, actions])
    return w_conv1, w_conv2, w_conv3, w_fc1, w_fc2


def create_bias(actions):
    b_conv1 = bias_variable([32])
    b_conv2 = bias_variable([64])
    b_conv3 = bias_variable([64])
    b_fc1 = bias_variable([512])
    b_fc2 = bias_variable([actions])
    return b_conv1, b_conv2, b_conv3, b_fc1, b_fc2


def create_input_hidden_qvalue(actions):
    stateInput = tf.placeholder("float", [None, 80, 80, 4])

    # hidden layers
    w_conv1, w_conv2, w_conv3, w_fc1, w_fc2 = create_network_weights(actions)
    b_conv1, b_conv2, b_conv3, b_fc1, b_fc2 = create_bias(actions)
    h_conv1 = tf.nn.relu(conv2d(stateInput, w_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2, 2) + b_conv2)
    h_conv3 = tf.nn.relu(conv2d(h_conv2, w_conv3, 1) + b_conv3)
    h_conv3_flat = tf.reshape(h_conv3, [-1, 1600])
    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, w_fc1) + b_fc1)
    # Q Value layer
    QValue = tf.matmul(h_fc1, w_fc2) + b_fc2
    return stateInput, QValue, w_conv1, b_conv1, w_conv2, b_conv2, w_conv3, b_conv3, w_fc1, b_fc1, w_fc2, b_fc2
