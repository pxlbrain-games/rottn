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

    *time_order_index* should be in alignment with the servers current update counter.
    '''

    def __init__(self, time_order_index=0, game_status=GameStatus().Paused):
        self.game_status = game_status
        self.time_order_index = time_order_index

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

    def __init__(self, time_order_index: int, **kwargs):
        self.__dict__ = kwargs
        self.time_order_index = time_order_index

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
        if self.time_order_index > other.time_order_index:
            other.__dict__.update(self.__dict__)
        return other

    # Check time ordering
    def __lt__(self, other):
        return self.time_order_index < other.time_order_index

    def __gt__(self, other):
        return self.time_order_index > other.time_order_index

class PlayerAction(Sendable):
    '''
    An update the player sends to the server about the actions of it's character.
    Any collision events involving the player character are processed client-side and sent as
    *PlayerAction*s to the server. The server will validate a client's *PlayerAction* and
    respond with an *OutOfSync* error, if it doesn't add up with the server-side game state.
    '''
    pass
