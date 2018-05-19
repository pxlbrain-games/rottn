# -*- coding: utf-8 -*-
'''
Module that defines the network protocol which *GameServiceConnection*s and *GamerService*s use
to communicate. It contains the *GameServicePackage* class, which represents a unit of information
that client and server can exchange with each other, as well as classes that make up parts
of a package.
'''

import sys
from bossfight.core.sharedGameData import SharedGameState, SharedGameStateUpdate, PlayerAction
# SharedGameState is not used explicitely, but it needs to be findable
# via 'getattr()' in 'GameServicePackage.from_datagram()'!
from bossfight.core.mixins import Sendable

# Unique 4-byte token to mark the end of the header of a GameServicePackage
_HEADER_END_TOKEN = bytes.fromhex('b5968459')

class PackageType:
    '''
    Enum class with the following values:
    - *GetSharedGameStateRequest*: As client request the full shared game state from the server.
        body = None
    - *GetGameStateUpdateRequest*: As client request all polled game state updates.
        body = *SharedGameStateUpdate*
    - *PostPlayerActionRequest*: As client post a player action to the *GameService*.
        body = *PlayerAction*
    - *GameServiceResponse*: As server respond to a client request.
        body = request-dependent
    - *GameServiceError*: As server report an error to the client.
        body = *ErrorMessage*
    '''
    @property
    def GetSharedGameStateRequest(self):
        return 1
    @property
    def GetGameStateUpdateRequest(self):
        return 2
    @property
    def PostPlayerActionRequest(self):
        return 3
    @property
    def GameServiceResponse(self):
        return 4
    @property
    def GameServiceError(self):
        return 5

class ErrorType:
    '''
    Enum class with the following values:
    - *RequestTimeout*: Server response took to long.
    - *UnpackError*: Request or response bytepack corrupted.
    - *RequestInvalid*: Server could not handle the request.

    To be used as part of an *ErrorMessage* object in a *GameServiceError* package.
    '''
    @property
    def RequestTimeout(self):
        return 1
    @property
    def UnpackError(self):
        return 2
    @property
    def RequestInvalid(self):
        return 3

class ErrorMessage(Sendable):
    '''
    The sendable type *ErrorMessage* is used for the body of *GameServicePackage*s with
    *package_type* *PackageType().GameServiceError* in their *header*.
    '''
    def __init__(self, error_type=ErrorType().RequestInvalid, message=''):
        self.error_type = error_type
        self.message = message

class _GameServicePackageHeader(Sendable):
    def __init__(self, package_type=PackageType().GameServiceResponse, body_type='NoneType'):
        self.package_type = package_type
        self.body_type = body_type

    '''
    Override 'object' members
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.package_type == other.package_type and self.body_type == other.body_type
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class GameServicePackage:
    '''
    Contains *header* and *body* as attributes. The header contains information about the the
    package type and body. The body is some object of a core class like *ErrorMessage*,
    *SharedGameState*, *SharedGameStateUpdate* or *PlayerAction*.
    '''
    def __init__(self, package_type: PackageType, body: Sendable = None):
        self.header = _GameServicePackageHeader(package_type, body.__class__.__name__)
        self.body = body

    def to_datagram(self):
        '''
        Returns a bytepacked datagram representing the GameServicePackage.
        '''
        self.header.body_type = self.body.__class__.__name__
        datagram = bytearray(self.header.to_bytes())
        datagram.extend(_HEADER_END_TOKEN)
        if self.body != None:
            datagram.extend(self.body.to_bytes())
        return bytes(datagram)

    @staticmethod
    def from_datagram(datagram: bytes):
        '''
        Unpacks the given bytepacked datagram and returns it's content as a *GameServicePackage*
        object.
        '''
        datagram = datagram.split(_HEADER_END_TOKEN)
        header = _GameServicePackageHeader.from_bytes(datagram[0])
        if header.body_type != 'NoneType':
            body = getattr(sys.modules[__name__], header.body_type).from_bytes(datagram[1])
        else:
            body = None
        return GameServicePackage(header.package_type, body)

    def is_response(self):
        '''
        Returns *True* if the package is of package type *GameServiceResponse*.
        '''
        return self.header.package_type == PackageType().GameServiceResponse

    def is_error(self):
        '''
        Returns *True* if the package is of package type *GameServiceError*.
        '''
        return self.header.package_type == PackageType().GameServiceError

    def is_update_request(self):
        '''
        Returns *True* if the package is of package type *GetGameStateUpdateRequest*.
        '''
        return self.header.package_type == PackageType().GetGameStateUpdateRequest

    def is_state_request(self):
        '''
        Returns *True* if the package is of package type *GetSharedGameStateRequest*.
        '''
        return self.header.package_type == PackageType().GetSharedGameStateRequest

    '''
    Override object members
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.header == other.header and self.body == other.body
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

def timeout_error(message=''):
    '''
    Returns a *GameServicePackage* with package type *GameServiceError*,
    error type *RequestTimeout* and *message* as error message.
    '''
    return GameServicePackage(
        package_type=PackageType().GameServiceError,
        body=ErrorMessage(
            error_type=ErrorType().RequestTimeout,
            message=message
        )
    )

def unpack_error(message=''):
    '''
    Returns a *GameServicePackage* with package type *GameServiceError*,
    error type *UnpackError* and *message* as error message.
    '''
    return GameServicePackage(
        package_type=PackageType().GameServiceError,
        body=ErrorMessage(
            error_type=ErrorType().UnpackError,
            message=message
        )
    )

def request_invalid_error(message=''):
    '''
    Returns a *GameServicePackage* with package type *GameServiceError*,
    error type *RequestInvalid* and *message* as error message.
    '''
    return GameServicePackage(
        package_type=PackageType().GameServiceError,
        body=ErrorMessage(
            error_type=ErrorType().RequestInvalid,
            message=message
        )
    )

def game_state_request():
    '''
    Returns a *GameServicePackage* with package type *GetSharedGameStateRequest*.
    '''
    return GameServicePackage(
        package_type=PackageType().GetSharedGameStateRequest
    )

def game_state_update_request(time_order: int):
    '''
    Returns a *GameServicePackage* with package type *GetGameStateUpdateRequest*.
    Enter the *time_order* attribute of the client's last known *SharedGameState*.
    '''
    return GameServicePackage(
        package_type=PackageType().GetGameStateUpdateRequest,
        body=SharedGameStateUpdate(
            time_order=time_order
        )
    )

def post_action_request(player_action: PlayerAction):
    '''
    Returns a *GameServicePackage* with package type *PostPlayerActionRequest* with
    the given *PlayerAction* object as it's body.
    '''
    return GameServicePackage(
        package_type=PackageType().PostPlayerActionRequest,
        body=player_action
    )

def response(body: Sendable):
    '''
    Returns a *GameServicePackage* with package type *GameServiceResponse*.
    '''
    return GameServicePackage(
        package_type=PackageType().GameServiceResponse,
        body=body
    )
