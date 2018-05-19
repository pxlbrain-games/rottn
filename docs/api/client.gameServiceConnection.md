<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.gameServiceConnection">bossfight.client.gameServiceConnection</h1>


This module mainly contains the *GameServiceConnection* class, which represents a connection to a
running GameService (meaning a game server). Use this to manage your server connections.

<h2 id="bossfight.client.gameServiceConnection.ConnectionStatus">ConnectionStatus</h2>

```python
ConnectionStatus(self, /, *args, **kwargs)
```

Enum class with the following values:
- *Connected*: Connection is running.
- *WaitingForServer*: Connection is trying to connect/reconnect to the server.
- *Disconnected*: Connection is not communicating with the server.

<h2 id="bossfight.client.gameServiceConnection.GameServiceConnection">GameServiceConnection</h2>

```python
GameServiceConnection(self, server_address, closed=False)
```

Initialization of a *GameServiceConnection* will open a connection to a BossFight GameService
with the specified *server_address* as a tuple containing the IP-adress as a string and the
port as an int. Check the *connection_status* attribute to get the status of the Connection as
a *ConnectionStatus()* attribute.

A running *GameServiceConnection* will request an update of *shared_game_state* from the server
every *update_cycle_interval* seconds.

<h3 id="bossfight.client.gameServiceConnection.GameServiceConnection.connect">connect</h3>

```python
GameServiceConnection.connect(self)
```

Will try to connect/reconnect to the server if *connection_status* is
*ConnectionStatus().Disconnected*, otherwise does nothing.

<h3 id="bossfight.client.gameServiceConnection.GameServiceConnection.disconnect">disconnect</h3>

```python
GameServiceConnection.disconnect(self)
```

Will stop the connection from sending any further requests to the server.
Will do nothing if *connection_status* == *ConnectionStatus().Disconnected*.

<h3 id="bossfight.client.gameServiceConnection.GameServiceConnection.is_connected">is_connected</h3>

```python
GameServiceConnection.is_connected(self)
```

Returns *True* if the connection status is *Connected*.

<h3 id="bossfight.client.gameServiceConnection.GameServiceConnection.is_waiting">is_waiting</h3>

```python
GameServiceConnection.is_waiting(self)
```

Returns *True* if the connection status is *WaitingForServer*.

<h3 id="bossfight.client.gameServiceConnection.GameServiceConnection.post_player_action">post_player_action</h3>

```python
GameServiceConnection.post_player_action(self, player_action:bossfight.core.sharedGameData.PlayerAction)
```

Sends the *PlayerAction* object to the server.

