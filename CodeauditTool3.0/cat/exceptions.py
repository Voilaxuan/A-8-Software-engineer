# -*- coding: utf-8 -*-

class CobraException(Exception):
    """Base class for all Cobra exceptions."""


class PickupException(CobraException):
    """Base class for all Pickup exceptions."""


class PickupGitException(PickupException):
    """Base class for all Git exceptions"""


class NotExistException(PickupGitException):
    """Base class for Pickup exceptions"""


class AuthFailedException(PickupGitException):
    """Base class for Auth Failed exceptions"""
