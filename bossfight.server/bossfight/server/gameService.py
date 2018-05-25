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
from bossfight.core.sharedGameData \
    import SharedGameState, SharedGameStateUpdate, ActivityType, GameStatus
import bossfight.core.gameServiceProtocol as gsp
from bossfight.server.gameLoop import GameLoop

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
        self.shared_game_state = SharedGameState()
        self.client_activity_queue = []
        self._player_counter = 0
        self.game_loop = GameLoop(
            shared_game_state=self.shared_game_state,
            client_activity_queue=self.client_activity_queue,
        )
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
            # respond by sending the sum of all updates since the client's time-order point.
            update = sum(
                (upd for upd in self.server.game_loop.state_update_cache if upd > request.body),
                request.body
            )
            response = gsp.response(update)
        elif request.is_post_activity_request():
            # Pausing or Resuming the game and joining a server must be possible outside
            # of the game loop:
            if request.body.activity_type == ActivityType().PauseGame:
                self.server.game_loop.pause()
                self.server.shared_game_state.time_order += 1
                self.server.game_loop.cache_state_update(SharedGameStateUpdate(
                    time_order=self.server.shared_game_state.time_order,
                    game_status=GameStatus().Paused
                ))
            elif request.body.activity_type == ActivityType().ResumeGame:
                self.server.shared_game_state.time_order += 1
                self.server.game_loop.cache_state_update(SharedGameStateUpdate(
                    time_order=self.server.shared_game_state.time_order,
                    game_status=GameStatus().Active
                ))
                self.server.game_loop.start()
            elif request.body.activity_type == ActivityType().JoinServer:
                # A player dict is added to the game state. The id is unique for the
                # server session (counting from 0 upwards).
                update = SharedGameStateUpdate(
                    time_order=self.server.shared_game_state.time_order + 1,
                    players={
                        self.server._player_counter: {
                            'name': request.body.activity_data['name'],
                            'position': (0, 0),
                            'velocity': (0, 0)
                        }
                    }
                )
                self.server._player_counter += 1
                self.server.shared_game_state += update
                self.server.game_loop.cache_state_update(update)
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
