# -*- coding: utf-8 -*-

import sys
from enum import IntEnum
import umsgpack

class RequestType(IntEnum):
    GetSharedGameState = 1
    PostPlayerAction = 2

# Unique 6-byte tokens to mark the end of the header of a GameServiceRequest and the request itself:
_HEADER_END_TOKEN = bytes.fromhex('577160bd0672')
_REQUEST_END_TOKEN = bytes.fromhex('9be4ac9ca4b3')

class ISendable:
    '''
    Interface for objects that are supposed to be sendable as part of a server request.
    Inheriting classes must implement `_readDatagram(dgram_socket_filestream)` and possibly `_writeDatagram(self, dgram_socket_filestream)`.
    The arguments are file-like binary streams. `_readDatagram()` should be static and return an instance of the inheriting class.
    '''

    def _writeDatagram(self, dgram_socket_filestream):
        '''
        Writes the object into a file-like binary stream that supports `.write()`, e.g. one returned by `socket.makefile()`.
        Override this, if simple __dict__ serialization is insufficient.
        '''
        umsgpack.pack(self.__dict__, dgram_socket_filestream)

    @staticmethod
    def _readDatagram(dgram:bytes) -> object:
        '''Reads a file-like binary stream that supports `.read()`, e.g. one returned by `socket.makefile()`, and returns it's content as an instance of the inheriting class.'''
        raise NotImplementedError

class _GameServiceRequestHeader(ISendable):
    def __init__(self, request_type:RequestType, body_class:str):
        self.request_type = request_type
        self.body_class = body_class
    
    @staticmethod
    def _readDatagram(dgram:bytes):
        receivedHeader = umsgpack.unpackb(dgram)
        try:
            return _GameServiceRequestHeader(
                request_type=receivedHeader['request_type'],
                body_class=receivedHeader['body_class'])
        except KeyError:
            raise TypeError('Read datagram could no be parsed to _GameServiceRequestHeader.')


class GameServiceRequest:
    def __init__(self, request_type:RequestType, body:ISendable=None):
        self._header = _GameServiceRequestHeader(request_type, body.__class__.__name__)
        self.request_type = request_type
        self.body = body
    
    def send(self, dgram_socket_filestream):
        self._header._writeDatagram(dgram_socket_filestream)
        dgram_socket_filestream.write(_HEADER_END_TOKEN)
        self.body._writeDatagram(dgram_socket_filestream)
        dgram_socket_filestream.write(_REQUEST_END_TOKEN)
        dgram_socket_filestream.flush()
    
    @staticmethod
    def receive(dgram_socket_filestream):
        data = bytearray()
        while _REQUEST_END_TOKEN not in data:
            data.extend(dgram_socket_filestream.read(6))
        data = data.rstrip(_REQUEST_END_TOKEN).split(_HEADER_END_TOKEN)
        header = _GameServiceRequestHeader._readDatagram(data[0])
        body = getattr(sys.modules[__name__], header.body_class)._readDatagram(data[1])
        return GameServiceRequest(header.request_type, body)