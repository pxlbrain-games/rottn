# -*- coding: utf-8 -*-
"""
This module deals with animated sprites for characters.
"""

import enum
import math
import euclid3 as euclid
import pyglet
import cocos


class AnimationState(enum.IntEnum):
    Idle = 1
    Running = 2
    Blocking = 3
    Attacking = 4


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
    Weapon = 3
    Shield = 4


class AnimatedCharacter(cocos.batch.BatchableNode, pyglet.event.EventDispatcher):
    def __init__(
        self,
        moving_parent,
        body_spritesheet="clothes.png",
        head_spritesheet="male_head1.png",
        weapon_spritesheet=None,
        shield_spritesheet=None,
        scale=2.5,
    ):
        super().__init__()
        """
        spritesheet-schema:
        rows - 1: left-down, 2: down, 3: right-down, 4: right,
            5: right-up, 6: up, 7: left-up, 8: left
        columns - 1-4: idle, 5-12: run, 13-16: hit, 17-18: block
            19-24: fall, 25-28: cast, 29-32: shoot
        """
        self.sprites = dict()
        self.animation_state = AnimationState.Idle
        self.direction_state = DirectionState.Up
        self.moving_parent = moving_parent

        body_spritesheet = pyglet.image.ImageGrid(
            pyglet.resource.image(body_spritesheet), 8, 32
        )
        head_spritesheet = pyglet.image.ImageGrid(
            pyglet.resource.image(head_spritesheet), 8, 32
        )
        idle_sprites = {
            CharacterPart.Body: create_animated_sprites(
                body_spritesheet, 0, 3, 0.2, scale
            ),
            CharacterPart.Head: create_animated_sprites(
                head_spritesheet, 0, 3, 0.2, scale
            ),
        }
        running_sprites = {
            CharacterPart.Body: create_animated_sprites(
                body_spritesheet, 4, 11, 0.09, scale
            ),
            CharacterPart.Head: create_animated_sprites(
                head_spritesheet, 4, 11, 0.09, scale
            ),
        }
        attacking_sprites = {
            CharacterPart.Body: create_animated_sprites(
                body_spritesheet, 12, 15, 0.12, scale, False
            ),
            CharacterPart.Head: create_animated_sprites(
                head_spritesheet, 12, 15, 0.12, scale, False
            ),
        }
        if weapon_spritesheet is not None:
            weapon_spritesheet = pyglet.image.ImageGrid(
                pyglet.resource.image(weapon_spritesheet), 8, 32
            )
            idle_sprites[CharacterPart.Weapon] = create_animated_sprites(
                weapon_spritesheet, 0, 3, 0.2, scale
            )
            running_sprites[CharacterPart.Weapon] = create_animated_sprites(
                weapon_spritesheet, 4, 11, 0.09, scale
            )
            attacking_sprites[CharacterPart.Weapon] = create_animated_sprites(
                weapon_spritesheet, 12, 15, 0.12, scale, False
            )
        if shield_spritesheet is not None:
            shield_spritesheet = pyglet.image.ImageGrid(
                pyglet.resource.image(shield_spritesheet), 8, 32
            )
            idle_sprites[CharacterPart.Shield] = create_animated_sprites(
                shield_spritesheet, 0, 3, 0.2, scale
            )
            running_sprites[CharacterPart.Shield] = create_animated_sprites(
                shield_spritesheet, 4, 11, 0.09, scale
            )
            attacking_sprites[CharacterPart.Shield] = create_animated_sprites(
                shield_spritesheet, 12, 15, 0.12, scale, False
            )
        self.sprites[AnimationState.Idle] = idle_sprites
        for character_part in self.sprites[AnimationState.Idle]:
            for direction_state, sprite in self.sprites[AnimationState.Idle][
                character_part
            ].items():
                self.add(sprite)
                if direction_state != self.direction_state:
                    sprite.visible = False
        self.sprites[AnimationState.Running] = running_sprites
        for character_part in self.sprites[AnimationState.Running]:
            for sprite in self.sprites[AnimationState.Running][character_part].values():
                self.add(sprite)
                sprite.visible = False
        self.sprites[AnimationState.Attacking] = attacking_sprites
        for character_part in self.sprites[AnimationState.Attacking]:
            for sprite in self.sprites[AnimationState.Attacking][
                character_part
            ].values():
                self.add(sprite)
                sprite.visible = False
        self.schedule(self._update_direction)
        self.schedule(self._update_animation_state)

    def _update_direction(self, dt):
        direction = self.moving_parent.direction
        if direction != (0, 0):
            new_direction_state = int(
                (math.atan2(direction[1], direction[0]) * 4 / math.pi + 7 / 2) + 1
            )
            if new_direction_state == 0:
                new_direction_state = 8
            if new_direction_state != self.direction_state:
                for character_part in self.sprites[self.animation_state]:
                    self.sprites[self.animation_state][character_part][
                        self.direction_state
                    ].visible = False
                    self.sprites[self.animation_state][character_part][
                        new_direction_state
                    ].visible = True
                self.direction_state = new_direction_state

    def _update_animation_state(self, dt): #pylint: disable=w0613
        v_squared = euclid.Vector2(
            self.moving_parent.velocity[0], self.moving_parent.velocity[1]
        ).magnitude_squared()
        if v_squared > 30 and self.animation_state == AnimationState.Idle:
            for character_part in self.sprites[self.animation_state]:
                self.sprites[self.animation_state][character_part][
                    self.direction_state
                ].visible = False
                self.sprites[AnimationState.Running][character_part][
                    self.direction_state
                ].visible = True
            self.animation_state = AnimationState.Running
        elif v_squared < 30 and self.animation_state == AnimationState.Running:
            for character_part in self.sprites[self.animation_state]:
                self.sprites[self.animation_state][character_part][
                    self.direction_state
                ].visible = False
                self.sprites[AnimationState.Idle][character_part][
                    self.direction_state
                ].visible = True
            self.animation_state = AnimationState.Idle

    def trigger_animation(self, animation_state):
        for character_part in self.sprites[self.animation_state]:
            self.sprites[animation_state][character_part][
                self.direction_state
            ].restart_animation()
            self.sprites[self.animation_state][character_part][
                self.direction_state
            ].visible = False
            self.sprites[animation_state][character_part][
                self.direction_state
            ].visible = True
        self.animation_state = animation_state
        frames = self.sprites[animation_state][CharacterPart.Body][
            self.direction_state
        ]._animation.frames #pylint: disable=w0212
        duration = sum(
            [
                frame.duration if frame.duration is not None else frames[0].duration
                for frame in frames
            ]
        )
        pyglet.clock.schedule_once(self._end_animation, duration)

    def _end_animation(self, dt):
        for character_part in self.sprites[self.animation_state]:
            self.sprites[self.animation_state][character_part][
                self.direction_state
            ].visible = False
            self.sprites[AnimationState.Idle][character_part][
                self.direction_state
            ].visible = True
        self.dispatch_event('on_animation_end', self)
        self.animation_state = AnimationState.Idle

