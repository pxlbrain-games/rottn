<h1 id="bossfight.core">bossfight.core</h1>


<h1 id="bossfight.core.sharedGameData">bossfight.core.sharedGameData</h1>


This module contains classes for game objects that are relevant for both client and server.
Client as well as server are supposed to define subclasses of the classes in this module,
that extend those types with data and functionality, that is client-/server-specific.

<h2 id="bossfight.core.sharedGameData.Sendable">Sendable</h2>

```python
Sendable(self, /, *args, **kwargs)
```

Mixin for classes that are supposed to be sendable as part of a server request or response.
Sendables can only have basic Python types as attributes and their constructor needs
to be callable without passing any arguments.

<h3 id="bossfight.core.sharedGameData.Sendable.from_bytes">from_bytes</h3>

```python
Sendable.from_bytes(bytepack:bytes)
```

Returns a copy of the object that was packed into byte format.

<h3 id="bossfight.core.sharedGameData.Sendable.to_bytes">to_bytes</h3>

```python
Sendable.to_bytes(self)
```

Packs and return a small a binary representation of self.


<h2 id="bossfight.core.sharedGameData.GameStatus">GameStatus</h2>

```python
GameStatus(self, /, *args, **kwargs)
```

Enum class with the values:
- *Paused*
- *Active*

<h2 id="bossfight.core.sharedGameData.ActivityType">ActivityType</h2>

```python
ActivityType(self, /, *args, **kwargs)
```

Enum class with the values:
- *PauseGame*
- *ResumeGame*

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

<h2 id="bossfight.core.sharedGameData.ClientActivity">ClientActivity</h2>

```python
ClientActivity(self, activity_type=1, activity_data={})
```

An update the client sends to the server about client-side processes like player movement and
collisions. The server will validate *ClientActivity* samples and respond with an *OutOfSync*
error, if they contradict the server-side game state.

*activity_data* is a *dict* object, that contains all necessary information to process the
activity server-side (a player's *id*, *position* and *velocity* for example).

<h2 id="bossfight.core.sharedGameData.join_server_activity">join_server_activity</h2>

```python
join_server_activity(player_name:str)
```

Returns a *ClientActivity* that joins a player with name *player_name* to the game.

<h2 id="bossfight.core.sharedGameData.toggle_pause_activity">toggle_pause_activity</h2>

```python
toggle_pause_activity(shared_game_state:bossfight.core.sharedGameData.SharedGameState)
```

Returns a *ClientActivity* that either pauses or resumes the server's game loop, depending
on the *game_status* of the given *SharedGameState*.

