leafs package
=============

Submodules
----------

leafs.fs module
---------------

File system class represents virtual filesystem in LeaFS that
able to create file or folder, list folders, get files info
Object have to be initialize with configuration dictionary: i. e.::

    CONFIG = {
        'mongo': {
            'host': 'localhost',
            'port': 27017,
            'name': 'leafs',
            'collection': 'files',
        }
    }


..  automodule:: leafs.fs
    :members:
    :show-inheritance:

leafs.types module
------------------

..  automodule:: leafs.types
    :members:
    :show-inheritance:

..  testsetup:: *

    from leafs.types import File, Folder

File creation example:

..  doctest::

    >>> file = File(name='New File', path='/', meta={'mime_type': 'text/plain'})
    >>> file
    File('/New File')


Folder creation same as File:

..  doctest::

    >>> folder = Folder(name='New Folder', path='/home')
    >>> folder
    Folder('/home/New Folder')


leafs.errors module
-------------------

..  automodule:: leafs.errors
    :members:
    :show-inheritance:
