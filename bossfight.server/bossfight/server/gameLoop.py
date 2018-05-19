# -*- coding: utf-8 -*-
'''
This module handles the game logic, that is to be simulated by the server.
A game loop takes a *SharedGameState* and will update it according to the game logic
defined in it's update cycle, as long as the *game_status* is not *Paused*.
'''

import threading
import time
import math
from bossfight.core.sharedGameData import GameStatus, SharedGameState, ActionType, PlayerAction

class GameLoop:
    '''
    Class that can update a shared game state by running a game logic simulation thread.
    It must be passed a *SharedGameState* and a list of *PlayerAction*s from the
    *GameService* object which owns the GameLoop.

    Currently it only simulates a sine signal in the shared game state attribute *test_pos*.
    '''
    def __init__(self, shared_game_state: SharedGameState, player_action_queue: list):
        self.shared_game_state = shared_game_state
        self.player_action_queue = player_action_queue
        self._game_loop_thread = threading.Thread()
        self.update_cycle_interval = 0.03

    def start(self):
        '''
        Starts a thread that updates the shared game state every *update_cycle_interval* seconds.
        Use this to restart a paused game.
        '''
        if not self._game_loop_thread.is_alive():
            self._game_loop_thread = threading.Thread(target=self._update_cycle)
            self.shared_game_state.game_status = GameStatus().Active
            self._game_loop_thread.start()

    def pause(self):
        '''
        Stops the game loop until *start()* is called.
        If the game loop is not currently running does nothing.
        '''
        self.shared_game_state.game_status = GameStatus().Paused

    def _update_cycle(self):
        dt = self.update_cycle_interval
        while not self.shared_game_state.is_paused():
            t = time.time()
            # Handle player actions first
            actions_to_handle = self.player_action_queue[:5] # Get first 5 actions in queue
            for action in actions_to_handle:
                self._handle_action(action)
                del self.player_action_queue[0] # Should be safe, otherwise use *remove(action)*
            ### SIMULATING A SINE FOR TESTING
            self.shared_game_state.test_pos += math.cos(2.5*t)*max(self.update_cycle_interval, dt)
            # It is important that the game loop manages time ordering
            self.shared_game_state.time_order += 1
            dt = time.time() - t
            time.sleep(max(self.update_cycle_interval-dt, 0))

    def _handle_action(self, action: PlayerAction):
        pass
        #if action.action_type == ActionType().PauseGame:
        #    self.pause()
        #elif action.action_type == ActionType().ResumeGame:
        #    self.start()
