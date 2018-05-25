<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.ui">bossfight.client.ui</h1>


Defines CocosNodes for UI elements and provides useful mixins for user interaction.

<h2 id="bossfight.client.ui.Clickable">Clickable</h2>

```python
Clickable(self, /, *args, **kwargs)
```

Mixin that makes a CocosNode clickable and clicking on it
will call it's *on_click()* function.

<h2 id="bossfight.client.ui.Dragable">Dragable</h2>

```python
Dragable(self, /, *args, **kwargs)
```

Mixin that makes a CocosNode dragable by mouse and calls
it's *on_drag()* and *on_drop()* function.

