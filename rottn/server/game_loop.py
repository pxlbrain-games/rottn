# -*- coding: utf-8 -*-

import sys
import math
import random
import tensorflow
import euclid3 as euclid
from pygase import GameStateMachine
from pygase.gamestate import GameStateUpdate, TO_DELETE
from rottn.core import character_bases
from rottn.server.ai import actors

GRAPH = None


class BFStateMachine(GameStateMachine):
    """
    Subclasses the GameLoop from the PyGaSe package and defines server-side
    game logic.
    """

    def __init__(self, game_state_store, server):
        super().__init__(game_state_store)
        self.server = server
        self.player_characters = {}
        self.npc_actors = {}
        test_enemy = actors.TestEnemyActor("Test Enemy")
        test_enemy.position = (200, 100)
        test_enemy.direction = (-1, 0)
        test_enemy.velocity = (-1 * actors.ENEMY_VELOCITY, 0)
        self.npc_actors[0] = test_enemy
        add_enemy = GameStateUpdate(
            self._game_state_store.get_game_state().time_order + 1,
            npcs={0: test_enemy.get_state()}
        )
        self._game_state_store.push_update(add_enemy)
        self.register_event_handler("JOIN", self.on_join)
        self.register_event_handler("MOVE", self.on_move)
        self.register_event_handler("LEAVE", self.on_leave)

        self.learn_counter = 0
        global GRAPH
        GRAPH = tensorflow.get_default_graph()

    def on_join(self, player_name, game_state, client_address, **kwargs):
        """
        Initial assignments for when a new player joins the game.
        """
        new_player = character_bases.PlayerCharacter(player_name)
        player_id = len(game_state.players)
        self.player_characters[player_id] = new_player
        self.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
        return {
            "players": {
                player_id: new_player.get_state()
            }
        }

    def on_leave(self, player_id, **kwargs):
        return {"players": {player_id: TO_DELETE}}

    def on_move(self, move_event_data, **kwargs):
        """
        Handling of custom ROTTN client activities, like player movement or actions.
        """
        return self.player_characters[move_event_data["player_id"]].on_move(move_event_data)

    def time_step(self, game_state, dt):
        """
        ROTTN game state update. Simulates enemies and game world objects.
        """
        done = False
        hit = False
        if 0 in self.player_characters.keys():
            r_player = euclid.Vector2(
                self.player_characters[0].position[0],
                self.player_characters[0].position[1],
            )
            r_enemy = euclid.Vector2(
                self.npc_actors[0].position[0], self.npc_actors[0].position[1]
            )
            r = r_player - r_enemy
            distance = r.magnitude()
            if distance > 900:
                done = True
                sys.stderr.write("Left arena\n")
            elif distance < 140 and self.npc_actors[0].is_attacking():
                d_enemy = euclid.Vector2(
                    self.npc_actors[0].direction[0], self.npc_actors[0].direction[1]
                )
                angle = r.angle(d_enemy)
                if angle < 1.4 or (distance < 50 and angle < 1.57):
                    hit = True
                    sys.stderr.write("Hit\n")

        global GRAPH
        with GRAPH.as_default():
            if 0 in self.player_characters.keys():
                self.npc_actors[0].observe_and_act(self.player_characters[0], done, hit)
                if self.learn_counter >= 68:
                    self.npc_actors[0]._agent.replay(66)
                    self.learn_counter = 0
                else:
                    self.learn_counter += 1
        update = {"npcs": {}}
        for npc_id, actor in self.npc_actors.items():
            if done or hit:
                rand_angle = random.random() * 2 * math.pi
                actor.position = (
                    r_player.x + 600 * math.sin(rand_angle),
                    r_player.y + 600 * math.cos(rand_angle),
                )
            else:
                update["npcs"][npc_id] = actor.update(dt)
        return update
