prawdditions.filters
====================

The prawdditions.filters contains one class, :class:`.Filterable`, and many
other helper classes & functions, that can be used with :class:`.Filterable`.

.. codeauthor:: PokestarFan <@PythonCoderAS>

The Filterable Class
--------------------

.. autoclass:: prawdditions.filters.filter.Filterable
   :members:

Filter Callbacks
----------------

:class:`.Filterable` takes callback functions as filterable items, similar
to :func:`filter`. Custom functions can be provided, although there are a
lot of built-in functions that return callbacks.

.. toctree::
   :maxdepth: 2
   :caption: Filter Callbacks:

   filters/base

Filter Capsules
---------------

.. autoclass:: prawdditions.filters.capsule.FilterCapsule
   :members: