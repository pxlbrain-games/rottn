# -*- coding: utf-8 -*-
'''
Provides mixins for cocos layers that grant access to player controls
'''

class Avatar:
    '''
    Mixin that makes a CocosNode a controllable character.
    '''
    pass

class Clickable:
    '''
    Mixin that makes a CocosNode clickable and clicking on it
    will call it's *on_click()* function.
    '''
    pass

class Dragable:
    '''
    Mixin that makes a CocosNode dragable by mouse and calls
    it's *on_drag()* and *on_drop()* function.
    '''
    pass
