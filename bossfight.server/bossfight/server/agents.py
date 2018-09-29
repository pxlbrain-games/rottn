# -*- coding: utf-8 -*-

import bossfight.core.character_bases as character_bases

class TestEnemyAgent(character_bases.NonPlayerCharacter):
    def __init__(self, name):
        super().__init__(name)
        self.action_space = {'TurnLeft', 'TurnRight', 'StraightAhead'}
