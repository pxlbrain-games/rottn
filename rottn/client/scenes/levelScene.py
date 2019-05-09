# -*- coding: utf-8 -*-
"""
This is going to be the module containing the base level classes and components.
"""

import random
import time
import pyglet
import cocos
from cocos.director import director
from pygase import Client
from pygase.connection import ConnectionStatus
from rottn.client.characters import character_nodes
from rottn.client.characters import character_animations


class LevelData:
    def __init__(self, scrolling_manager):
        self.scrolling_manager = scrolling_manager
        self.local_player_ids = set()
        self.client = Client()
        self.client.register_event_handler("PLAYER_CREATED", self.on_player_created)
        
    def on_player_created(self, player_id):
        self.local_player_ids.add(player_id)


class LevelScene(cocos.scene.Scene):
    """
    Base class for alls kinds of ingame levels. It provides access to
    the level coordinate space, let's you add ingame objects like
    characters to the level, manages controls and HUD etc.

    Note: Currently this class implements a *Scene* that contains test content.
    """

    def __init__(self, server_address, local_player_names):
        super().__init__()
        scrolling_manager = cocos.layer.ScrollingManager(
            viewport=cocos.rect.Rect(0, 90, 1920, 900)
        )
        self.add(scrolling_manager)
        director.window.set_exclusive_mouse(True)
        self.level_data = LevelData(scrolling_manager)
        self.level_data.client.connect_in_thread(server_address[1], server_address[0])
        scrolling_manager.add(LevelLayer(self.level_data))
        self.add(HUDLayer(self.level_data))
        for name in local_player_names:
            self.level_data.client.dispatch_event("JOIN", name, retries=3)

    def on_exit(self):
        director.window.set_exclusive_mouse(False)
        successful_leaves = set()
        for player_id in self.level_data.local_player_ids:
            self.level_data.client.dispatch_event(
                "LEAVE",
                player_id,
                ack_callback=lambda: successful_leaves.add(player_id),
                retries=3
            )
        while successful_leaves != self.level_data.local_player_ids:
            pass
        self.level_data.client.disconnect(shutdown_server=True)
        super().on_exit()


class LevelLayer(cocos.layer.ScrollableLayer):
    """
    Layer that contains the actual level itself and everything in it.
    """

    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ### floor for testing!
        self.iso_map = create_iso_map(dimensions=(30, 40), origin=(-2000, 0))
        self.add(self.iso_map)
        self.npc_nodes = dict()
        with self.level_data.client.access_game_state() as game_state:
            for npc_id, npc in game_state.npcs.items():
                self.npc_nodes[npc_id] = character_nodes.NPCNode(npc)
                self.add(self.npc_nodes[npc_id])
        self.player_nodes = dict()
        self.schedule(self.update_focus)
        self.schedule_interval(self.update_player_nodes, 0.02)
        self.schedule_interval(self.dispatch_move_events, 0.02)

    def update_focus(self, dt):
        try:
            focus_node = [
                node
                for player_id, node in self.player_nodes.items()
                if player_id in self.level_data.local_player_ids
            ][0]
            self.level_data.scrolling_manager.set_focus(
                focus_node.position[0], focus_node.position[1]
            )
        except IndexError:
            pass

    def update_player_nodes(self, dt):
        with self.level_data.client.access_game_state() as game_state:
            players_to_add = {
                p_id: p for p_id, p in game_state.players.items()
                if p_id not in self.player_nodes
            }
            players_to_remove = {
                    p_id: p_node for p_id, p_node in self.player_nodes.items()
                    if p_id not in game_state.players
                }
            for player_id, player in players_to_add.items():
                if player_id in self.level_data.local_player_ids:
                    self.player_nodes[player_id] = character_nodes.LocalPlayerNode(
                        player["name"]
                    )
                    self.player_nodes[player_id].push_handlers(on_attack=self.on_attack)
                    self.player_nodes[player_id].animated_character.push_handlers(on_animation_end=self.on_animation_end)
                    self.add(self.player_nodes[player_id])
                else:
                    self.player_nodes[player_id] = character_nodes.PlayerNode(player)
                    self.add(self.player_nodes[player_id])
            for player_id, player_node in players_to_remove.items():
                player_node.kill()
                del self.player_nodes[player_id]
            # Update movement on all nodes from external players.
            player_nodes_to_update = {
                p_id: p_node
                for (p_id, p_node) in self.player_nodes.items()
                if p_id not in self.level_data.local_player_ids
            }
            for player_id, player_node in player_nodes_to_update.items():
                player = game_state.players[player_id]
                player_node.move_state_update(player, dt)
            for npc_id, npc_node in self.npc_nodes.items():
                npc = game_state.npcs[npc_id]
                npc_node.move_state_update(npc, dt)
                npc_node.attack_counter = npc["attack_counter"]
                if (
                    npc_node.is_attacking()
                    and npc_node.animated_character.animation_state
                    != character_animations.AnimationState.Attacking
                ):
                    npc_node.animated_character.trigger_animation(
                        character_animations.AnimationState.Attacking
                    )

    def dispatch_move_events(self, dt):
        for player_id, player_node in self.player_nodes.items():
            if isinstance(player_node, character_nodes.LocalPlayerNode):
                self.level_data.client.dispatch_event("MOVE", player_node.get_move_event_data(player_id))

    def on_attack(self, player_node):
        if player_node.animated_character.animation_state != character_animations.AnimationState.Attacking:
            player_node.animated_character.trigger_animation(
                character_animations.AnimationState.Attacking
            )
            player_node.stop_movement()

    def on_animation_end(self, animated_character):
        animated_character.moving_parent.resume_movement()

