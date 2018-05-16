# -*- coding: utf-8 -*-
'''
This module contains classes for game objects that are relevant for both client and server.
Client as well as server are supposed to define subclasses of the classes in this module,
that extend those types with data and functionality, that is client-/server-specific.
'''

from bossfight.core.mixins import Sendable

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

class SharedGameState(Sendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Since it is a *Sendable*, it can only contain basic python types as attributes.
    '''

    def __init__(self, game_status=GameStatus().Paused):
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
