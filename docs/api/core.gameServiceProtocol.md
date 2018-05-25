<h1 id="bossfight.core">bossfight.core</h1>


<h1 id="bossfight.core.gameServiceProtocol">bossfight.core.gameServiceProtocol</h1>


Module that defines the network protocol which *GameServiceConnection*s and *GamerService*s use
to communicate. It contains the *GameServicePackage* class, which represents a unit of information
that client and server can exchange with each other, as well as classes that make up parts
of a package.

<h2 id="bossfight.core.gameServiceProtocol.PackageType">PackageType</h2>

```python
PackageType(self, /, *args, **kwargs)
```

Enum class with the following values:
- *GetSharedGameStateRequest*: As client request the full shared game state from the server.
    body = None
- *GetGameStateUpdateRequest*: As client request all polled game state updates.
    body = *SharedGameStateUpdate* (purely for time-ordering)
- *PostClientActivityRequest*: As client post client-side activity to the *GameService*.
    body = *ClientActivity*
- *GameServiceResponse*: As server respond to a client request.
    body = request-dependent
- *GameServiceError*: As server report an error to the client.
    body = *ErrorMessage*

<h2 id="bossfight.core.gameServiceProtocol.ErrorType">ErrorType</h2>

```python
ErrorType(self, /, *args, **kwargs)
```

Enum class with the following values:
- *RequestTimeout*: Server response took to long.
- *UnpackError*: Request or response bytepack corrupted.
- *RequestInvalid*: Server could not handle the request.

To be used as part of an *ErrorMessage* object in a *GameServiceError* package.

<h2 id="bossfight.core.gameServiceProtocol.ErrorMessage">ErrorMessage</h2>

```python
ErrorMessage(self, error_type=3, message='')
```

The sendable type *ErrorMessage* is used for the body of *GameServicePackage*s with
*package_type* *PackageType().GameServiceError* in their *header*.

<h2 id="bossfight.core.gameServiceProtocol.GameServicePackage">GameServicePackage</h2>

```python
GameServicePackage(self, package_type:bossfight.core.gameServiceProtocol.PackageType, body:bossfight.core.sharedGameData.Sendable=None)
```

Contains *header* and *body* as attributes. The header contains information about the the
package type and body. The body is some object of a core class like *ErrorMessage*,
*SharedGameState*, *SharedGameStateUpdate* or *ClientActivity*.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.from_datagram">from_datagram</h3>

```python
GameServicePackage.from_datagram(datagram:bytes)
```

Unpacks the given bytepacked datagram and returns it's content as a *GameServicePackage*
object.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.to_datagram">to_datagram</h3>

```python
GameServicePackage.to_datagram(self)
```

Returns a bytepacked datagram representing the GameServicePackage.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.is_response">is_response</h3>

```python
GameServicePackage.is_response(self)
```

Returns *True* if the package is of package type *GameServiceResponse*.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.is_error">is_error</h3>

```python
GameServicePackage.is_error(self)
```

Returns *True* if the package is of package type *GameServiceError*.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.is_update_request">is_update_request</h3>

```python
GameServicePackage.is_update_request(self)
```

Returns *True* if the package is of package type *GetGameStateUpdateRequest*.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.is_state_request">is_state_request</h3>

```python
GameServicePackage.is_state_request(self)
```

Returns *True* if the package is of package type *GetSharedGameStateRequest*.

<h3 id="bossfight.core.gameServiceProtocol.GameServicePackage.is_post_activity_request">is_post_activity_request</h3>

```python
GameServicePackage.is_post_activity_request(self)
```

Returns *True* if the package is of package type *PostClientActivityRequest*.

<h2 id="bossfight.core.gameServiceProtocol.timeout_error">timeout_error</h2>

```python
timeout_error(message='')
```

Returns a *GameServicePackage* with package type *GameServiceError*,
error type *RequestTimeout* and *message* as error message.

<h2 id="bossfight.core.gameServiceProtocol.unpack_error">unpack_error</h2>

```python
unpack_error(message='')
```

Returns a *GameServicePackage* with package type *GameServiceError*,
error type *UnpackError* and *message* as error message.

<h2 id="bossfight.core.gameServiceProtocol.request_invalid_error">request_invalid_error</h2>

```python
request_invalid_error(message='')
```

Returns a *GameServicePackage* with package type *GameServiceError*,
error type *RequestInvalid* and *message* as error message.

<h2 id="bossfight.core.gameServiceProtocol.game_state_request">game_state_request</h2>

```python
game_state_request()
```

Returns a *GameServicePackage* with package type *GetSharedGameStateRequest*.

<h2 id="bossfight.core.gameServiceProtocol.game_state_update_request">game_state_update_request</h2>

```python
game_state_update_request(time_order:int)
```

Returns a *GameServicePackage* with package type *GetGameStateUpdateRequest*.
Enter the *time_order* attribute of the client's last known *SharedGameState*.

<h2 id="bossfight.core.gameServiceProtocol.post_activity_request">post_activity_request</h2>

```python
post_activity_request(client_activity:bossfight.core.sharedGameData.ClientActivity)
```

Returns a *GameServicePackage* with package type *PostClientActivityRequest* with
the given *ClientActivity* object as it's body.

<h2 id="bossfight.core.gameServiceProtocol.response">response</h2>

```python
response(body:bossfight.core.sharedGameData.Sendable)
```

Returns a *GameServicePackage* with package type *GameServiceResponse*.

