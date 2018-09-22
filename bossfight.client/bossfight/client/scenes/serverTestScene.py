# -*- coding: utf-8 -*-

import cocos
from pyglet.window import mouse
from cocos.director import director
import pygase.client
import bossfight.client.server_manager as server_manager

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
            position=(init_position[0], init_position[1]-entry_number*145),
            width=600,
            height=120,
            multiline=True,
            font_name='Arial',
            font_size=27,
            anchor_x='left',
            anchor_y='top'
        )
        ServerListEntryNode.entry_counter += 1
        self.schedule(self.update)

    def update(self, dt):
        if not self.pid in server_manager.get_running_processes():
            self.kill()
            for entry in self.parent.get_children():
                if entry.__class__ == ServerListEntryNode and \
                  entry.index > self.index:
                    entry.do(cocos.actions.MoveBy((0, 140), 0.3))

class ServerListLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.add(
            cocos.text.Label(
                text='Server List',
                position=(650, 850),
                font_name='Arial',
                font_size=48,
                anchor_x='left',
                anchor_y='bottom'
            )
        )
        for pid in server_manager.get_running_processes():
            self.add_entry(
                ip_address=server_manager.get_ip_address(pid),
                port=server_manager.get_port(pid),
                pid=pid
            )

    def add_entry(self, ip_address, port, pid):
        self.add(
            ServerListEntryNode(
                server_address=(ip_address, port),
                process_id=pid,
                init_position=(600, 800),
                entry_number=len(self.children)-1
            )
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        x, y = director.get_virtual_coordinates(x, y)
        if 500 < x < 1170:
            upper_end = 800
            for child in self.get_children():
                if child.__class__ == ServerListEntryNode:
                    if upper_end > y > upper_end - 120:
                        server_manager.shutdown(child.pid)
                    upper_end -= 140

class ConnectionTextLayer(cocos.layer.Layer):
    def __init__(self, position, connection):
        super().__init__()
        self.add(cocos.text.Label(
            text='Waiting for Server ...',
            font_name='Arial',
            font_size=16,
            anchor_x='left',
            anchor_y='top',
            position=position
        ), name='status')
        self.add(cocos.text.Label(
            text='',
            font_name='Arial',
            font_size=16,
            anchor_x='left',
            anchor_y='top',
            position=(position[0]+250, position[1])
        ), name='latency')
        self.connection = connection
        self.schedule(self.update_text)

    def update_text(self, dt):
        if self.connection.is_connected():
            self.get('latency').visible = True
            self.get('latency').element.text = \
                'Latency: ' + str(int(self.connection.latency)) + ' ms'
            self.get('status').element.text = 'Connected'
        else:
            self.get('latency').visible = False
            if self.connection.is_waiting():
                self.get('status').element.text = 'Waiting for server ...'
            else:
                self.get('status').element.text = 'Disconnected'

class ConnectionListEntryNode(cocos.text.Label):

    entry_counter = 1

    def __init__(self, server_address, init_position, entry_number, connection):
        self.index = ConnectionListEntryNode.entry_counter
        entry_text = 'Connection ' + str(self.index) + '\n' \
                   + 'IP Address: ' + server_address[0] + ':' + str(server_address[1])
        super().__init__(
            text=entry_text,
            position=(init_position[0], init_position[1]-entry_number*160),
            width=600,
            height=120,
            multiline=True,
            font_name='Arial',
            font_size=27,
            anchor_x='left',
            anchor_y='top'
        )
        ConnectionListEntryNode.entry_counter += 1
        self.add(ConnectionTextLayer(
            position=(0, -100),
            connection=connection
        ), name='text_layer')
        self.connection = connection
        self.schedule(self.update)

    def update(self, dt):
        if not self.connection in self.parent.parent.connections:
            self.get('text_layer').kill()
            self.kill()
            for entry in self.parent.get_children():
                if entry.__class__ == ConnectionListEntryNode and \
                  entry.index > self.index:
                    entry.do(cocos.actions.MoveBy((0, 140), 0.3))

class ConnectionListLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.add(
            cocos.text.Label(
                text='Connection List',
                position=(1300, 850),
                font_name='Arial',
                font_size=48,
                anchor_x='left',
                anchor_y='bottom'
            )
        )

    def add_entry(self, ip_address, port, connection):
        self.add(
            ConnectionListEntryNode(
                server_address=(ip_address, port),
                init_position=(1250, 800),
                entry_number=len(self.children)-1,
                connection=connection
            )
        )

    def on_mouse_press(self, x, y, buttons, modifiers):
        x, y = director.get_virtual_coordinates(x, y)
        if 1300 < x < 1870:
            upper_end = 800
            for child in self.get_children():
                if child.__class__ == ConnectionListEntryNode:
                    if upper_end > y > upper_end - 125:
                        if buttons & mouse.LEFT:
                            if child.connection.is_connected():
                                child.connection.disconnect()
                            else:
                                child.connection.connect()
                        else:
                            child.connection.disconnect()
                            self.parent.connections.remove(child.connection)
                    upper_end -= 140

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
        self.server_ip_addresses = server_manager.get_available_ip_addresses()
        self.selected_server_ip_idx = 0
        self.selected_connection_address = (self.server_ip_addresses[0], 9999)
        menu_items = [
            cocos.menu.MultipleMenuItem(
                label='IP: ',
                callback_func=self.on_server_ip_address,
                items=self.server_ip_addresses,
                default_item=self.selected_server_ip_idx
            ),
            cocos.menu.MenuItem('Create Server', self.on_create_server),
            cocos.menu.EntryMenuItem(
                label='IP: ',
                callback_func=self.on_connection_ip_address,
                value=self.server_ip_addresses[0],
                max_length=16
            ),
            cocos.menu.EntryMenuItem(
                label='Port: ',
                callback_func=self.on_connection_port,
                value='9999',
                max_length=5
            ),
            cocos.menu.MenuItem('Open Connection', self.on_open_connection),
            cocos.menu.MenuItem('Shutdown All', self.on_shutdown_all),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out(),
            layout_strategy=cocos.menu.fixedPositionMenuLayout([
                (280, 900),
                (280, 850),
                (280, 750),
                (280, 700),
                (280, 650),
                (280, 550),
                (280, 500)
            ])
        )

    def on_server_ip_address(self, selected_ip_idx):
        self.selected_server_ip_idx = selected_ip_idx

    def on_create_server(self):
        pid = server_manager.run_server(
            self.server_ip_addresses[self.selected_server_ip_idx]
        )
        ip_address = server_manager.get_ip_address(pid)
        port = server_manager.get_port(pid)
        self.parent.get('server_list').add_entry(
            ip_address,
            port,
            pid
        )

    def on_connection_ip_address(self, new_value):
        self.selected_connection_address = (
            new_value,
            self.selected_connection_address[1]
        )

    def on_connection_port(self, new_value):
        try:
            self.selected_connection_address = (
                self.selected_connection_address[0],
                int(new_value)
            )
        except ValueError:
            pass

    def on_open_connection(self):
        connection = pygase.client.Connection(self.selected_connection_address)
        self.parent.connections.append(connection)
        self.parent.get('connection_list').add_entry(
            ip_address=self.selected_connection_address[0],
            port=self.selected_connection_address[1],
            connection=connection
        )

    def on_shutdown_all(self):
        server_manager.clean_up()

    def on_back(self):
        self.parent.end()

    def on_quit(self):
        self.on_back()

class ServerTestScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.add(ServerTestMenuLayer(), name='menu_layer')
        self.add(ServerListLayer(), name='server_list')
        self.add(ConnectionListLayer(), name='connection_list')

    def on_exit(self):
        for connection in self.connections:
            connection.disconnect()
        super().on_exit()
