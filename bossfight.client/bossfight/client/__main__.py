# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client.scenes.mainMenuScene import MainMenuScene

director.init()

# Run bossfight.server and then run the client on another terminal

director.run(MainMenuScene())