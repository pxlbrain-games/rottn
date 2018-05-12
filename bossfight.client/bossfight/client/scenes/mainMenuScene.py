# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from bossfight.client.scenes.serverTestScene import ServerTestScene


class MainMenuScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.open_main_menu()
    
    def open_options_menu(self):
        self.add(OptionsMenuLayer())
    
    def open_main_menu(self):
        self.add(MainMenuLayer())

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
        self.parent.open_options_menu()
        self.kill()
    
    def on_quit(self):
        self.parent.end()

class OptionsMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='Options')
        self.font_title.update({
            'font_size': 32,
            'bold': True
        })
        self.font_item.update({
            'font_size': 16
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255,255,255,255)
        })
        self.resolutions = ['640x480', '1024x720', '1920x1080']
        self.fullscreen = False
        menu_items = [
            cocos.menu.MultipleMenuItem('Resolution: ', self.on_resolution, self.resolutions, 0),
            cocos.menu.ToggleMenuItem('Fullscreen: ', self.on_fullscreen, self.fullscreen),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(menu_items, cocos.menu.zoom_in(), cocos.menu.zoom_out())
    
    def on_resolution(self, resolution):
        pass
    
    def on_fullscreen(self, fullscreen):
        pass

    def on_back(self):
        self.parent.open_main_menu()
        self.kill()