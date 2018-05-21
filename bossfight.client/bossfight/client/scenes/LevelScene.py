# -*- coding: utf-8 -*-

import random
import cocos
#from pyglet.window import mouse
import pyglet
#from cocos.director import director
import bossfight.client.serverManager as serverManager
import bossfight.client.gameServiceConnection as gameServiceConnection
from bossfight.core.sharedGameData import PlayerAction, ActionType

class LevelScene(cocos.scene.Scene):
    '''
    Base class for alls kinds of ingame levels. It provides access to
    the level coordinate space, let's you add ingame objects like
    characters to the level, manages controls and HUD etc.
    '''

    def __init__(self):
        super().__init__()
        self.scrolling_manager = cocos.layer.ScrollingManager(
            viewport=cocos.rect.Rect(0, 0, 1920, 1080)
        )
        self.add(self.scrolling_manager)
        self.scrolling_manager.add(
            LevelLayer()
        )

class LevelLayer(cocos.layer.ScrollableLayer):
    '''
    Layer that contains the actual level itself and everything in it.
    '''

    is_event_handler = True

    def __init__(self):
        super().__init__()
        ### floor for testing!
        self.iso_map = create_iso_map(
            dimensions=(40, 30),
            origin=(-1000, -700)
        )
        self.add(self.iso_map)
        image = pyglet.resource.image('fireball.png')
        image_seq = pyglet.image.ImageGrid(image, 1, 4)
        self.fireball = cocos.sprite.Sprite(
            image=image_seq.get_animation(0.1),
            position=(100, 100),
            scale=3.0
        )
        self.add(self.fireball)
        self.fireball.velocity = (0, 0)
        self.keys_pressed = []
        self.fireball.do(cocos.actions.Move())
        self.schedule(self.update_fireball)

    def update_fireball(self, dt):
        velocity = cocos.euclid.Vector2(0, 0)
        if 'UP' in self.keys_pressed and 'DOWN' not in self.keys_pressed:
            velocity += (0, 1)
        if 'DOWN' in self.keys_pressed and 'UP' not in self.keys_pressed:
            velocity -= (0, 1)
        if 'RIGHT' in self.keys_pressed and 'LEFT' not in self.keys_pressed:
            velocity += (1, 0)
        if 'LEFT' in self.keys_pressed and 'RIGHT' not in self.keys_pressed:
            velocity -= (1, 0)
        velocity.normalize()
        velocity *= 300
        self.fireball.velocity = velocity.xy
        self.parent.set_focus(
            self.fireball.position[0],
            self.fireball.position[1]
        )

    def on_key_press(self, key, modifier):
        if key == pyglet.window.key.UP:
            self.keys_pressed.append('UP')
        if key == pyglet.window.key.DOWN:
            self.keys_pressed.append('DOWN')
        if key == pyglet.window.key.LEFT:
            self.keys_pressed.append('LEFT')
        if key == pyglet.window.key.RIGHT:
            self.keys_pressed.append('RIGHT')

    def on_key_release(self, key, modifier):
        if key == pyglet.window.key.UP:
            self.keys_pressed.remove('UP')
        if key == pyglet.window.key.DOWN:
            self.keys_pressed.remove('DOWN')
        if key == pyglet.window.key.LEFT:
            self.keys_pressed.remove('LEFT')
        if key == pyglet.window.key.RIGHT:
            self.keys_pressed.remove('RIGHT')

def create_iso_map(dimensions, origin):
    image = pyglet.resource.image('iso_floor_tiles.png')
    image_grid = pyglet.image.ImageGrid(image, 8, 4)
    batch = cocos.batch.BatchNode()
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            batch.add(cocos.sprite.Sprite(
                image=image_grid[random.randint(0, 31)],
                position=(
                    origin[0] + column*128 + (0 if row%2 == 0 else 1)*64,
                    origin[1] + row*32
                ),
                scale=2.0
            ))
    return batch
