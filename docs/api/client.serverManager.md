<h1 id="bossfight.client">bossfight.client</h1>


<h1 id="bossfight.client.serverManager">bossfight.client.serverManager</h1>


A module that helps with running and maintaining bossfight.server processes.

<h2 id="bossfight.client.serverManager.get_running_processes">get_running_processes</h2>

```python
get_running_processes()
```

Returns an iterable list of *pid*s of running server processes.

<h2 id="bossfight.client.serverManager.get_available_ip_addresses">get_available_ip_addresses</h2>

```python
get_available_ip_addresses()
```

Returns a list of all available IP addresses that the server can be bound to.
Keep in mind that `127.0.0.1` is only suitable for local servers.

<h2 id="bossfight.client.serverManager.run_server">run_server</h2>

```python
run_server(ip_address='localhost', port=0)
```

Starts a server bound to the specified address and return the process ID.

<h2 id="bossfight.client.serverManager.get_ip_address">get_ip_address</h2>

```python
get_ip_address(pid)
```

Returns the the IP address of the server running under ther process ID *pid*.

<h2 id="bossfight.client.serverManager.get_port">get_port</h2>

```python
get_port(pid)
```

Returns the the port of the server running under ther process ID *pid*.

<h2 id="bossfight.client.serverManager.shutdown">shutdown</h2>

```python
shutdown(pid)
```

Terminates the server process with process ID *pid*.

<h2 id="bossfight.client.serverManager.clean_up">clean_up</h2>

```python
clean_up()
```

Terminates all running server processes.

