# -*- coding: utf-8 -*-

import cocos
import bossfight.client.gameServiceConnection as gameServiceConnection
import bossfight.core.gameServiceProtocol as gsp
import subprocess
import sys

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
        for child in self.get_children(): child.visible = False
    
class ServerTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(ServerTestTextLayer(), name='text_layer')
        self.server_process = subprocess.Popen([sys.executable, '-m', 'bossfight.server'])
        self.connection = gameServiceConnection.GameServiceConnection(('localhost', 9999))
        self.schedule(self.update_text)
    
    def update_text(self, dt):
        for child in self.get('text_layer').get_children(): child.visible = False
        self.get('text_layer').get(str(self.connection.connection_status)).visible = True

    def on_exit(self):
        self.connection.close()
        self.server_process.terminate()
        super().on_exit()