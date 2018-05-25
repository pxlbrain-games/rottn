# -*- coding: utf-8 -*-
'''
This module defines the *GameService* class, a server that can handle requests from
a client's *GameServiceConnection* object.

**Note: The IP address you bind the GameService to is a local IP address from the
192.168.x.x address space. If you want computers outside your local network to be
able to connect to your game server, you will have to forward the port from the local
address your server is bound to to your external IPv4 address!**
'''

import socketserver
import threading
from umsgpack import InsufficientDataException
import bossfight.core.sharedGameData as sharedGameData
import bossfight.core.gameServiceProtocol as gsp
from bossfight.server.gameLoop import GameLoop

UPDATE_CACHE_SIZE = 100

class GameService(socketserver.ThreadingUDPServer):
    '''
    Threading UDP server that manages clients and processes requests.

    Call *serve_forever*() in a seperate thread for the server to start handling requests from
    *GameServiceConnection*s. Call *shutdown*() to stop it.

    *game_loop* is the server's *GameLoop* object, which simulates the game logic and updates
    the *shared_game_state*.
    '''

    def __init__(self, ip_address: str, port: int):
        super().__init__((ip_address, port), _GameServiceRequestHandler)
        self.shared_game_state = sharedGameData.SharedGameState()
        self.client_activity_queue = []
        self._state_update_cache = []
        self._player_counter = 0
        self.game_loop = GameLoop(self)
        self._server_thread = threading.Thread()

    def start(self):
        '''
        Runs the server in a dedicated Thread and starts the game loop.
        Does nothing if server is already running.
        Must be called for the server to handle requests and is terminated by *shutdown()*
        '''
        if not self._server_thread.is_alive():
            self._server_thread = threading.Thread(target=self.serve_forever)
            self.game_loop.start()
            self._server_thread.start()

    def shutdown(self):
        '''
        Stops the server's request handling and pauses the game loop.
        '''
        super().shutdown()
        self.game_loop.pause()

    def get_ip_address(self):
        '''
        Returns the servers IP address as a string.
        '''
        return self.socket.getsockname()[0]

    def get_port(self):
        '''
        Returns the servers port as an integer.
        '''
        return self.socket.getsockname()[1]

    def cache_state_update(self, state_update: sharedGameData.SharedGameStateUpdate):
        self._state_update_cache.append(state_update)
        if len(self._state_update_cache) > UPDATE_CACHE_SIZE:
            self._state_update_cache = self._state_update_cache[1:]

class _GameServiceRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Read out request
        try:
            request = gsp.GameServicePackage.from_datagram(self.request[0])
        except (InsufficientDataException, TypeError):
            # if unpacking request failed send back error message and exit handle function
            response = gsp.unpack_error('Server responded: Byte error.')
            self.request[1].sendto(response.to_datagram(), self.client_address)
            return

        # Handle request and assign response here
        if request.is_update_request():
            # respond by sending an update representing the whole state for now.
            # Proper updating still needs to be implemented.
            update = sharedGameData.SharedGameStateUpdate(
                time_order=self.server.shared_game_state.time_order,
                game_status=self.server.shared_game_state.game_status,
                test_pos=self.server.shared_game_state.test_pos
            )
            response = gsp.response(update)
        elif request.is_post_activity_request():
            # Pausing or Resuming the game and joining a server must be possible outside
            # of the game loop:
            if request.body.activity_type == sharedGameData.ActivityType().PauseGame:
                self.server.game_loop.pause()
                self.server.shared_game_state.time_order += 1
                self.server.cache_state_update(sharedGameData.SharedGameStateUpdate(
                    time_order=self.server.shared_game_state.time_order,
                    game_status=sharedGameData.GameStatus().Paused
                ))
            elif request.body.activity_type == sharedGameData.ActivityType().ResumeGame:
                self.server.shared_game_state.time_order += 1
                self.server.cache_state_update(sharedGameData.SharedGameStateUpdate(
                    time_order=self.server.shared_game_state.time_order,
                    game_status=sharedGameData.GameStatus().Active
                ))
                self.server.game_loop.start()
            elif request.body.activity_type == sharedGameData.ActivityType().JoinServer:
                # A player dict is added to the game state. The id is unique for the
                # server session.
                self.server.shared_game_state.players.append({
                    'id': self.server._player_counter,
                    'name': request.body.activity_data['name'],
                    'position': (0, 0),
                    'velocity': (0, 0)
                })
                self.server._player_counter += 1
            else:
                # Any other kind of activity: add to the queue for the game loop
                self.server.client_activity_queue.append(request.body)
            response = gsp.response(None)
        elif request.is_state_request():
            # respond by sending back the shared game state
            response = gsp.response(self.server.shared_game_state)
        else:
            # if none of the above were a match the request was invalid
            response = gsp.request_invalid_error('Server responded: Request invalid.')

        # Send response
        self.request[1].sendto(response.to_datagram(), self.client_address)
