# -*- coding: utf-8 -*-

import threading
from bossfight.server.gameService import GameService

server = GameService(('localhost', 9999))
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
server_thread.join(10.0)
print('Server ran for 10 s.')
server.shutdown()