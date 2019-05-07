# -*- coding: utf-8 -*-
"""
This module introduces bases classes for characters that client and server
can subclass in order to create their respective versions of enemies, players
and other NPCs.
"""

class Character:
    """
    Base class for any kind of character in the game.
    """

    def __init__(self, name_or_state):
        super().__init__()  # for cooperative multiple inheritance
        if isinstance(name_or_state, str):
            self.name = name_or_state
            self.position = (0, 0)
            self.velocity = (0, 0)
            self.direction = (0, 1)
            self.health = 100
        else:
            self.set_state(name_or_state)

    def get_state(self):
        return {
            "name": self.name,
            "position": self.position,
            "velocity": self.velocity,
            "direction": self.direction,
            "health": self.health,
        }

    def set_state(self, state: dict):
        self.name = state["name"]
        self.position = state["position"]
        self.velocity = state["velocity"]
        self.direction = state["direction"]
        self.health = state["health"]


class PlayerCharacter(Character):
    """
    A type that describes a player character in the game world
    """

    def __init__(self, name_or_state):
        super().__init__(name_or_state)

    def get_move_event_data(self, player_id):
        return {
            "player_id": player_id,
            "position": self.position,
            "velocity": self.velocity,
            "direction": self.direction
        }

    def on_move(self, move_event_data):
        self.position = move_event_data["position"]
        self.velocity = move_event_data["velocity"]
        self.direction = move_event_data["direction"]
        return {
            "players": {
                move_event_data["player_id"]: {
                    "position": self.position,
                    "velocity": self.velocity,
                    "direction": self.direction,
                }
            }
        }


class NonPlayerCharacter(Character):
    """
    A type that describes an enemy in the game world
    """

    def __init__(self, name_or_state):
        super().__init__(name_or_state)
        self.attack_counter = 0.0

    def get_state(self):
        state = super().get_state()
        state["attack_counter"] = self.attack_counter
        return state

    def set_state(self, state: dict):
        super().set_state(state)
        self.attack_counter = state["attack_counter"]

    def is_attacking(self):
        return self.attack_counter > 0.0
