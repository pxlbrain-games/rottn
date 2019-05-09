# -*- coding: utf-8 -*-
"""
Main script of rottn.server package.

- `rottn.server` will run a local server on an arbitrary free port
- `rottn.server ip_address` will start a server on an arbitrary free port
bound to the given IP address.
- `rottn.server ip_address port` will run a server on the specified port
and IP address.

In either case the server process will give the following output on stdout
directly after starting the server:

`ip_address\\n

port\\EOF`

To shutdown the server, write a line containing `shutdown` to the processes
*stdin* channel.
"""

import time
import sys
from pygase import Server, GameStateStore, GameState
from rottn.server.game_loop import BFStateMachine

SHARED_GAME_STATE = GameState(npcs=dict(), players=dict())
GAME_STATE_STORE = GameStateStore(SHARED_GAME_STATE)
SERVER = Server(GAME_STATE_STORE)
GAME_STATE_MACHINE = BFStateMachine(GAME_STATE_STORE, SERVER)

IP_ADDRESS, PORT = ('localhost', 0)
if len(sys.argv) > 1:
    IP_ADDRESS = sys.argv[1]
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])

GAME_STATE_MACHINE.run_game_loop_in_thread()
SERVER.run_in_thread(PORT, IP_ADDRESS, GAME_STATE_MACHINE)
time.sleep(0.1)
print(SERVER.hostname)
print(SERVER.port)
sys.stdout.close()

while not sys.stdin.readline().__contains__("shutdown"):
    pass
SERVER.shutdown()
