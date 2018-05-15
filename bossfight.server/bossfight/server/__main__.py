# -*- coding: utf-8 -*-

import sys
import threading
from bossfight.server.gameService import GameService

for arg in sys.argv:
    pass

server = GameService('localhost', 9999)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
server_thread.join(10.0)
print('Server ran for 10 s.')
server.shutdown()