# -*- coding: utf-8 -*-

import pygase.shared
import pygase.server

class BFGameLoop(pygase.server.GameLoop):
    '''
    Subclasses the GameLoop from the PyGaSe package and defines server-side
    game logic.
    '''

    def on_join(self, player_id, update):
        '''
        Initial assignments for when a new player joins the game.
        '''
        update.players[player_id]['position'] = (0, 0)
        update.players[player_id]['velocity'] = (0, 0)
        update.players[player_id]['direction'] = (0, 1)

    def handle_activity(self, activity: pygase.shared.ClientActivity, update, dt):
        '''
        Handling of custom BossFight client activities, like player movement or actions.
        '''
        if activity.activity_type == pygase.shared.ActivityType.MovePlayer:
            player_id = activity.activity_data['player_id']
            position = activity.activity_data['position']
            velocity = activity.activity_data['velocity']
            direction = activity.activity_data['direction']
            update.players = {
                player_id: {
                    'position': position,
                    'velocity': velocity,
                    'direction': direction
                }
            }

    def update_game_state(self, update, dt):
        '''
        BossFight game state update. Simulates enemies and game world objects.
        '''
        
