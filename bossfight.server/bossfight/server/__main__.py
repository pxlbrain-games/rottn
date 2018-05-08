# -*- coding: utf-8 -*-

from bossfight.server.testServer import UDPGameService

with UDPGameService(('localhost', 9990)) as server:
    server.serve_forever()