# -*- coding: utf-8 -*-

import pygase.shared
import pygase.server
import bossfight.core.character_bases as character_bases
import bossfight.server.ai.actors as actors

class BFGameLoop(pygase.server.GameLoop):
    '''
    Subclasses the GameLoop from the PyGaSe package and defines server-side
    game logic.
    '''
    def __init__(self, server: pygase.server.Server):
        super().__init__(server)
        self.player_characters = {}
        self.npc_actors = {}
        test_enemy = actors.TestEnemyActor('Test Enemy')
        test_enemy.position = (200, 100)
        test_enemy.direction = (-1, 0)
        test_enemy.velocity = (-100, 0)
        self.npc_actors[0] = test_enemy
        self.server.game_state.npcs[0] = test_enemy.get_state()

        self.learn_counter = 0

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
        #self.npc_actors[0].turn_by_angle(1.5*dt)
        if 0 in self.player_characters.keys():
            self.npc_actors[0].observe_and_act(self.player_characters[0])
            if self.learn_counter >= 50:
                self.npc_actors[0]._agent.replay(32)
                self.learn_counter = 0
            else:
                self.learn_counter += 1
        for npc_id, actor in self.npc_actors.items():
            actor.update(npc_id, update, dt)
