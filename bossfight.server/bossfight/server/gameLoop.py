# -*- coding: utf-8 -*-
'''
This module handles the game logic, that is to be simulated by the server.
A game loop takes a *SharedGameState* and will update it according to the game logic
defined in it's update cycle, as long as the *game_status* is not *Paused*.
'''

import threading
import time
import math
#from bossfight.server.gameService import GameService
from bossfight.core.sharedGameData import GameStatus, SharedGameState, SharedGameStateUpdate, ActivityType, ClientActivity

UPDATE_CACHE_SIZE = 100

class GameLoop:
    '''
    Class that can update a shared game state by running a game logic simulation thread.
    It must be passed a *SharedGameState* and a list of *ClientActivity*s from the
    *GameService* object which owns the *GameLoop*.

    Currently it only simulates a sine signal in the shared game state attribute *test_pos*.
    '''
    def __init__(self, shared_game_state: SharedGameState, client_activity_queue: list):
        self.shared_game_state = shared_game_state
        self.client_activity_queue = client_activity_queue
        self.state_update_cache = []
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
            # Handle client activities first
            activities_to_handle = self.client_activity_queue[:5]
            # Get first 5 activitys in queue
            for activity in activities_to_handle:
                self._handle_activity(activity)
                del self.client_activity_queue[0]
                # Should be safe, otherwise use *remove(activity)*
            # Create update object and fill it with all necessary changes
            ### SIMULATING A SINE FOR TESTING
            update = SharedGameStateUpdate(self.shared_game_state.time_order + 1)
            update.test_pos = math.sin(2.5*t)
            # Add the update to the game state and cache it for the clients
            self.shared_game_state += update
            self.cache_state_update(update)
            dt = time.time() - t
            time.sleep(max(self.update_cycle_interval-dt, 0))

    def _handle_activity(self, activity: ClientActivity):
        pass
        #if activity.activity_type == ActivityType().PauseGame:
        #    self.pause()
        #elif activity.activity_type == ActivityType().ResumeGame:
        #    self.start()

    def cache_state_update(self, state_update: SharedGameStateUpdate):
        self.state_update_cache.append(state_update)
        if len(self.state_update_cache) > UPDATE_CACHE_SIZE:
            self.state_update_cache = self.state_update_cache[1:]
