# -*- coding: utf-8 -*-

import math
import numpy
import euclid3 as euclid
import bossfight.core.character_bases as character_bases
import bossfight.server.ai.dqn as dqn

ATTACK_DURATION = 0.38
ENEMY_VELOCITY = 200

class TestEnemyActor(character_bases.NonPlayerCharacter):
    def __init__(self, name):
        super().__init__(name)
        self.action_space = ['TurnLeft', 'TurnRight', 'StraightAhead', 'Attack']
        self._agent = dqn.DQNAgent(4, 4, [0.33, 0.33, 0.33, 0.01])
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
        if self.is_attacking():
            self.attack_counter -= dt
            if self.attack_counter <= 0:
                self.attack_counter = 0
                self.velocity = (ENEMY_VELOCITY*euclid.Vector2(self.direction[0], self.direction[1])).xy
                self._state_update.update({'velocity': self.velocity})
            self._state_update.update({'attack_counter': self.attack_counter})
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

    def start_attack(self):
        self.attack_counter = ATTACK_DURATION
        self.velocity = (0, 0)
        self._state_update.update({
            'velocity': self.velocity,
            'attack_counter': self.attack_counter
        })

    def observe_and_act(self, player: character_bases.Character, done=False, hit=False):
        # observe current state
        r_self = euclid.Vector2(self.position[0], self.position[1])
        v_self = euclid.Vector2(self.velocity[0], self.velocity[1])
        r_player = euclid.Vector2(player.position[0], player.position[1])
        v_player = euclid.Vector2(player.velocity[0], player.velocity[1])
        r_rel = (r_player - r_self)
        v_rel = (v_player - v_self)
        n = euclid.Vector2(self.direction[0], self.direction[1])
        basis = [n, n.cross()]
        r = euclid.Vector2(r_rel.dot(basis[0]), r_rel.dot(basis[1]))
        v = euclid.Vector2(v_rel.dot(basis[0]), v_rel.dot(basis[1]))
        observation = numpy.array([[r.x, r.y, v.x, v.y]], dtype=float)
        # calculate reward for last action and remember
        if self._last_observation is not None:
            distance = r.magnitude()
            delta_distance = distance - self._last_observation[0][0]
            reward = 1.0/(distance + 0.02) - 10.0*delta_distance + 1/(r.angle(euclid.Vector2(0, 1)) + 0.04)
            if self.is_attacking() and not hit:
                reward -= 300.0
            elif hit:
                reward += 1500.0
            if done:
                reward -= 40.0 # penalty for going to far away
            self._agent.remember(self._last_observation, self._last_action, reward, observation, done)
        # act
        action = self._agent.predict_best_action(observation)
        self.perform_action(self.action_space[action])
        # store stuff
        self._last_observation = observation
        self._last_action = action

    def perform_action(self, action):
        if not self.is_attacking():
            if action == 'TurnLeft':
                self.turn_by_angle(0.05)
            elif action == 'TurnRight':
                self.turn_by_angle(-0.05)
            elif action == 'Attack':
                self.start_attack()
