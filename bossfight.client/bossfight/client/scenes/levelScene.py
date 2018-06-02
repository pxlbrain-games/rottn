# -*- coding: utf-8 -*-
'''
This is going to be the module containing the base level classes and components.
'''

import random
import cocos
import pyglet
import pygase.shared
import pygase.client
import bossfight.client.player_controls as player_controls
import bossfight.core.activities as activities

class LevelData:
    def __init__(self, server_address, scrolling_manager):
        self.connection = pygase.client.Connection(server_address, closed=True)
        self.scrolling_manager = scrolling_manager
        self.local_players = {}

class LevelScene(cocos.scene.Scene):
    '''
    Base class for alls kinds of ingame levels. It provides access to
    the level coordinate space, let's you add ingame objects like
    characters to the level, manages controls and HUD etc.

    Note: Currently this class implements a *Scene* that contains test content.
    '''

    def __init__(self, server_address, local_player_names):
        super().__init__()
        scrolling_manager = cocos.layer.ScrollingManager(
            viewport=cocos.rect.Rect(0, 90, 1920, 900)
        )
        self.add(scrolling_manager)
        self.level_data = LevelData(server_address, scrolling_manager)
        scrolling_manager.add(LevelLayer(self.level_data))
        self.add(HUDLayer(self.level_data))
        self.level_data.connection.connect()
        for name in local_player_names:
            self.level_data.connection.post_client_activity(
                pygase.shared.join_server_activity(name)
            )
        while len(self.level_data.local_players) < len(local_player_names):
            for player_id, player in self.level_data.connection.game_state.players.copy().items():
                if player_id not in self.level_data.local_players \
                  and player['name'] in local_player_names:
                    self.level_data.local_players[player_id] = player['name']

    def on_exit(self):
        self.level_data.connection.disconnect()
        super().on_exit()

class LevelLayer(cocos.layer.ScrollableLayer):
    '''
    Layer that contains the actual level itself and everything in it.
    '''

    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ### floor for testing!
        self.iso_map = create_iso_map(
            dimensions=(15, 20),
            origin=(-1000, 0)
        )
        self.add(self.iso_map)
        self.player_nodes = {}
        self.schedule(self.update_focus)
        self.schedule_interval(self.update_player_nodes, 0.03)
        self.schedule_interval(self.post_move_activity, 0.03)

    def update_focus(self, dt):
        try:
            focus_node = [node for player_id, node in self.player_nodes.items() \
                if player_id in self.level_data.local_players][0]
            self.level_data.scrolling_manager.set_focus(
                focus_node.position[0],
                focus_node.position[1]
            )
        except IndexError:
            pass

    def update_player_nodes(self, dt):
        for player_id, player in self.level_data.connection.game_state.players.copy().items():
            if player_id not in self.player_nodes:
                if player_id in self.level_data.local_players:
                    self.player_nodes[player_id] = player_controls.ControllableNode()
                    self.player_nodes[player_id].add(PlayerNode(player['name']))
                    self.add(self.player_nodes[player_id])
                else:
                    self.player_nodes[player_id] = PlayerNode(player['name'])
                    self.player_nodes[player_id].do(cocos.actions.Move())
                    self.add(self.player_nodes[player_id])
            self.player_nodes[player_id].position = player['position']
            if player_id not in self.level_data.local_players:
                self.player_nodes[player_id].velocity = player['velocity']


    def post_move_activity(self, dt):
        for player_id in self.level_data.local_players:
            self.level_data.connection.post_client_activity(
                activities.move_player_activity(
                    player_id=player_id,
                    position=self.player_nodes[player_id].position,
                    velocity=self.player_nodes[player_id].velocity,
                    time_order=self.level_data.connection.game_state.time_order
                )
            )

class PlayerNode(cocos.cocosnode.CocosNode):
    def __init__(self, name):
        super().__init__()
        self.name_label = cocos.text.Label(
            text=name,
            position=(0, 90),
            font_name='Arial',
            font_size=24,
            anchor_x='center',
            anchor_y='center'
        )
        image = pyglet.resource.image('fireball.png')
        image_seq = pyglet.image.ImageGrid(image, 1, 4)
        self.fireball = cocos.sprite.Sprite(
            image=image_seq.get_animation(0.1),
            scale=3.0
        )
        self.add(self.name_label),
        self.add(self.fireball)

class HUDLayer(cocos.layer.Layer):

    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ip = level_data.connection.server_address[0]
        port = str(level_data.connection.server_address[1])
        connection_text = 'Server Address: ' + ip + ':' + port
        connection_label = cocos.text.Label(
            text=connection_text,
            position=(1920, 1080),
            font_name='Arial',
            font_size=24,
            anchor_x='right',
            anchor_y='top'
        )
        self.add(connection_label)
        self.connection_status_texts = [
            'Connected',
            'Waiting for Server ...',
            'Disconnnected'
        ]
        self.connection_status_label = cocos.text.Label(
            text=self.connection_status_texts[
                level_data.connection.connection_status-1
            ] + ' - ' + \
            'Latency: ' + str(int(level_data.connection.latency)) + ' ms',
            position=(1920, 1050),
            font_name='Arial',
            font_size=24,
            anchor_x='right',
            anchor_y='top'
        )
        self.add(self.connection_status_label)
        self.player_list_label = cocos.text.Label(
            text='',
            position=(0, 1080),
            font_name='Arial',
            font_size=24,
            anchor_x='left',
            anchor_y='top'
        )
        self.add(self.player_list_label)
        self.schedule_interval(self.update_text, 0.5)

    def update_text(self, dt):
        self.connection_status_label.element.text = \
            self.connection_status_texts[
                self.level_data.connection.connection_status-1
            ] + ' - ' + \
            'Latency: ' + str(int(self.level_data.connection.latency)) + ' ms'
        player_list_text = ''
        for player_id, player in self.level_data.connection.game_state.players.copy().items():
            player_list_text += player['name']
            if player_id in self.level_data.local_players:
                player_list_text += ' (local)'
            player_list_text += ', '
        self.player_list_label.element.text = player_list_text[:-2]

def create_iso_map(dimensions, origin):
    image = pyglet.resource.image('iso_floor_tiles.png')
    image_grid = pyglet.image.ImageGrid(image, 8, 4)
    batch = cocos.batch.BatchNode()
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            batch.add(cocos.sprite.Sprite(
                image=image_grid[random.randint(0, 31)],
                position=(
                    origin[0] + column*64 + row*64,
                    origin[1] - column*32 + row*32
                ),
                scale=2.0
            ))
    return batch
