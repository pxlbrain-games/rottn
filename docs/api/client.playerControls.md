<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.playerControls">bossfight.client.playerControls</h1>


Defines the controls for the player character.

<h2 id="bossfight.client.playerControls.ControllableNode">ControllableNode</h2>

```python
ControllableNode(self, position=(0, 0), joystick=None, mouse_and_keyboard=True, speed=300)
```

A *CocosNode* that can be controlled by the player.
Controllable Nodes automatically react to Controller or Mouse & Keyboard input.
If you use multiple inheritance, inherit from *ControllableNode* before any third party
(and thus possibly non-cooperative) base classes. (This class **is** cooperative btw.)

