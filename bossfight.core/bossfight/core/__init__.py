# -*- coding: utf-8 -*-
'''
This package defines the shared game data, most importantly the initial shared GameState and
custom client activities for the PyGaSe game server.
'''

import pygase.shared

SHARED_GAME_STATE = pygase.shared.GameState()
SHARED_GAME_STATE.test_t = 0
SHARED_GAME_STATE.test_pos = 0

pygase.shared.ActivityType.add_type('MovePlayer')