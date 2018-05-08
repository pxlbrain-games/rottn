# -*- coding: utf-8 -*-

import socket
import cocos
from cocos.director import director
import bossfight.client.testScene as testScene
import bossfight.client.gameServiceConnection as gameServiceConnection
import bossfight.core.gameServiceProtocol as gsp

director.init()

# Run bossfight.server and then run the client on another terminal

connection = gameServiceConnection.UDPGameServiceConnection(('localhost', 9990))

request1 = gsp.GameServicePackage(gsp.PackageType.GetSharedGameStateRequest)
request2 = gsp.GameServicePackage(gsp.PackageType.GetGameStateUpdateRequest)

text = ''

try:
    response = connection.send_and_recv(request1)
    if response.header.package_type == gsp.PackageType.GameServiceResponse and response.header.body_type == 'SharedGameState':
        text = 'Connection successful!'
    response = connection.send_and_recv(request2)
    if response.header.package_type == gsp.PackageType.GameServiceError:
        text = 'Connection still successful!'
except:
    text = 'Connection failed.'

testScene = testScene.TestScene(text)
director.run(testScene)