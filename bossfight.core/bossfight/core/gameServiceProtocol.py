# -*- coding: utf-8 -*-

import sys
from enum import IntEnum
import umsgpack
from bossfight.core.sharedGameData import ISendable, SharedGameState

class PackageType(IntEnum):
    GetSharedGameStateRequest = 1
    GetGameStateUpdateRequest = 2
    PostPlayerActionRequest = 3
    GameServiceResponse = 4
    GameServiceError = 5

# Unique 4-byte token to mark the end of the header of a GameServicePackage
_HEADER_END_TOKEN = bytes.fromhex('b5968459')

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
    Contains `.header` and `.body` attributes. The header contains information about the request, the body and the client.
    The body is some object of a core class like `SharedGameState`, `SharedGameStateUpdate` or `PlayerAction`.
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
        Unpacks the given bytepacked datagram and returns it's content as a GameServicePackage object.
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