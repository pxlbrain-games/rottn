<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.config">bossfight.client.config</h1>


Module that manages access to the clients configuration. Via *config.get* you get
a singleton object that allows access to the config keys as attributes:
`config.get.screen_mode['width'] = 1920`
Use *load()* and *save()* to persist and restore config on/from disk.

<h2 id="bossfight.client.config.get_default">get_default</h2>

```python
get_default()
```

Returns a deep copy of the default configuration dictionary.

<h2 id="bossfight.client.config.revert_to_default">revert_to_default</h2>

```python
revert_to_default()
```

Reverts config data to the default configuration.

<h2 id="bossfight.client.config.save">save</h2>

```python
save()
```

Saves the client configuration data in a json file in the application data directory.

Windows 7+: `C:\Users\{username}\AppData\Local\ePyCom\bossfight\client_config.json`

<h2 id="bossfight.client.config.load">load</h2>

```python
load()
```

Loads the client configuration data from a json file in the application data directory.

Windows 7+: `C:\Users\{username}\AppData\Local\ePyCom\bossfight\client_config.json`

