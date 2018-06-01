<h1 id="bossfight.server">bossfight.server</h1>


<h1 id="bossfight.server.game_loop">bossfight.server.game_loop</h1>


<h2 id="bossfight.server.game_loop.BFGameLoop">BFGameLoop</h2>

```python
BFGameLoop(self, server:pygase.server.Server)
```

Subclasses the GameLoop from the PyGaSe package and defines server-side
game logic.

<h3 id="bossfight.server.game_loop.BFGameLoop.on_join">on_join</h3>

```python
BFGameLoop.on_join(self, player_id, update)
```

Initial assignments for when a new player joins the game.

<h3 id="bossfight.server.game_loop.BFGameLoop.handle_activity">handle_activity</h3>

```python
BFGameLoop.handle_activity(self, activity, update, dt)
```

Handling of custom BossFight client activities, like player movement or actions.

<h3 id="bossfight.server.game_loop.BFGameLoop.update_game_state">update_game_state</h3>

```python
BFGameLoop.update_game_state(self, update, dt)
```

BossFight game state update. Simulates enemies and game world objects.

