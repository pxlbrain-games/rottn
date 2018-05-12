# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from bossfight.client.scenes.serverTestScene import ServerTestScene

class MainMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='BossFight')
        self.font_title.update({
            'font_size': 64,
            'bold': True
        })
        self.font_item.update({
            'font_size': 32
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255,255,255,255)
        })
        menu_items = [
            cocos.menu.MenuItem('Test Server', self.on_test_server),
            cocos.menu.MenuItem('Options', self.on_options),
            cocos.menu.MenuItem('Quit', self.on_quit)
        ]
        self.create_menu(menu_items, cocos.menu.zoom_in(), cocos.menu.zoom_out())#, cocos.menu.shake())
    
    def on_test_server(self):
        director.push(ServerTestScene())
    
    def on_options(self):
        #self.visible = False
        self.pause()
    
    def on_quit(self):
        self.parent.end()

class MainMenuScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__(MainMenuLayer())