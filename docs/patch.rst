prawdditions.patch
------------------

This submodule contains functions that directly add attributes to PRAW
models. To prevent conflicts with future PRAW additions, the models will not
be modified without a call to :func:`.patch`. Furthermore, the additions can
be removed with a call to :func:`.unpatch`.

prawdditions.patch.patch
++++++++++++++++++++++++

.. autofunction:: prawdditions.patch.patch

prawdditions.patch.unpatch
++++++++++++++++++++++++++

.. autofunction:: prawdditions.patch.unpatch

Patched Functions
+++++++++++++++++

prawdditions.patch.message.message
**********************************

.. autofunction:: prawdditions.patch.message.message

prawdditions.patch.update.update
********************************

.. autofunction:: prawdditions.patch.update.update