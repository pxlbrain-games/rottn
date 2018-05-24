# -*- coding: utf-8 -*-

import random
import cocos
#from pyglet.window import mouse
import pyglet
#from cocos.director import director
import bossfight.client.playerControls as playerControls
#import bossfight.client.serverManager as serverManager
#import bossfight.client.gameServiceConnection as gameServiceConnection
#from bossfight.core.sharedGameData import PlayerAction, ActionType

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
        self.fireball = playerControls.ControllableNode(
            position=(100, 100)
        )
        self.fireball.add(cocos.sprite.Sprite(
            image=image_seq.get_animation(0.1),
            scale=3.0
        ))
        self.add(self.fireball)
        self.schedule(self.update_focus)

    def update_focus(self, dt):
        self.parent.set_focus(
            self.fireball.position[0],
            self.fireball.position[1]
        )

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
