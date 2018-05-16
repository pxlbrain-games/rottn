<h1 id="bossfight.core">bossfight.core</h1>


<h1 id="bossfight.core.mixins">bossfight.core.mixins</h1>


Module that contains some useful mixin classes.

<h2 id="bossfight.core.mixins.Sendable">Sendable</h2>

```python
Sendable(self, /, *args, **kwargs)
```

Mixin for classes that are supposed to be sendable as part of a server request or response.
Sendables can only have basic Python types as attributes and their constructor needs
to be callable without passing any arguments.

