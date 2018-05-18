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
SharedGameState(self, time_order=0, game_status=1)
```

Contains game state information that is required to be known both by the server and the client.
Since it is a *Sendable*, it can only contain basic python types as attributes.

*time_order* should be in alignment with the servers current update counter.

<h3 id="bossfight.core.sharedGameData.SharedGameState.is_paused">is_paused</h3>

```python
SharedGameState.is_paused(self)
```

Returns *True* if game status is *Paused*.

<h2 id="bossfight.core.sharedGameData.SharedGameStateUpdate">SharedGameStateUpdate</h2>

```python
SharedGameStateUpdate(self, time_order=0, **kwargs)
```

Represents a set of changes to carry out on a *SharedGameState*.
The server should keep an update counter and label all updated with ascending index.

Keywords are *SharedGameState* atttribute names.

Use the *+* operator to add *SharedGameStateUpdate*s together or to add them to a
*SharedGameState* (returning the updated update/state).

Adding up available updates will always result in an equally or more current but
also heavier update (meaning it will contain more data).

<h2 id="bossfight.core.sharedGameData.PlayerAction">PlayerAction</h2>

```python
PlayerAction(self, /, *args, **kwargs)
```

An update the player sends to the server about the actions of it's character.
Any collision events involving the player character are processed client-side and sent as
*PlayerAction*s to the server. The server will validate a client's *PlayerAction* and
respond with an *OutOfSync* error, if it doesn't add up with the server-side game state.

