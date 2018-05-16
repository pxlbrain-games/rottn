<h1 id="bossfight.server">bossfight.server</h1>


<h1 id="bossfight.server.gameService">bossfight.server.gameService</h1>


This module defines the *GameService* class, a server that can handle requests from
a client's *GameServiceConnection* object.

<h2 id="bossfight.server.gameService.GameService">GameService</h2>

```python
GameService(self, ip_address:str, port:int)
```

Threading UDP server that manages clients and processes requests.

Call *serve_forever*() in a seperate thread for the server to start handling requests from
*GameServiceConnection*s. Call *shutdown*() to stop it.

<h3 id="bossfight.server.gameService.GameService.get_ip_address">get_ip_address</h3>

```python
GameService.get_ip_address(self)
```

Returns the servers IP address as a string.

<h3 id="bossfight.server.gameService.GameService.get_port">get_port</h3>

```python
GameService.get_port(self)
```

Returns the servers port as an integer.

