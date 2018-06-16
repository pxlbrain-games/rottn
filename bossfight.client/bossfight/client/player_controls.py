# -*- coding: utf-8 -*-
'''
Defines the controls for the player character.
'''

import math
import pyglet
import cocos
from cocos.director import director
from pyglet.window import key

BASE_SPEED = 300

RAD_TO_DEG = 180/cocos.euclid.math.pi

class ControllableNode(cocos.cocosnode.CocosNode):
    '''
    A *CocosNode* that can be controlled by the player.
    Controllable Nodes automatically react to Controller or Mouse & Keyboard input.
    If you use multiple inheritance, inherit from *ControllableNode* before any third party
    (and thus possibly non-cooperative) base classes. (This class **is** cooperative btw.)
    '''

    def __init__(self, position=(0, 0), direction=(0, 1), joystick=None, mouse_and_keyboard=True, speed=BASE_SPEED):
        super().__init__()
        self.position = position
        self.direction = cocos.euclid.Vector2(0, 0) + direction
        self.direction.normalize()
        image = pyglet.resource.image('arrow_icon.png')
        self.line = cocos.sprite.Sprite(image, scale=0.08, opacity=100)
        self.add(self.line)
        self.joystick = joystick
        if joystick is None:
            try:
                self.joystick = pyglet.input.get_joysticks()[0]
            except IndexError:
                print('Controller not found.')
        if self.joystick is not None:
            self.joystick.push_handlers(self)
            try:
                self.joystick.open(window=director.window)
            except OSError:
                pass # Controller was already openend
        if mouse_and_keyboard:
            self.keyboard = key.KeyStateHandler()
            director.window.push_handlers(self.keyboard)
            director.window.push_handlers(self)
        else:
            self.keyboard = None
        self.speed = speed
        self.velocity = (0, 0)
        self.do(cocos.actions.Move())
        self.schedule(self._update_movement)

    def on_mouse_motion(self, x, y, dx, dy):
        turn = cocos.euclid.Matrix3.new_rotate(-0.01*dx)
        self.direction = turn*self.direction
        self.line.rotation += 0.01*dx*RAD_TO_DEG

    def _update_movement(self, dt):
        new_joy_direction = cocos.euclid.Vector2(self.joystick.rx, -self.joystick.ry)
        if self.joystick is not None and new_joy_direction.magnitude_squared() > 0.1:
            new_joy_direction.normalize()
            angle = math.acos(min(self.direction.dot(new_joy_direction), 1.0))*RAD_TO_DEG
            # THE SIGN NEEDS SOME THINKING ...
            sign = 1 if self.direction.x < new_joy_direction.x and self.direction.y > new_joy_direction.y \
                or self.direction.x > new_joy_direction.x and self.direction.y < new_joy_direction.y else -1
            self.line.rotation += sign*angle
            self.direction = new_joy_direction
        velocity = cocos.euclid.Vector2(0, 0)
        if self.joystick is None or \
          self.joystick.x*self.joystick.x + self.joystick.y*self.joystick.y < 0.05 and \
          self.keyboard is not None:
            if self.keyboard[key.W]:
                velocity += self.direction
            if self.keyboard[key.S]:
                velocity -= self.direction
            if self.keyboard[key.D]:
                velocity += self.direction.cross()
            if self.keyboard[key.A]:
                velocity -= self.direction.cross()
            velocity.normalize()
        else:
            velocity += (self.joystick.x, -self.joystick.y)
            velocity *= velocity.magnitude_squared()
            if velocity.magnitude_squared() > 1.0:
                # This can never be True on physical analog sticks,
                # but should still be checked, as the driver theoretically allows this.
                velocity.normalize()
        velocity *= self.speed
        self.velocity = velocity.xy
