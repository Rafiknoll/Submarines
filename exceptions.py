"""
Name:       exceptions.py

Purpose:    Provides dedicated exceptions for the submarine game

Usage:      from exceptions import *

Author:     Rafael Knoll
"""


class LocationOccupiedException(Exception):
    """
    Occurs when attempting to place a submarine in an occupied location
    """
    pass


class ConnectionNotMadeYetException(Exception):
    """
    Occurs when an attempt to use a connection is made before the connection itself was made
    """
    pass


class EnemySurrenderedException(Exception):
    """
    Occurs when the enemy surrenders in the middle of the game
    """
    pass


class SelfSurrenderException(Exception):
    """
    Occurs when the player surrenders in the middle of the game
    """
    pass
