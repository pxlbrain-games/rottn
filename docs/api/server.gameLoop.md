<h1 id="bossfight.server">bossfight.server</h1>


<h1 id="bossfight.server.gameLoop">bossfight.server.gameLoop</h1>


This module handles the game logic, that is to be simulated by the server.
A game loop takes a *SharedGameState* and will update it according to the game logic
defined in it's update cycle, as long as the *game_status* is not *Paused*.

<h2 id="bossfight.server.gameLoop.GameLoop">GameLoop</h2>

```python
GameLoop(self, shared_game_state:bossfight.core.sharedGameData.SharedGameState, player_action_queue:list)
```

Class that can update a shared game state by running a game logic simulation thread.
It must be passed a *SharedGameState* and a list of *PlayerAction*s from the
*GameService* object which owns the GameLoop.

Currently it only simulates a sine signal in the shared game state attribute *test_pos*.

<h3 id="bossfight.server.gameLoop.GameLoop.start">start</h3>

```python
GameLoop.start(self)
```

Starts a thread that updates the shared game state every *update_cycle_interval* seconds.
Use this to restart a paused game.

<h3 id="bossfight.server.gameLoop.GameLoop.pause">pause</h3>

```python
GameLoop.pause(self)
```

Stops the game loop until *start()* is called.
If the game loop is not currently running does nothing.

