# -*- coding: utf-8 -*-

import pyglet.resource
from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene
import bossfight.client.config as config
import bossfight.client.server_manager as server_manager

director.init(
    caption='BossFight',
    fullscreen=False,
    width=1920,
    height=1080,
    vsync=False
)
pyglet.resource.path = ['resources/spritesheets', 'resources/spritesheets/isometric_hero']
pyglet.resource.reindex()
director.window.set_fullscreen(
    fullscreen=config.get.screen_mode['fullscreen'],
    width=config.get.screen_mode['width'],
    height=config.get.screen_mode['height']
)
director.show_FPS = True
director.run(MainMenuScene())

server_manager.clean_up()
