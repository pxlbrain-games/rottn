# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
import bossfight.client.testScene as testScene

director.init()

testScene = testScene.TestScene()
director.run(testScene)