# -*- coding: utf-8 -*-
'''
This module deals with animated sprites for characters.
'''

import enum
import math
import euclid3 as euclid
import pyglet
import cocos

class AnimationState(enum.IntEnum):
    Idle = 1
    Running = 2
    Blocking = 3

class DirectionState(enum.IntEnum):
    Left = 8
    LeftUp = 7
    Up = 6
    RightUp = 5
    Right = 4
    RightDown = 3
    Down = 2
    LeftDown = 1

class CharacterPart(enum.IntEnum):
    Body = 1
    Head = 2

class AnimatedCharacter(cocos.batch.BatchableNode):
    def __init__(self, moving_parent, body_spritesheet='clothes.png', head_spritesheet='male_head1.png', scale=2.5):
        super().__init__()
        '''
        spritesheet-schema:
        rows - 1: left-down, 2: down, 3: right-down, 4: right,
            5: right-up, 6: up, 7: left-up, 8: left
        columns - 1-4: idle, 5-12: run, 13-16: hit, 17-18: block
            19-24: fall, 25-28: cast, 29-32: shoot
        '''
        self.sprites = dict()
        self.animation_state = AnimationState.Idle
        self.direction_state = DirectionState.Up
        self.moving_parent = moving_parent

        clothes_spritesheet = pyglet.image.ImageGrid(
            pyglet.resource.image(body_spritesheet), 8, 32
        )
        head_spritesheet = pyglet.image.ImageGrid(
            pyglet.resource.image(head_spritesheet), 8, 32
        )
        idle_sprites = {
            CharacterPart.Body: create_animated_sprites(clothes_spritesheet, 0, 3, 0.2, scale),
            CharacterPart.Head: create_animated_sprites(head_spritesheet, 0, 3, 0.2, scale)
        }
        running_sprites = {
            CharacterPart.Body: create_animated_sprites(clothes_spritesheet, 4, 11, 0.09, scale),
            CharacterPart.Head: create_animated_sprites(head_spritesheet, 4, 11, 0.09, scale)
        }
        self.sprites[AnimationState.Idle] = idle_sprites
        for character_part in CharacterPart:
            for direction_state, sprite in self.sprites[AnimationState.Idle][character_part].items():
                self.add(sprite)
                if direction_state != self.direction_state:
                    sprite.visible = False
        self.sprites[AnimationState.Running] = running_sprites
        for character_part in CharacterPart:
            for sprite in self.sprites[AnimationState.Running][character_part].values():
                self.add(sprite)
                sprite.visible = False
        self.schedule(self.update_direction)
        self.schedule(self.update_animation_state)

    def update_direction(self, dt):
        # This should always be direction, but direction of other players is not
        # part of the game state and player movement client activity yet.
        direction = self.moving_parent.direction #\
        #    if self.moving_parent.__class__ == player_controls.ControllableNode \
        #    else self.moving_parent.velocity
        if direction != (0, 0):
            new_direction_state = int((math.atan2(direction[1], direction[0])*4/math.pi + 7/2) + 1)
            if new_direction_state == 0:
                new_direction_state = 8
            if new_direction_state != self.direction_state:
                parts = {CharacterPart.Body, CharacterPart.Head}
                for part in parts:
                    self.sprites[self.animation_state][part][self.direction_state].visible = False
                    self.sprites[self.animation_state][part][new_direction_state].visible = True
                self.direction_state = new_direction_state

    def update_animation_state(self, dt):
        v_squared = euclid.Vector2(
            self.moving_parent.velocity[0], self.moving_parent.velocity[1]
        ).magnitude_squared()
        if v_squared > 30 and self.animation_state == AnimationState.Idle:
            for part in CharacterPart:
                self.sprites[self.animation_state][part][self.direction_state].visible = False
                self.sprites[AnimationState.Running][part][self.direction_state].visible = True
            self.animation_state = AnimationState.Running
        elif v_squared < 30 and self.animation_state == AnimationState.Running:
            for part in CharacterPart:
                self.sprites[self.animation_state][part][self.direction_state].visible = False
                self.sprites[AnimationState.Idle][part][self.direction_state].visible = True
            self.animation_state = AnimationState.Idle

### These are just helper functions for the isometric_hero spritesheet:

def create_animation(image_grid, row, start, end, duration=0.1):
    frames = []
    for i in range(start, end):
        frames.append(pyglet.image.AnimationFrame(image_grid[i+row*32], duration))
    return pyglet.image.Animation(frames)

def create_animated_sprites(spritesheet, start, end, duration=0.1, scale=1):
    animations = [
        create_animation(spritesheet, i, start, end, duration) for i in range(0,8)
    ]
    sprites = {
        i: cocos.sprite.Sprite(image=animations[i-1], position=(0, 75), scale=scale) \
        for i in range(1,9)
    }
    return sprites
