# -*- coding: utf-8 -*-

import sys
from enum import IntEnum
import umsgpack
from bossfight.core.sharedGameData import ISendable, SharedGameState

# Unique 4-byte token to mark the end of the header of a GameServicePackage
_HEADER_END_TOKEN = bytes.fromhex('b5968459')

class PackageType(IntEnum):
    '''
    Enum class with the following values:
    - *GetSharedGameStateRequest*: As client request the full shared game state from the server. body=None
    - *GetGameStateUpdateRequest*: As client request all polled game state updates. body=None
    - *PostPlayerActionRequest*: As client post a player action to the GameService. body=PlayerAction object
    - *GameServiceResponse*: As server respond to a client request. body=request-dependent
    - *GameServiceError*: As server report an error to the client. body=ErrorMessage
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

class ErrorMessage(ISendable):
    def __init__(self, error_type:ErrorType, message=''):
        self.error_type = error_type
        self.message = message
    
    '''
    Implement ISendable
    '''
    @staticmethod
    def from_bytes(bytepack:bytes):
        receivedError = umsgpack.unpackb(bytepack)
        try:
            return ErrorMessage(
                error_type=receivedError['error_type'],
                message=receivedError['message'])
        except KeyError:
            raise TypeError('Bytes could no be parsed into ErrorMessage.')

class _GameServicePackageHeader(ISendable):
    def __init__(self, package_type:PackageType, body_type:str):
        self.package_type = package_type
        self.body_type = body_type
    
    '''
    Implementation of ISendable interface
    '''
    @staticmethod
    def from_bytes(bytepack:bytes):
        receivedHeader = umsgpack.unpackb(bytepack)
        try:
            return _GameServicePackageHeader(
                package_type=receivedHeader['package_type'],
                body_type=receivedHeader['body_type'])
        except KeyError:
            raise TypeError('Bytes could no be parsed into _GameServicePackageHeader.')
    
    '''
    Override object members
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.package_type == other.package_type and self.body_type == other.body_type
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

class GameServicePackage:
    '''
    Contains *header* and *body* as attributes. The header contains information about the the package type and body.
    The body is some object of a core class like *ErrorMessage*, *SharedGameState*, *SharedGameStateUpdate*
    or *PlayerAction*.
    '''
    def __init__(self, package_type:PackageType, body:ISendable=None):
        self.header = _GameServicePackageHeader(package_type, body.__class__.__name__)
        self.body = body
       
    def to_datagram(self):
        '''
        Returns a bytepacked datagram representing the GameServicePackage.
        '''
        self.header.body_type = self.body.__class__.__name__
        datagram = bytearray(self.header.to_bytes())
        datagram.extend(_HEADER_END_TOKEN)
        if self.body != None: datagram.extend(self.body.to_bytes())
        return bytes(datagram)
    
    @staticmethod
    def from_datagram(datagram:bytes):
        '''
        Unpacks the given bytepacked datagram and returns it's content as a *GameServicePackage* object.
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