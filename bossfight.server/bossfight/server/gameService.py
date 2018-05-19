# -*- coding: utf-8 -*-
'''
This module defines the *GameService* class, a server that can handle requests from
a client's *GameServiceConnection* object.
'''

import socketserver
import threading
from umsgpack import InsufficientDataException
import bossfight.core.sharedGameData as sharedGameData
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
        self.shared_game_state = sharedGameData.SharedGameState()
        self.player_action_queue = []
        self.game_loop = GameLoop(self.shared_game_state, self.player_action_queue)
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
            # respond by sending an update representing the whole state for now.
            # Proper updating still needs to be implemented.
            update = sharedGameData.SharedGameStateUpdate(
                time_order=self.server.shared_game_state.time_order,
                game_status=self.server.shared_game_state.game_status,
                test_pos=self.server.shared_game_state.test_pos
            )
            response = gsp.response(update)
        elif request.is_post_action_request():
            if request.body.action_type == sharedGameData.ActionType().PauseGame:
                self.server.game_loop.pause()
            elif request.body.action_type == sharedGameData.ActionType().ResumeGame:
                self.server.game_loop.start()
            else:                
                # add the player action to the queue
                self.server.player_action_queue.append(request.body)
            response = gsp.response(None)
        elif request.is_state_request():
            # respond by sending back the shared game state
            response = gsp.response(self.server.shared_game_state)
        else:
            # if none of the above were a match the request was invalid
            response = gsp.request_invalid_error('Server responded: Request invalid.')

        # Send response
        self.request[1].sendto(response.to_datagram(), self.client_address)
