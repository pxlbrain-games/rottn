# -*- coding: utf-8 -*-

import cocos
import pyglet
import pygase.shared
import pygase.client
import bossfight.client.server_manager as server_manager

class GameLoopTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(FireballLayer())
        if not server_manager.get_running_processes():
            self.server_process = server_manager.run_server()
        else:
            self.server_process = server_manager.get_running_processes()[0]
        self.connection = pygase.client.Connection(
            server_address=(
                server_manager.get_ip_address(self.server_process),
                server_manager.get_port(self.server_process)
            )
        )

    def on_exit(self):
        for child in self.get_children():
            child.kill()
        self.connection.disconnect()
        server_manager.shutdown(self.server_process)

class FireballLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        image = pyglet.resource.image('fireball.png')
        image_seq = pyglet.image.ImageGrid(image, 1, 4)
        self.fireball = cocos.sprite.Sprite(
            image=image_seq.get_animation(0.1),
            position=(960, 540),
            scale=3.0
        )
        self.add(self.fireball)
        self.schedule(self.update_position)

    def update_position(self, dt):
        self.fireball.position = (
            self.fireball.position[0],
            540 + self.parent.connection.game_state.test_pos*400
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.parent.connection.post_client_activity(
            pygase.shared.toggle_pause_activity(self.parent.connection.game_state)
        )
