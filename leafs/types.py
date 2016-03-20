# coding: utf-8
import collections
import datetime
import os

__author__ = 'Andrey Maksimov <meamka@ya.ru>'
__date__ = '16.03.16'

Filetype = collections.namedtuple('FileType', ['FILE', 'FOLDER'])
FILETYPE = Filetype(FILE=0, FOLDER=1)


class File(object):
    """Base file type for LeaFS file system.

    """

    # Meta fields available to update
    METAKEYS = ['size', 'mime_type', 'md5', 'custom_properties', 'created', 'modified']

    def __init__(self, name, path=None, meta=None):
        """Intialize new file with named *name* in given folder `path`.
        Additional data can be passed through `meta` dict.
        Available `meta`-fields:

            * **created** — file creation date
            * **custom_properties** — dictionary with custom meta data
            * **md5** — md5 hash of file
            * **mime_type** — mime type
            * **modified** — file modification date
            * **size** — file size


            >>> file = File(name='New File', path='/', meta={'mime_type': 'text/plain'})
            >>> file
            File('/New File')

        :param name: filename
        :type name: str
        :param path: path to parent folder for file
        :type path: str or None
        :param meta: additional data can be passed through `meta` dict.
        :type meta: dict or None
        :return: :class:`leafs.types.File` object
        :rtype: `leafs.types.File`
        :raises: `leafs.errors.DuplicatedFileError`
        """
        self.name = name
        self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        self.path = path
        self.type = FILETYPE.FILE
        self.md5 = ''
        self.size = 0
        self.mime_type = ''
        self.public_url = None

        if isinstance(meta, dict):
            [setattr(self, key, value) for key, value in meta.items() if key in File.METAKEYS]

    def __repr__(self):
        return '%s(\'%s\')' % (self.__class__.__name__, os.path.join(self.path, self.name))

    def to_save(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}


class Folder(File):
    def __init__(self, name, path=None, meta=None):
        super(Folder, self).__init__(name=name, path=path, meta=meta)
        self.type = FILETYPE.FOLDER
