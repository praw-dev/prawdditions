prawdditions
============

.. image:: https://img.shields.io/pypi/v/prawdditions.svg
           :alt: Latest prawdditions Version
           :target: https://pypi.python.org/pypi/prawdditions


Prawdditions is an auxiliary package for the PRAW project, designed to supplement its existing functionality. Prawdditions aims to add more abstract functionality to the praw libraries that would otherwise clash with the clean design that praw 4.0.0 exhibits. An example of this is an abstracted `message` function that does not extend from a redditor or subreddit class. Prawdditions adds this functionality in a manner that doesn't explicitly require the instantiation of such objects, and will aim to build out similar such functionality in the future.


Installation
------------

Install prawdditions using ``pip`` via:

.. code-block:: console

    pip install prawdditions


Usage
-----

The following example demonstrates how to use prawdditions...

.. code-block:: python

   import praw
   import prawdditions
   
   #Instantiate Reddit Client
   reddit = praw.Reddit(...)
   
   #Abstract message function now available.
   reddit.message('user_or_subreddit','subject','body')

Contact
-------

Author: Randy Goodman

Email: randy@kindofabigdeal.org
