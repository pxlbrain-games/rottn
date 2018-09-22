# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from pyglet.window import NoSuchScreenModeException
import bossfight.client.config as config
import bossfight.client.server_manager as server_manager
from bossfight.client.scenes.serverTestScene import ServerTestScene
from bossfight.client.scenes.levelScene import LevelScene

class MainMenuScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.open_main_menu()

    def open_test_level_menu(self):
        self.add(TestLevelMenuLayer())

    def open_options_menu(self):
        self.add(OptionsMenuLayer())

    def open_main_menu(self):
        self.add(MainMenuLayer())

class MainMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='BossFight')
        self.font_title.update({
            'font_size': 128,
            'bold': True
        })
        self.font_item.update({
            'font_size': 64
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        menu_items = [
            cocos.menu.MenuItem('Test Level', self.on_test_level),
            cocos.menu.MenuItem('Test Server', self.on_test_server),
            cocos.menu.MenuItem('Options', self.on_options),
            cocos.menu.MenuItem('Quit', self.on_quit)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out()
        )

    def on_test_level(self):
        self.parent.open_test_level_menu()
        self.kill()

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
            'font_size': 64,
            'bold': True
        })
        self.font_item.update({
            'font_size': 32
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        self.resolutions = ['854x480', '1280x720', '1600x900', '1920x1080']
        current_resolution = [
            idx for idx, value in enumerate(self.resolutions) \
            if value == str(config.get.screen_mode['width']) + 'x' \
            + str(config.get.screen_mode['height'])
        ][0]
        menu_items = [
            cocos.menu.MultipleMenuItem(
                'Resolution: ', self.on_resolution, self.resolutions, current_resolution
            ),
            cocos.menu.ToggleMenuItem(
                'Fullscreen: ', self.on_fullscreen, config.get.screen_mode['fullscreen']
            ),
            cocos.menu.MenuItem('Revert to default', self.on_default),
            cocos.menu.MenuItem('Apply', self.on_apply),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out()
        )

    def on_resolution(self, index):
        width_height = self.resolutions[index].split('x')
        config.get.screen_mode['width'] = int(width_height[0])
        config.get.screen_mode['height'] = int(width_height[1])

    def on_fullscreen(self, fullscreen):
        config.get.screen_mode['fullscreen'] = bool(fullscreen)

    def on_default(self):
        config.revert_to_default()
        self.parent.open_options_menu()
        self.kill()

    def on_apply(self):
        try:
            director.window.set_fullscreen(
                fullscreen=config.get.screen_mode['fullscreen'],
                width=config.get.screen_mode['width'],
                height=config.get.screen_mode['height']
            )
            config.save()
        except NoSuchScreenModeException:
            config.load()
            self.parent.open_options_menu()
            self.kill()

    def on_back(self):
        config.load()
        self.parent.open_main_menu()
        self.kill()

    def on_quit(self):
        self.on_back()

class TestLevelMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='Options')
        self.font_title.update({
            'font_size': 64,
            'bold': True
        })
        self.font_item.update({
            'font_size': 32
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        self.player_name = 'Bob Host'
        self.selected_connection_address = (
            server_manager.get_available_ip_addresses()[0],
            0
        )
        menu_items = [
            cocos.menu.EntryMenuItem(
                label='Player Name: ',
                callback_func=self.on_player_name,
                value=self.player_name,
                max_length=15
            ),
            cocos.menu.EntryMenuItem(
                label='IP: ',
                callback_func=self.on_selected_ip_address,
                value=self.selected_connection_address[0],
                max_length=16
            ),
            cocos.menu.EntryMenuItem(
                label='Port: ',
                callback_func=self.on_selected_port,
                value=str(self.selected_connection_address[1]),
                max_length=5
            ),
            cocos.menu.MenuItem('Start on new Server', self.on_start_new_server),
            cocos.menu.MenuItem('Join Server', self.on_join_server),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out()
        )

    def on_player_name(self, new_value):
        self.player_name = new_value

    def on_start_new_server(self):
        pid = server_manager.run_server(
            ip_address=self.selected_connection_address[0],
            port=self.selected_connection_address[1]
        )
        self.on_back()
        director.push(LevelScene(
            server_address=server_manager.get_server_address(pid),
            local_player_names=[self.player_name]
        ))

    def on_selected_ip_address(self, new_value):
        self.selected_connection_address = (
            new_value,
            self.selected_connection_address[1]
        )

    def on_selected_port(self, new_value):
        try:
            self.selected_connection_address = (
                self.selected_connection_address[0],
                int(new_value)
            )
        except ValueError:
            pass

    def on_join_server(self):
        self.on_back()
        director.push(LevelScene(
            server_address=self.selected_connection_address,
            local_player_names=[self.player_name]
        ))

    def on_back(self):
        config.load()
        self.parent.open_main_menu()
        self.kill()

    def on_quit(self):
        self.on_back()
