<h1 id="bossfight.core">bossfight.core</h1>


<h1 id="bossfight.core.sharedGameData">bossfight.core.sharedGameData</h1>


This module contains classes for game objects that are relevant for both client and server.
Client as well as server are supposed to define subclasses of the classes in this module,
that extend those types with data and functionality, that is client-/server-specific.

<h2 id="bossfight.core.sharedGameData.GameStatus">GameStatus</h2>

```python
GameStatus(self, /, *args, **kwargs)
```

Enum class with the values:
- *Paused*
- *Active*

<h2 id="bossfight.core.sharedGameData.SharedGameState">SharedGameState</h2>

```python
SharedGameState(self, game_status=1)
```

Contains game state information that is required to be known both by the server and the client.
Since it is a *Sendable*, it can only contain basic python types as attributes.

