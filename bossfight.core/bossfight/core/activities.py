# -*- coding: utf-8 -*-
'''
A module that defines some convenience functions for the creation
and handling of BossFight client activities.
'''

import pygase.shared 

def move_player_activity(player_id, position, velocity, time_order):
    '''
    Todo: Creates a ClientActivity for player movement.
    '''
    return pygase.shared.ClientActivity(
        activity_type=pygase.shared.ActivityType.MovePlayer,
        activity_data={
            'player_id': player_id,
            'position': position,
            'velocity': velocity,
            'time_order': time_order
        }
    )
