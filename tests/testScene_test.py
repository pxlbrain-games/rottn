# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(\
                os.path.dirname(__file__), '..\\bossfight.client')))
from cocos.director import director
from bossfight.client import testScene

director.init()

def test_testScene():
    assert len(testScene.TestScene().children) == 1