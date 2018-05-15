# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene
from bossfight.client.config import Config

config = Config()

director.init(
    caption='BossFight',
    fullscreen=False,
    width=1920,
    height=1080
)
director.window.set_fullscreen(
    fullscreen=config.screen_mode['fullscreen'],
    width=config.screen_mode['width'],
    height=config.screen_mode['height']
)
director.show_FPS = True

# Run bossfight.server and then run the client on another terminal

director.run(MainMenuScene())
