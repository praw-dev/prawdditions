"""Patch functions are stored in this submodule."""

from praw import Reddit
from praw.models.reddit.wikipage import WikiPage

from .message import message
from .update import update


def patch():
    """Apply new methods to classes."""
    Reddit.message = message
    WikiPage.update = update


def unpatch():
    """Remove added methods."""
    del Reddit.message
    del WikiPage.update
