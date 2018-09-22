# -*- coding: utf-8 -*-
'''
This module introduces bases classes for characters that client and server
can subclass in order to create their respective versions of enemies, players
and other NPCs.
'''

class Character:
    '''
    Base class for any kind of character in the game.
    '''

    def __init__(self, name, position):
        super().__init__() #for cooperative multiple inheritance
        self.name = name
        self.position = position
        self.velocity = (0, 0)
        self.direction = (0, 1)
        self.damage = 0

class PlayerCharacter(Character):
    '''
    A type that describes a player character in the game world
    '''
    def __init__(self, player_id, name, position=(0, 0)):
        super().__init__(name, position)
        self.player_id = player_id

class NonPlayerCharacter(Character):
    '''
    A type that describes an enemy in the game world
    '''
    def __init__(self, npc_id, name, position=(0, 0)):
        super().__init__(name, position)
        self.npc_id = npc_id
