.. _tests:

Tests
=====


Types:
------

..  testsetup:: *

    from leafs.types import File, Folder

..  doctest::

    >>> file = File(name='New File', path='/', meta={'mime_type': 'text/plain'})
    >>> file
    File('/New File')


FileSystem:
-----------

..  testsetup:: *

    from leafs.fs import FileSytem

..  doctest::

    >>> CONFIG = {
    ...     'mongo': {
    ...         'host': 'localhost',
    ...         'port': 27017,
    ...         'name': 'leafs',
    ...         'collection': 'files',
    ...     }
    ... }
    >>> fs = FileSystem(CONFIG)
    >>> fs.listdir()
    []
