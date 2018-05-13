# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene
from bossfight.client.config import Config

config = Config()

director.init(
    fullscreen=config.fullscreen,
    width=config.screen_resolution['width'],
    height=config.screen_resolution['height']
)
director.show_FPS = True

# Run bossfight.server and then run the client on another terminal

director.run(MainMenuScene())