class HUDLayer(cocos.layer.Layer):
    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ip_address = level_data.client.connection.remote_address[0]
        port = str(level_data.client.connection.remote_address[1])
        connection_text = "Server Address: " + ip_address + ":" + port
        connection_label = cocos.text.Label(
            text=connection_text,
            position=(1920, 1080),
            font_name="Arial",
            font_size=24,
            anchor_x="right",
            anchor_y="top",
        )
        self.add(connection_label)
        self.connection_status_label = cocos.text.Label(
            text=ConnectionStatus.get(level_data.client.connection.status)
            + " - "
            + "Latency: "
            + str(int(level_data.client.connection.latency))
            + " ms",
            position=(1920, 1050),
            font_name="Arial",
            font_size=24,
            anchor_x="right",
            anchor_y="top",
        )
        self.add(self.connection_status_label)
        self.player_list_label = cocos.text.Label(
            text="",
            position=(0, 1080),
            font_name="Arial",
            font_size=24,
            anchor_x="left",
            anchor_y="top",
        )
        self.add(self.player_list_label)
        self.schedule_interval(self.update_text, 0.5)

    def update_text(self, dt):
        self.connection_status_label.element.text = (
            ConnectionStatus.get(self.level_data.client.connection.status)
            + " - "
            + "Latency: "
            + str(int(self.level_data.client.connection.latency))
            + " ms"
        )
        player_list_text = ""
        with self.level_data.client.access_game_state() as game_state:
            for player_id, player in game_state.players.items():
                player_list_text += player["name"]
                if player_id in self.level_data.local_player_ids:
                    player_list_text += " (local)"
                player_list_text += ", "
        self.player_list_label.element.text = player_list_text[:-2]

def create_iso_map(dimensions, origin):
    image = pyglet.resource.image("iso_floor_tiles.png")
    image_grid = pyglet.image.ImageGrid(image, 8, 4)
    batch = cocos.batch.BatchNode()
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            batch.add(
                cocos.sprite.Sprite(
                    image=image_grid[random.randint(0, 31)],
                    position=(
                        origin[0] + column * 64 + row * 64,
                        origin[1] - column * 32 + row * 32,
                    ),
                    scale=2.0,
                )
            )
    return batch
