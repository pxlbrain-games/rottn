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
import threading
from bossfight.server.gameService import GameService

if len(sys.argv) == 1:
    SERVER = GameService('localhost', 0)
elif len(sys.argv) == 2:
    SERVER = GameService(sys.argv[1], 0)
else:
    SERVER = GameService(sys.argv[1], int(sys.argv[2]))

print(SERVER.get_ip_address())
print(SERVER.get_port())
sys.stdout.close()

SERVER_THREAD = threading.Thread(target=SERVER.serve_forever)
SERVER_THREAD.start()

SHUTDOWN = False
while not SHUTDOWN:
    if sys.stdin.readline().__contains__('shutdown'):
        SERVER.shutdown()
        SHUTDOWN = True
