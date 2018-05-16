# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene
import bossfight.client.config as config

director.init(
    caption='BossFight',
    fullscreen=False,
    width=1920,
    height=1080
)
director.window.set_fullscreen(
    fullscreen=config.get.screen_mode['fullscreen'],
    width=config.get.screen_mode['width'],
    height=config.get.screen_mode['height']
)
director.show_FPS = True

# Run bossfight.server and then run the client on another terminal

director.run(MainMenuScene())
