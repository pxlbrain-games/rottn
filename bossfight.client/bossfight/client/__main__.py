# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene

director.init()
director.show_FPS = True

# Run bossfight.server and then run the client on another terminal

director.run(MainMenuScene())