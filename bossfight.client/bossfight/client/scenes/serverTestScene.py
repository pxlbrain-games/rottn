# -*- coding: utf-8 -*-

import cocos
import bossfight.client.gameServiceConnection as gameServiceConnection
import bossfight.core.gameServiceProtocol as gsp

class ServerTestTextLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

    def on_enter(self):
        request = gsp.GameServicePackage(gsp.PackageType.GetSharedGameStateRequest)
        try:
            response = self.parent.test_connection.send_and_recv(request)
            if response.header.package_type == gsp.PackageType.GameServiceResponse and response.header.body_type == 'SharedGameState':
                self.add(cocos.text.Label(
                    'Connection successful!',
                    font_name='Arial',
                    font_size=16,
                    anchor_x='center',
                    anchor_y='center',
                    position=(320, 240)
                    ))
        except:
            self.add(cocos.text.Label(
                'Connection failed.',
                font_name='Arial',
                font_size=16,
                anchor_x='center',
                anchor_y='center',
                position=(320, 240)
                ))

class ServerTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(ServerTestTextLayer())
        self.test_connection=gameServiceConnection.UDPGameServiceConnection(('localhost', 9990))
