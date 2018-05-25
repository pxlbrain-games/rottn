<h1 id="bossfight.client.scenes">bossfight.client.scenes</h1>


<h1 id="bossfight.client.scenes.levelScene">bossfight.client.scenes.levelScene</h1>


This is going to be the module containing the base level classes and components.

<h2 id="bossfight.client.scenes.levelScene.LevelScene">LevelScene</h2>

```python
LevelScene(self, server_address, local_player_names)
```

Base class for alls kinds of ingame levels. It provides access to
the level coordinate space, let's you add ingame objects like
characters to the level, manages controls and HUD etc.

Note: Currently this class implements a *Scene* that contains test content.

<h2 id="bossfight.client.scenes.levelScene.LevelLayer">LevelLayer</h2>

```python
LevelLayer(self, level_data:bossfight.client.scenes.levelScene.LevelData)
```

Layer that contains the actual level itself and everything in it.

