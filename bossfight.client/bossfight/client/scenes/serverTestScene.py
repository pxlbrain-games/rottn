# -*- coding: utf-8 -*-

import subprocess
import cocos
import bossfight.client.config as config
import bossfight.client.serverManager as serverManager
import bossfight.client.gameServiceConnection as gameServiceConnection

class ServerListEntryNode(cocos.text.Label):

    entry_counter = 1

    def __init__(self, server_address, process_id, init_position, entry_number):
        self.pid = process_id
        self.index = ServerListEntryNode.entry_counter
        entry_text = 'Server ' + str(self.index) + ' - ' \
                   + 'PID: ' + str(process_id) + '\n' \
                   + 'IP Address: ' + server_address[0] + ':' + str(server_address[1])
        super().__init__(
            text=entry_text,
            position=(init_position[0], init_position[1]-entry_number*140),
            width=600,
            height=120,
            multiline=True,
            font_name='Arial',
            font_size=32,
            anchor_x='left',
            anchor_y='top'
        )
        ServerListEntryNode.entry_counter += 1
        self.schedule(self.update)

    def update(self, dt):
        if not self.pid in serverManager.get_running_processes():
            self.kill()
            for entry in self.parent.get_children():
                if entry.__class__ == ServerListEntryNode and \
                  entry.index > self.index:
                    entry.do(cocos.actions.MoveBy((0, 140), 0.3))

class ServerListLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.add(
            cocos.text.Label(
                'Server List',
                position=(700, 850),
                font_name='Arial',
                font_size=48,
                anchor_x='left',
                anchor_y='bottom'
            )
        )
        for pid in serverManager.get_running_processes():
            self.add_entry(
                ip_address=serverManager.get_ip_address(pid),
                port=serverManager.get_port(pid),
                pid=pid
            )

    def add_entry(self, ip_address, port, pid):
        self.add(
            ServerListEntryNode(
                server_address=(ip_address, port),
                process_id=pid,
                init_position=(700, 800),
                entry_number=len(self.children)-1
            )
        )

class ServerTestTextLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.add(cocos.text.Label(
            'Waiting for Server ...',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus().WaitingForServer))
        self.add(cocos.text.Label(
            'Connected',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus().Connected))
        self.add(cocos.text.Label(
            'Disconnected',
            font_name='Arial',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            position=(320, 240)
            ), name=str(gameServiceConnection.ConnectionStatus().Disconnected))
        for child in self.get_children():
            child.visible = False

class ServerTestMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__('GameService Test')
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
        self.ip_addresses = serverManager.get_available_ip_addresses()
        self.selected_ip_idx = 0
        menu_items = [
            cocos.menu.MultipleMenuItem(
                label='IP: ',
                callback_func=self.on_ip_address,
                items=serverManager.get_available_ip_addresses(),
                default_item=self.selected_ip_idx
            ),
            cocos.menu.MenuItem('Create Server', self.on_create_server),
            #cocos.menu.MenuItem('Open Connection', self.on_open_connection),
            cocos.menu.MenuItem('Shutdown All', self.on_shutdown_all),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out(),
            layout_strategy=cocos.menu.fixedPositionMenuLayout([
                (350, 900),
                (350, 850),
                (350, 800),
                (350, 750)
            ])
        )

    def on_ip_address(self, selected_ip_idx):
        self.selected_ip_idx = selected_ip_idx

    def on_create_server(self):
        pid = serverManager.run_server(self.ip_addresses[self.selected_ip_idx])
        ip_address = serverManager.get_ip_address(pid)
        port = serverManager.get_port(pid)
        self.parent.get('server_list').add_entry(
            ip_address,
            port,
            pid
        )
    
    def on_shutdown_all(self):
        serverManager.clean_up()

    def on_open_connection(self):
        if self.parent.connection is None:
            self.parent.connection = \
                gameServiceConnection.GameServiceConnection(('localhost', 9999))

    def on_back(self):
        self.parent.end()

    def on_quit(self):
        self.on_back()

class ServerTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(ServerTestTextLayer(), name='text_layer')
        self.add(ServerTestMenuLayer(), name='menu_layer')
        self.add(ServerListLayer(), name='server_list')
        self.connection = None
        self.schedule(self.update_text)

    def update_text(self, dt):
        for child in self.get('text_layer').get_children():
            child.visible = False
        if not self.connection is None:
            self.get('text_layer').get(str(self.connection.connection_status)).visible = True

    def on_exit(self):
        if not self.connection is None:
            self.connection.disconnect()
        super().on_exit()
