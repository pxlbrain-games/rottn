# -*- coding: utf-8 -*-

import cocos

class TestScene(cocos.scene.Scene):
    def __init__(self, text):
        super(TestScene, self).__init__()
        label = cocos.text.Label(
            text,
            font_name = 'Arial',
            font_size = 16,
            anchor_x = 'center',
            anchor_y = 'center'
        )
        label.position = 320, 240
        self.add(label)