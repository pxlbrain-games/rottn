# -*- coding: utf-8 -*-

import random
from collections import deque
import numpy
import keras

# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, observation_size, action_size):
        self.observation_size = observation_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = keras.Sequential()
        model.add(keras.layers.Dense(24, input_dim=self.observation_size, activation='relu'))
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, observation, action, reward, next_observation, done):
        self.memory.append((observation, action, reward, next_observation, done))

    def predict_best_action(self, observation):
        if numpy.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        predicted_rewards = self.model.predict(observation)
        return numpy.argmax(predicted_rewards[0])  # returns action index

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for observation, action, reward, next_observation, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma*numpy.amax(self.model.predict(next_observation)[0])
            target_f = self.model.predict(observation)
            target_f[0][action] = target
            self.model.fit(observation, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
