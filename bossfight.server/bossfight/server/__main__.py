# -*- coding: utf-8 -*-
'''
Main script of bossfight.server package.

- `bossfight.server` will run a local server on an arbitrary free port
- `bossfight.server ip_address` will start a server on an arbitrary free port
bound to the given IP address.
- `bossfight.server ip_address port` will run a server on the specified port
and IP address.

In either case the server process will give the following output on stdout
directly after starting the server:

`ip_address\\n

port\\EOF`

To shutdown the server, write a line containing `shutdown` to the processes
*stdin* channel.
'''

import sys
import pygase.shared
import pygase.server
from bossfight.core import SHARED_GAME_STATE
from bossfight.server.game_loop import BFGameLoop

if len(sys.argv) == 1:
    SERVER = pygase.server.Server(
        ip_address='localhost',
        port=0,
        game_loop_class=BFGameLoop,
        game_state=SHARED_GAME_STATE
    )
elif len(sys.argv) == 2:
    SERVER = pygase.server.Server(
        ip_address=sys.argv[1],
        port=0,
        game_loop_class=BFGameLoop,
        game_state=SHARED_GAME_STATE
    )
else:
    SERVER = pygase.server.Server(
        ip_address=sys.argv[1],
        port=int(sys.argv[2]),
        game_loop_class=BFGameLoop,
        game_state=SHARED_GAME_STATE
    )

print(SERVER.get_ip_address())
print(SERVER.get_port())
sys.stdout.close()

SERVER.start()

while not sys.stdin.readline().__contains__('shutdown'):
    pass
SERVER.shutdown()
