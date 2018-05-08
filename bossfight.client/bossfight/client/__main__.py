# -*- coding: utf-8 -*-

import socket
import cocos
from cocos.director import director
import bossfight.client.testScene as testScene
import bossfight.client.gameServiceConnection as gameServiceConnection
import bossfight.core.gameServiceProtocol as gsp

director.init()

# Run bossfight.server and then run the client on another terminal

connection = gameServiceConnection.GameServiceConnection(('localhost', 9990))

request = gsp.GameServicePackage(gsp.PackageType.GetSharedGameStateRequest)

text = ''

try:
    response = connection.send_and_recv(request)
    if response.header.package_type == gsp.PackageType.GameServiceResponse and response.header.body_type == 'SharedGameState':
        text = 'Connection successful!'
except:
    text = 'Connection failed.'

testScene = testScene.TestScene(text)
director.run(testScene)