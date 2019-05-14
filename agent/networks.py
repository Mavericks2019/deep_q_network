from utils.network_functions import create_input_hidden_qvalue


class Network:
    def __init__(self, actions):
        self.actions = actions
        self.stateInput, self.QValue, self.w_conv1, self.b_conv1, self.w_conv2, self.b_conv2, self.w_conv3, \
            self.b_conv3, self.w_fc1, self.b_fc1, self.w_fc2, self.b_fc2 = create_input_hidden_qvalue(self.actions)
