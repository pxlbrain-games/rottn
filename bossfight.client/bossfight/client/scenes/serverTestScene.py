# -*- coding: utf-8 -*-

import subprocess
import cocos
from bossfight.client.config import Config
import bossfight.client.gameServiceConnection as gameServiceConnection

class ServerTestTextLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.add(cocos.text.Label(
            'Waiting for Server ...',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus.WaitingForServer))
        self.add(cocos.text.Label(
            'Connected',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus.Connected))
        self.add(cocos.text.Label(
            'Disconnected',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus.Disconnected))
        for child in self.get_children():
            child.visible = False

class ServerTestMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__('GameService Test')
        self.font_title.update({
            'font_size': 32,
            'bold': True
        })
        self.font_item.update({
            'font_size': 16
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        menu_items = [
            cocos.menu.MenuItem('Create Server', self.on_create_server),
            cocos.menu.MenuItem('Open Connection', self.on_open_connection),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out(),
            layout_strategy=cocos.menu.fixedPositionMenuLayout([
                (150, 160),
                (150, 130),
                (150, 100)
            ])
        )

    def on_create_server(self):
        if self.parent.server_process is None:
            self.parent.server_process = subprocess.Popen(Config().local_server_exec)

    def on_open_connection(self):
        if self.parent.connection is None:
            self.parent.connection = gameServiceConnection.GameServiceConnection(('localhost', 9999))

    def on_back(self):
        self.parent.end()

    def on_quit(self):
        self.on_back()

class ServerTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(ServerTestTextLayer(), name='text_layer')
        self.add(ServerTestMenuLayer(), name='menu_layer')
        self.server_process = None
        self.connection = None
        self.schedule(self.update_text)

    def update_text(self, dt):
        for child in self.get('text_layer').get_children():
            child.visible = False
        if not self.connection is None:
            self.get('text_layer').get(str(self.connection.connection_status)).visible = True

    def on_exit(self):
        if not self.connection is None:
            self.connection.disconnect()
        if not self.server_process is None:
            self.server_process.terminate()
        super().on_exit()
