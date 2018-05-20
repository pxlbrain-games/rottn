<h1 id="bossfight.server">bossfight.server</h1>


<h1 id="bossfight.server.gameService">bossfight.server.gameService</h1>


This module defines the *GameService* class, a server that can handle requests from
a client's *GameServiceConnection* object.

**Note: The IP address you bind the GameService to is a local IP address from the
192.168.x.x address space. If you want computers outside your local network to be
able to connect to your game server, you will have to forward the port from the local
address your server is bound to to your external IPv4 address!**

<h2 id="bossfight.server.gameService.GameService">GameService</h2>

```python
GameService(self, ip_address:str, port:int)
```

Threading UDP server that manages clients and processes requests.

Call *serve_forever*() in a seperate thread for the server to start handling requests from
*GameServiceConnection*s. Call *shutdown*() to stop it.

*game_loop* is the server's *GameLoop* object, which simulates the game logic and updates
the *shared_game_state*.

<h3 id="bossfight.server.gameService.GameService.start">start</h3>

```python
GameService.start(self)
```

Runs the server in a dedicated Thread and starts the game loop.
Does nothing if server is already running.
Must be called for the server to handle requests and is terminated by *shutdown()*

<h3 id="bossfight.server.gameService.GameService.shutdown">shutdown</h3>

```python
GameService.shutdown(self)
```

Stops the server's request handling and pauses the game loop.

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

