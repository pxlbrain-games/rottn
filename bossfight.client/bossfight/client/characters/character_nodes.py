# -*- coding: utf-8 -*-
"""
This module contains the clients subclasses of the core
character types.
"""

import cocos
from bossfight.core import character_bases
from bossfight.client import player_controls
from bossfight.client.characters import character_animations


class PlayerNode(character_bases.PlayerCharacter, cocos.cocosnode.CocosNode):
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


class NPCNode(character_bases.NonPlayerCharacter, cocos.cocosnode.CocosNode):
    def __init__(self, name_or_state):
        super().__init__(name_or_state)
        """
        fireball_spritesheet = pyglet.image.ImageGrid(
            pyglet.resource.image('fireball.png'), 1, 4
        )
        fireball_animation = pyglet.image.Animation.from_image_sequence(fireball_spritesheet, 0.1)
        self.sprite = cocos.sprite.Sprite(
            image=fireball_animation,
            position=(0, 50),
            scale=2.5
        )
        self.add(self.sprite) Vector2
        """
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
