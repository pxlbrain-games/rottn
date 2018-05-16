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

