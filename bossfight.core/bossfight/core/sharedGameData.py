# -*- coding: utf-8 -*-
'''
This module contains classes for game objects that are relevant for both client and server.
Client as well as server are supposed to define subclasses of the classes in this module,
that extend those types with data and functionality, that is client-/server-specific.
'''

import umsgpack

class Sendable:
    '''
    Mixin for classes that are supposed to be sendable as part of a server request or response.
    Sendables can only have basic Python types as attributes and their constructor needs
    to be callable without passing any arguments.
    '''

    def to_bytes(self):
        '''
        Packs and return a small a binary representation of self.

        '''
        return umsgpack.packb(self.__dict__)

    @classmethod
    def from_bytes(cls, bytepack: bytes):
        '''
        Returns a copy of the object that was packed into byte format.
        '''
        try:
            received_sendable = cls()
            received_sendable.__dict__ = umsgpack.unpackb(bytepack)
            return received_sendable
        except KeyError:
            raise TypeError('Bytes could no be parsed into ' + cls.__name__ + '.')

class GameStatus:
    '''
    Enum class with the values:
    - *Paused*
    - *Active*
    '''
    @property
    def Paused(self):
        return 1
    @property
    def Active(self):
        return 2

class ActionType:
    '''
    Enum class with the values:
    - *PauseGame*
    - *ResumeGame*
    '''
    @property
    def PauseGame(self):
        return 1
    @property
    def ResumeGame(self):
        return 2

class SharedGameState(Sendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Since it is a *Sendable*, it can only contain basic python types as attributes.

    *time_order* should be in alignment with the servers current update counter.
    '''

    def __init__(self, time_order=0, game_status=GameStatus().Paused):
        self.game_status = game_status
        self.time_order = time_order

        ### ONLY FOR TESTING PURPOSES
        self.test_pos = 0

    def is_paused(self):
        '''
        Returns *True* if game status is *Paused*.
        '''
        return self.game_status == GameStatus().Paused

    '''
    Overrides of 'object' member functions
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_status == other.game_status
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class SharedGameStateUpdate(Sendable):
    '''
    Represents a set of changes to carry out on a *SharedGameState*.
    The server should keep an update counter and label all updated with ascending index.

    Keywords are *SharedGameState* atttribute names.

    Use the *+* operator to add *SharedGameStateUpdate*s together or to add them to a
    *SharedGameState* (returning the updated update/state).

    Adding up available updates will always result in an equally or more current but
    also heavier update (meaning it will contain more data).
    '''

    def __init__(self, time_order=0, **kwargs):
        self.__dict__ = kwargs
        self.time_order = time_order

    # Adding to another update should return an updated update
    def __add__(self, other):
        if other > self:
            self.__dict__.update(other.__dict__)
            return self
        else:
            other.__dict__.update(self.__dict__)
            return other

    # Adding to a SharedGameState should update and return the state
    def __radd__(self, other):
        if self.time_order > other.time_order:
            other.__dict__.update(self.__dict__)
        return other

    # Check time ordering
    def __lt__(self, other):
        return self.time_order < other.time_order

    def __gt__(self, other):
        return self.time_order > other.time_order

class PlayerAction(Sendable):
    '''
    An update the player sends to the server about the actions of it's character.
    Any collision events involving the player character are processed client-side and sent as
    *PlayerAction*s to the server. The server will validate a client's *PlayerAction* and
    respond with an *OutOfSync* error, if it doesn't add up with the server-side game state.
    '''
    def __init__(self, action_type=ActionType().PauseGame, action_data={}):
        self.action_type = action_type
        self.action_data = action_data
