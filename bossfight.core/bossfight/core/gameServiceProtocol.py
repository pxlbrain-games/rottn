# -*- coding: utf-8 -*-
'''
Module that defines the network protocol, which *GameServiceConnection*s and *GamerService*s use
to communicate. It contains the *GameServicePackage* class, which represents a unit of information
that client and server can exchange with each other, as well as classes that make up parts
of a package.
'''

import sys
from enum import IntEnum
from bossfight.core.sharedGameData import SharedGameState
# SharedGameState is not used explicitely, but it needs to be findable
# via 'getattr()' in 'GameServicePackage.from_datagram()'!
from bossfight.core.mixins import Sendable

# Unique 4-byte token to mark the end of the header of a GameServicePackage
_HEADER_END_TOKEN = bytes.fromhex('b5968459')

class PackageType(IntEnum):
    '''
    Enum class with the following values:
    - *GetSharedGameStateRequest*: As client request the full shared game state from the server.
        body=None
    - *GetGameStateUpdateRequest*: As client request all polled game state updates.
        body=None
    - *PostPlayerActionRequest*: As client post a player action to the GameService.
        body=*PlayerAction* object
    - *GameServiceResponse*: As server respond to a client request.
        body=request-dependent
    - *GameServiceError*: As server report an error to the client.
        body=*ErrorMessage* object
    '''
    GetSharedGameStateRequest = 1
    GetGameStateUpdateRequest = 2
    PostPlayerActionRequest = 3
    GameServiceResponse = 4
    GameServiceError = 5

class ErrorType(IntEnum):
    '''
    Enum class with the following values:
    - *RequestTimeout*: Server response took to long.
    - *UnpackError*: Request or response bytepack corrupted.
    - *RequestInvalid*: Server could not handle the request.

    To be used as part of an *ErrorMessage* object in a *GameServiceError* package.
    '''
    RequestTimeout = 1
    UnpackError = 2
    RequestInvalid = 3

class ErrorMessage(Sendable):
    '''
    The sendable type *ErrorMessage* is used for the body of *GameServicePackage*s with
    *package_type* *PackageType.GameServiceError* in their *header*.
    '''
    def __init__(self, error_type=ErrorType.RequestInvalid, message=''):
        self.error_type = error_type
        self.message = message

class _GameServicePackageHeader(Sendable):
    def __init__(self, package_type=PackageType.GameServiceResponse, body_type='NoneType'):
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

    '''
    Override object members
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.header == other.header and self.body == other.body
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
