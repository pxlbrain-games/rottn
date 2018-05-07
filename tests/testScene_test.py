# -*- coding: utf-8 -*-

from cocos.director import director
from bossfight.client import testScene

director.init()

def test_testScene():
    assert len(testScene.TestScene('test').children) == 1