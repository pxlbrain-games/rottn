# -*- coding: utf-8 -*-
'''
This module mainly contains the *GameServiceConnection* class, which represents a connection to a
running GameService (meaning a game server). Use this to manage your server connections.
'''

import socket
import threading
import time
import bossfight.core.sharedGameData as sharedGameData
import bossfight.core.gameServiceProtocol as gsp

class ConnectionStatus:
    '''
    Enum class with the following values:
    - *Connected*: Connection is running.
    - *WaitingForServer*: Connection is trying to connect/reconnect to the server.
    - *Disconnected*: Connection is not communicating with the server.
    '''
    @property
    def Connected(self):
        return 1
    @property
    def WaitingForServer(self):
        return 2
    @property
    def Disconnected(self):
        return 3

class GameServiceConnection:
    '''
    Initialization of a *GameServiceConnection* will open a connection to a BossFight GameService
    with the specified *server_address* as a tuple containing the IP-adress as a string and the
    port as an int. Check the *connection_status* attribute to get the status of the Connection as
    a *ConnectionStatus()* attribute.

    A running *GameServiceConnection* will request an update of *sharedGameState* from the server
    every *update_cycle_interval* seconds.
    *sharedGameState* is a *sharedGameData.SharedGameState* object.
    '''

    @property
    def request_timeout(self):
        return self._client_socket.timeout

    @request_timeout.setter
    def request_timeout(self, value: float):
        self._client_socket.settimeout(value)

    def __init__(self, server_address, closed=False):
        self.shared_game_state = sharedGameData.SharedGameState()
        self.server_address = server_address
        self._client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.request_timeout = 0.5
        self.connection_timeout = 5.0
        self.latency = 0
        self._buffer_size = 1024
        self.update_cycle_interval = 0.03
        self._polled_actions = {}
        if not closed:
            self._update_cycle_thread = threading.Thread(target=self._update_cycle)
            self.connection_status = ConnectionStatus().WaitingForServer
            self._update_cycle_thread.start()
        else:
            self._update_cycle_thread = threading.Thread()
            self.connection_status = ConnectionStatus().Disconnected

    def __del__(self):
        self.disconnect()
        self._client_socket.close()

    def _send_and_recv(self, package: gsp.GameServicePackage):

        # Send package to server ...
        self._client_socket.sendto(package.to_datagram(), self.server_address)
        # ... and return response if possible, otherwise return GameServiceError package
        try:
            return gsp.GameServicePackage.from_datagram(self._client_socket.recv(self._buffer_size))
        except socket.timeout:
            return gsp.timeout_error('Request timed out.')
        except ConnectionResetError:
            return gsp.timeout_error('Server not found.')

    def connect(self):
        '''
        Will try to connect/reconnect to the server if *connection_status* is
        *ConnectionStatus().Disconnected*, otherwise does nothing.
        '''
        if not self._update_cycle_thread.is_alive():
            self._update_cycle_thread = threading.Thread(target=self._update_cycle)
            self._update_cycle_thread.start()

    def disconnect(self):
        '''
        Will stop the connection from sending any further requests to the server.
        Will do nothing if *connection_status* == *ConnectionStatus().Disconnected*.
        '''
        t_0 = time.time()
        # Force update cycle to end
        while self._update_cycle_thread.is_alive() and time.time()-t_0 < self.request_timeout:
            self.connection_status = ConnectionStatus().Disconnected
        if self._update_cycle_thread.is_alive():
            raise threading.ThreadError

    def is_connected(self):
        '''
        Returns *True* if the connection status is *Connected*.
        '''
        return self.connection_status == ConnectionStatus().Connected

    def is_waiting(self):
        '''
        Returns *True* if the connection status is *WaitingForServer*.
        '''
        return self.connection_status == ConnectionStatus().WaitingForServer

    def poll_player_action(self, player_action: sharedGameData.PlayerAction):
        '''
        Sends the *PlayerAction* object to the server. ---> Not fully implemented yet! <---
        '''
        ### Implement polling!
        thread = threading.Thread(
            target=self._send_and_recv,
            args=(gsp.post_action_request(player_action))
        )
        thread.start()

    def _try_connect(self):
        t_0 = time.time()
        self.connection_status = ConnectionStatus().WaitingForServer
        # Try to successfully get the shared game state for connection_timeout seconds
        while time.time()-t_0 < self.connection_timeout and \
          not self.connection_status == ConnectionStatus().Disconnected:
            t_1 = time.time()
            response = self._send_and_recv(gsp.game_state_request())
            if response.is_response():
                self.shared_game_state = response.body
                self.connection_status = ConnectionStatus().Connected
                return # Connection successful, leave _try_connect()
            #elif response.is_error():
            #    print(response.body.message)
            dt = time.time() - t_1
            time.sleep(max(self.update_cycle_interval - dt, 0))
        # if this point is reached connection was unsuccessful
        self.connection_status = ConnectionStatus().Disconnected

    def _update_cycle(self):
        self._try_connect()
        latency_timer = 0
        while not self.connection_status == ConnectionStatus().Disconnected:
            t_0 = time.time()
            response = self._send_and_recv(
                gsp.game_state_update_request(self.shared_game_state.time_order)
            )
            if response.is_response():
                self.shared_game_state += response.body
            else:
                #if response.is_error():
                #    print(response.body.message)
                self._try_connect()
            dt = time.time()-t_0
            if not latency_timer % 60:
                self.latency = dt*1000
            latency_timer += 1
            time.sleep(max(self.update_cycle_interval-dt, 0))
