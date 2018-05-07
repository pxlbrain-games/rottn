# -*- coding: utf-8 -*-

import socket
import cocos
from cocos.director import director
import bossfight.client.testScene as testScene

director.init()

# Run bossfight.server and then run the client on another terminal

buffersize = 1024
server_address = ('localhost', 9990)

try:
    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    clientSocket.sendto('BossFight'.encode('utf-8'), server_address)
    serverResponse = str(clientSocket.recv(buffersize), 'utf-8')
except:
    serverResponse = 'Server not found.'

testScene = testScene.TestScene(serverResponse)
director.run(testScene)