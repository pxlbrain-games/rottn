# -*- coding: utf-8 -*-

import math
import numpy
import euclid3 as euclid
import bossfight.core.character_bases as character_bases
import bossfight.server.ai.dqn as dqn

class TestEnemyActor(character_bases.NonPlayerCharacter):
    def __init__(self, name):
        super().__init__(name)
        self.action_space = ['TurnLeft', 'TurnRight', 'StraightAhead']
        self._agent = dqn.DQNAgent(4, 3)
        self._last_observation = None
        self._last_action = None
        self._state_update = dict()

    def update(self, npc_id, update, dt):
        if not hasattr(update, 'npcs'):
            update.npcs = dict()
        if self.velocity != (0, 0):
            self.position = (
                self.position[0] + self.velocity[0]*dt,
                self.position[1] + self.velocity[1]*dt
            )
            self._state_update.update({'position': self.position})
        update.npcs.update({npc_id: self._state_update.copy()})
        self._state_update.clear()

    def turn_by_angle(self, angle):
        turn = euclid.Matrix3.new_rotate(angle)
        self.direction = (turn*euclid.Vector2(self.direction[0], self.direction[1])).xy
        self.velocity = (turn*euclid.Vector2(self.velocity[0], self.velocity[1])).xy
        self._state_update.update({
            'velocity': self.velocity,
            'direction': self.direction
        })

    def observe_and_act(self, player: character_bases.Character, done=False):
        # observe current state
        r_self = euclid.Vector2(self.position[0], self.position[1])
        r_player = euclid.Vector2(player.position[0], player.position[1])
        r = r_player - r_self
        distance = r.magnitude()
        delta_distance = distance - self._last_observation[0][0] if self._last_observation is not None else 0
        angle = math.atan2(self.velocity[1], self.velocity[0]) - math.atan2(r.y, r.x)
        delta_angle = angle - self._last_observation[0][2] if self._last_observation is not None else 0
        observation = numpy.array([[distance, delta_distance, angle, delta_angle]], dtype=float)
        # calculate reward for last action and remember
        if self._last_action is not None:
            reward = 50.0/distance
            if done:
                reward -= 20.0 # penalty for loosing
            self._agent.remember(self._last_observation, self._last_action, reward, observation, done)
        # act
        action = self._agent.predict_best_action(observation)
        self.perform_action(self.action_space[action])
        # store stuff
        self._last_observation = observation
        self._last_action = action

    def perform_action(self, action):
        if action == 'TurnLeft':
            self.turn_by_angle(0.05)
        elif action == 'TurnRight':
            self.turn_by_angle(-0.05)