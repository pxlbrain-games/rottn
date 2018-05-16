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

<h3 id="bossfight.server.gameService.GameService.get_available_ip_addresses">get_available_ip_addresses</h3>

```python
GameService.get_available_ip_addresses()
```

Returns a list of all available IP addresses that the server can be bound to.
Keep in mind that `127.0.0.1` is only suitable for local servers.

<h3 id="bossfight.server.gameService.GameService.get_address">get_address</h3>

```python
GameService.get_address(self)
```

Returns a tuple *(ip_address: str, port: int)* that represents the servers address.

