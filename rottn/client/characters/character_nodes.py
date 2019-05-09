# -*- coding: utf-8 -*-
"""
This module contains the clients subclasses of the core
character types.
"""

import cocos
from rottn.core import character_bases
from rottn.client import player_controls
from rottn.client.characters import character_animations

class CharacterNode(cocos.cocosnode.CocosNode):

    def __init__(self):
        super().__init__()
        self.velocity = (0, 0)

    def move_state_update(self, new_state, dt):
        vx = (new_state["position"][0] - self.position[0]) / dt
        vy = (new_state["position"][1] - self.position[1]) / dt
        ax = (new_state["velocity"][0] - self.velocity[0] + 0.11 * vx) / dt
        ay = (new_state["velocity"][1] - self.velocity[1] + 0.11 * vy) / dt
        self.acceleration = (ax, ay)
        self.direction = new_state["direction"]

class PlayerNode(character_bases.PlayerCharacter, CharacterNode):
    """
    A **CocosNode** that represents a player in the game world.
    """

    def __init__(self, name_or_state):
        super().__init__(name_or_state)
        self.name_label = cocos.text.Label(
            text=self.name,
            position=(0, 120),
            font_name="Arial",
            font_size=24,
            anchor_x="center",
            anchor_y="center",
        )
        self.add(self.name_label)
        self.animated_character = character_animations.AnimatedCharacter(
            moving_parent=self,
            weapon_spritesheet="shortsword.png",
            shield_spritesheet="buckler.png",
        )
        self.add(self.animated_character)
        self.do(cocos.actions.Move())


class LocalPlayerNode(PlayerNode, player_controls.ControllableNode):
    """
    A special kind of **PlayerNode** that reacts to player inputs.
    """

    def __init__(self, name, position=(0, 0)):
        super().__init__(name)
        self.position = position


class NPCNode(character_bases.NonPlayerCharacter, CharacterNode):
    def __init__(self, name_or_state):
        super().__init__(name_or_state)
        self.animated_character = character_animations.AnimatedCharacter(
            moving_parent=self,
            body_spritesheet="steel_armor.png",
            head_spritesheet="male_head3.png",
            weapon_spritesheet="longsword.png",
            shield_spritesheet="shield.png",
            scale=2.8,
        )
        self.add(self.animated_character)
        self.do(cocos.actions.Move())
