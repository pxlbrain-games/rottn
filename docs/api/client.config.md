<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.config">bossfight.client.config</h1>


Module that manages access to the clients configuration. Contains the *Config* class,
which acts as an interface to a singleton config data state in memory and deals with
saving/loading the client config on/from disk.

<h2 id="bossfight.client.config.Config">Config</h2>

```python
Config(self)
```

Singleton class that stores all the client configuration info.
You can create as many instances as you like, they all will refer to the same config data.

<h3 id="bossfight.client.config.Config.get_default">get_default</h3>

```python
Config.get_default()
```

Returns a deep copy of the default configuration dictionary.

<h3 id="bossfight.client.config.Config.revert_to_default">revert_to_default</h3>

```python
Config.revert_to_default(self)
```

Reverts config data to the default configuration defined in *DEFAULT_CONFIG*.

<h3 id="bossfight.client.config.Config.save">save</h3>

```python
Config.save(self)
```

Saves the client configuration data in a json file in the application data directory.

Windows 7+: `C:\Users\{username}\AppData\Local\ePyCom\bossfight\client_config.json`

<h3 id="bossfight.client.config.Config.load">load</h3>

```python
Config.load(self)
```

Loads the client configuration data from a json file in the application data directory.

Windows 7+: `C:\Users\{username}\AppData\Local\ePyCom\bossfight\client_config.json`

