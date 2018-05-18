# -*- coding: utf-8 -*-
'''
Game logic
'''

import threading

class GameLoop:
    def __init__(self, shared_game_state):
        self.shared_game_state = shared_game_state
        self._game_loop_thread = threading.Thread()
        self.update_cycle_interval = 0.03

    def _update_cycle(self):
        pass
