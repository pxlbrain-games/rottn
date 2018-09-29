# -*- coding: utf-8 -*-

import pygase.shared
import pygase.server
import bossfight.core.character_bases as character_bases
import bossfight.server.agents as agents

class BFGameLoop(pygase.server.GameLoop):
    '''
    Subclasses the GameLoop from the PyGaSe package and defines server-side
    game logic.
    '''
    def __init__(self, server: pygase.server.Server):
        super().__init__(server)
        self.player_characters = {}
        self.test_enemy = agents.TestEnemyAgent('Test Enemy')
        self.test_enemy.position = (400, -100)
        self.test_enemy.direction = (-1, 0)
        self.test_enemy.velocity = (-100, 0)
        self.server.game_state.npcs[0] = self.test_enemy.get_state()

    def on_join(self, player_id, update):
        '''
        Initial assignments for when a new player joins the game.
        '''
        new_player = character_bases.PlayerCharacter(update.players[player_id]['name'])
        update.players[player_id].update(new_player.get_state())
        self.player_characters[player_id] = new_player

    def handle_activity(self, activity: pygase.shared.ClientActivity, update, dt):
        '''
        Handling of custom BossFight client activities, like player movement or actions.
        '''
        if activity.activity_type == pygase.shared.ActivityType.MovePlayer:
            player = self.player_characters[activity.activity_data['player_id']]
            player.handle_move_activity(activity, update)

    def update_game_state(self, update, dt):
        '''
        BossFight game state update. Simulates enemies and game world objects.
        '''
        self.test_enemy.position = (
            self.test_enemy.position[0] + self.test_enemy.velocity[0]*dt,
            self.test_enemy.position[1] + self.test_enemy.velocity[1]*dt
        )
        update.npcs = {0: self.test_enemy.get_state()}
