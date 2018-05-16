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
    body = None
- *PostPlayerActionRequest*: As client post a player action to the *GameService*.
    body = *PlayerAction*
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
GameServicePackage(self, package_type:bossfight.core.gameServiceProtocol.PackageType, body:bossfight.core.mixins.Sendable=None)
```

Contains *header* and *body* as attributes. The header contains information about the the
package type and body. The body is some object of a core class like *ErrorMessage*,
*SharedGameState*, *SharedGameStateUpdate* or *PlayerAction*.

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

