# -*- coding: utf-8 -*-

from bossfight.server.testServer import TestUDPServer

with TestUDPServer(('localhost', 9990)) as server:
    server.serve_forever()