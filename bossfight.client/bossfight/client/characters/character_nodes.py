# -*- coding: utf-8 -*-
'''
This module contains the clients subclasses of the core
character types.
'''

import cocos
import bossfight.core.activities as activities
import bossfight.core.character_bases as character_bases
import bossfight.client.player_controls as player_controls
import bossfight.client.characters.character_animations as character_animations

class PlayerNode(character_bases.PlayerCharacter, cocos.cocosnode.CocosNode):
    '''
    A **CocosNode** that represents a player in the game world.
    '''

    def __init__(self, player_id, name, position=(0, 0)):
        super().__init__(player_id, name, position)
        self.name_label = cocos.text.Label(
            text=name,
            position=(0, 120),
            font_name='Arial',
            font_size=24,
            anchor_x='center',
            anchor_y='center'
        )
        self.add(self.name_label)
        self.animated_character = character_animations.AnimatedCharacter(self)
        self.add(self.animated_character)
        self.do(cocos.actions.Move())


class LocalPlayerNode(PlayerNode, player_controls.ControllableNode):
    '''
    A special kind of **PlayerNode** that reacts to player inputs.
    '''

    def __init__(self, player_id, name, position=(0, 0)):
        super().__init__(player_id, name, position)

    def get_move_activity(self, time_order):
        return activities.move_player_activity(
            self.player_id,
            self.position,
            self.velocity,
            self.direction,
            time_order
        )

class TestEnemyNode(character_bases.NonPlayerCharacter, cocos.cocosnode.CocosNode):
    def __init__(self):
        super().__init__(0, 'Test Enemy')
        '''
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
        '''
        self.animated_character = character_animations.AnimatedCharacter(
            moving_parent=self,
            body_spritesheet='steel_armor.png',
            head_spritesheet='male_head3.png',
            scale=2.8
        )
        self.add(self.animated_character)
        self.do(cocos.actions.Move())
