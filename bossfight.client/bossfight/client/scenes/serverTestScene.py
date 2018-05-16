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
        entry_text = 'Server ' + str(ServerListEntryNode.entry_counter) + ' - ' \
                   + 'PID: ' + str(process_id) + '\n' \
                   + 'IP Address: ' + server_address[0] + ':' + str(server_address[1])
        super().__init__(
            text=entry_text,
            position=(init_position[0], init_position[1]-entry_number*160),
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

class ServerListLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.add(
            cocos.text.Label(
                'Server List',
                position=(650, 850),
                font_name='Arial',
                font_size=48,
                anchor_x='left',
                anchor_y='bottom'
            )
        )

    def add_entry(self, ip_address, port, pid):
        self.add(
            ServerListEntryNode(
                server_address=(ip_address, port),
                process_id=pid,
                init_position=(650, 800),
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
        menu_items = [
            cocos.menu.MenuItem('Create Server', self.on_create_server),
            cocos.menu.MenuItem('Open Connection', self.on_open_connection),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out(),
            layout_strategy=cocos.menu.fixedPositionMenuLayout([
                (300, 900),
                (300, 850),
                (300, 800)
            ])
        )

    def on_create_server(self):
        #if self.parent.server_process is None:
        #    cmd = config.get.local_server_exec.copy()
        #    cmd.extend(['localhost', '9999'])
        #    self.parent.server_process = subprocess.Popen(
        #        cmd,
        #        stdout=subprocess.PIPE
        #    )
        #    ip_address = str(self.parent.server_process.stdout.readline(), 'utf-8').strip()
        #    port = int(self.parent.server_process.stdout.readline())
        pid = serverManager.run_server()
        ip_address = serverManager.get_ip_address(pid)
        port = serverManager.get_port(pid)
        self.parent.get('server_list').add_entry(
            ip_address,
            port,
            pid#self.parent.server_process.pid
        )

    def on_open_connection(self):
        if self.parent.connection is None:
            self.parent.connection = gameServiceConnection.GameServiceConnection(('localhost', 9999))

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
        #self.server_process = None
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
        #if not self.server_process is None:
        #    self.server_process.terminate()
        for pid in serverManager.get_running_processes():
            serverManager.shutdown(pid)
        super().on_exit()