AnimatedCharacter.register_event_type('on_animation_end')

### These are just helper functions for the isometric_hero spritesheet:

def create_animation(image_grid, row, start, end, duration=0.1, loop=True):
    frames = []
    for i in range(start, end + 1):
        frames.append(pyglet.image.AnimationFrame(image_grid[i + row * 32], duration))
    if not loop:
        frames[-1].duration = None
    return pyglet.image.Animation(frames)


def create_animated_sprites(spritesheet, start, end, duration=0.1, scale=1, loop=True):
    animations = [
        create_animation(spritesheet, i, start, end, duration, loop)
        for i in range(0, 8)
    ]
    sprites = {
        i: AnimatedSprite(image=animations[i - 1], position=(0, 75), scale=scale)
        for i in range(1, 9)
    }
    return sprites


### This is a custom pyglet.sprite.Sprite subclass that allows some more interaction with animations


class AnimatedSprite(cocos.sprite.Sprite):
    def restart_animation(self):
        if self._animation is not None:
            pyglet.clock.unschedule(self._animate)
            self._frame_index = 0
            self._texture = self._animation.frames[0].image.get_texture()
            self._next_dt = self._animation.frames[0].duration
            if self._next_dt:
                pyglet.clock.schedule_once(self._animate, self._next_dt)
            self._create_vertex_list()


### might also come in handy: pause_animation, resume_animation
