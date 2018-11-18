# -*- coding: utf-8 -*-
"""
Defines CocosNodes for UI elements and provides useful mixins for user interaction.
"""


class Clickable:
    """
    Mixin that makes a CocosNode clickable and clicking on it
    will call it's *on_click()* function.
    """

    pass


class Dragable:
    """
    Mixin that makes a CocosNode dragable by mouse and calls
    it's *on_drag()* and *on_drop()* function.
    """

    pass
