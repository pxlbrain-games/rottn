# -*- coding: utf-8 -*-
'''
Defines the controls for the player character.
'''

import pyglet
import cocos
from cocos.director import director

class Avatar(cocos.cocosnode.CocosNode):
    '''
    Mixin that makes a CocosNode responsive to player controls.
    You should call *init_avatar()* to initialize player controls.
    '''

    def init_avatar(self, joystick=None, mouse_and_keyboard=True):
        self.joystick = joystick
        if joystick is None:
            try:
                self.joystick = pyglet.input.get_joysticks()[0]
            except IndexError:
                print('Controller not found.')
        if joystick is not None:
            self.joystick.push_handlers(self)            
            try:
                self.joystick.open()
            except OSError:
                pass # Controller was already openend
        if mouse_and_keyboard:
            director.window.push_handlers(self)
        self._keys_pressed = []
        self.velocity = (0, 0)
        self.do(cocos.actions.Move())
        self.schedule(self._update_movement)

    def _update_movement(self, dt):
        velocity = cocos.euclid.Vector2(0, 0)
        if self.joystick is None or \
          self.joystick.x*self.joystick.x + self.joystick.y*self.joystick.y < 0.1:
            if 'UP' in self._keys_pressed and 'DOWN' not in self._keys_pressed:
                velocity += (0, 1)
            if 'DOWN' in self._keys_pressed and 'UP' not in self._keys_pressed:
                velocity -= (0, 1)
            if 'RIGHT' in self._keys_pressed and 'LEFT' not in self._keys_pressed:
                velocity += (1, 0)
            if 'LEFT' in self._keys_pressed and 'RIGHT' not in self._keys_pressed:
                velocity -= (1, 0)
            velocity.normalize()
            velocity *= 300
        else:
            velocity += 300*(self.joystick.x, self.joystick.y)
        self.velocity = velocity.xy

    def on_key_press(self, key, modifier):
        if key == pyglet.window.key.UP:
            self._keys_pressed.append('UP')
        if key == pyglet.window.key.DOWN:
            self._keys_pressed.append('DOWN')
        if key == pyglet.window.key.LEFT:
            self._keys_pressed.append('LEFT')
        if key == pyglet.window.key.RIGHT:
            self._keys_pressed.append('RIGHT')

    def on_key_release(self, key, modifier):
        if key == pyglet.window.key.UP:
            self._keys_pressed.remove('UP')
        if key == pyglet.window.key.DOWN:
            self._keys_pressed.remove('DOWN')
        if key == pyglet.window.key.LEFT:
            self._keys_pressed.remove('LEFT')
        if key == pyglet.window.key.RIGHT:
            self._keys_pressed.remove('RIGHT')
