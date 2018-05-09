# -*- coding: utf-8 -*-

import threading
from bossfight.server.gameService import UDPGameService

server = UDPGameService(('localhost', 9990))
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
server_thread.join(5.0)
print('Server ran for 5 s.')
server.shutdown()