# -*- coding: utf-8 -*-
'''
This module contains classes for all kinds of game objects that are relevant for both client and server.
Client as well as server are supposed to define subclasses of the classes in this module,
that extend those types with data and functionality, that is client-/server-specific.
'''

from enum import IntEnum
from bossfight.core.mixins import Sendable

class GameStatus(IntEnum):
    '''
    Enum class with the values:
    - *Paused*
    - *Active*
    '''
    Paused = 1
    Active = 2

class SharedGameState(Sendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Since it is a *Sendable*, it can only contain basic python types as attributes.
    '''

    def __init__(self, game_status=GameStatus.Paused):
        self.game_status = game_status

    '''
    Overrides of 'object' member functions
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_status == other.game_status
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
