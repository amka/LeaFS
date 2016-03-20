# coding: utf-8
import datetime
import hashlib
import logging
import mimetypes
import os
import re

from pymongo import MongoClient, ASCENDING, DESCENDING, ReturnDocument
from pymongo.errors import DuplicateKeyError

from leafs.errors import DuplicatedFileError
from leafs.types import File, Folder

__author__ = 'Andrey Maksimov <meamka@ya.ru>'
__date__ = '16.03.16'

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)


class FileSystem(object):
    """Leafs file system class. Represents virtual file system with root **/**.

    :ivar cwd: current working directory
    """

    SORTFIELDS = ['type', 'created', 'modified', 'name']

    def __init__(self, config):
        """Initialize :class:`leafs.fs.FileSystem` object.
         `config` — dictionary with mongodb settings, i.e.:

         .. code-block:

            {
                'mongo': {
                    'host': 'localhost',
                    'port': 27017,
                    'name': 'leafs',
                    'collection': 'files',
                }
            }

        :param config: dict with mongo settings
        :type config: dict
        :return: None
        """
        self.client = MongoClient(host=config['mongo']['host'], port=config['mongo']['port'])
        self.db = self.client.get_database(config['mongo']['name'])
        self.storage = self.db.get_collection(name=config['mongo']['collection'])
        logger.debug('LeaFS initialized.')

        self.cwd = '/'

    def mkdir(self, name, path=None, meta=None):
        """Create a directory named `name` in given folder `path`.
        Additional data can be passed through `meta` dict.
        Available `meta`-fields:

            * **created** — file creation date
            * **custom_properties** — dictionary with custom meta data
            * **md5** — md5 hash of file
            * **mime_type** — mime type
            * **modified** — file modification date
            * **size** — file size

        :param name: name of new directory
        :type name: str
        :param path: path to directory
        :type path: str
        :param meta: additional metadata for directory
        :type meta: dict
        :return: `leafs.types.Folder` object
        :rtype: `leafs.types.Folder`
        """
        logger.debug('Directory created in path: %s', path)
        if not path or not re.match('[A-z0-9\s\-/_.]+', path):
            path = self.cwd

        new_folder = Folder(name=name, path=path, meta=meta)

        logger.debug('Try to create folder %s in folder %s', new_folder.to_save(), path or self.cwd)
        try:
            self.storage.save(new_folder.to_save())
        except DuplicateKeyError as e:
            logger.debug(e)
            raise DuplicatedFileError(e.message)

        self.touch(path=path)
        return new_folder

    def mkfile(self, name, path=None, meta=None):
        """Create a file named `name` in given folder `path`.
        Additional data can be passed through `meta` dict.
        Available `meta`-fields:

            * **created** — file creation date
            * **custom_properties** — dictionary with custom meta data
            * **md5** — md5 hash of file
            * **mime_type** — mime type
            * **modified** — file modification date
            * **size** — file size

        By default it creates text file with mime-type: *text/plain*

        :param name: name of new directory
        :type name: str
        :param path: path to directory
        :type path: str
        :param meta: additional metadata for directory
        :type meta: dict
        :return: boolean result of file creation
        :rtype: `leafs.types.File`
        """
        logger.debug('File created in path: %s', path)
        if not path or not re.match('[A-z0-9\s\-/_.]+', path):
            path = self.cwd

        new_file = File(name=name, path=path, meta={'mime_type': 'text/plain'})

        logger.debug('Try to create file %s in folder %s', new_file.to_save(), path or self.cwd)
        try:
            self.storage.save(new_file.to_save())
        except DuplicateKeyError as e:
            logger.debug(e)
            raise DuplicatedFileError(e.message)

        self.touch(path=path)
        return new_file

    def _get_md5(self, filename):
        """Calculate md5 hash from file

        :param filename: path to file
        :type filename: str
        :return: md5 hash
        :rtype: str
        """
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def add_file(self, filename):
        """Create a :class:`leafs.types.File` object for given filename.

        :param filename: path to file to add
        :type filename: str
        :return: boolean result of file creation
        :rtype: `leafs.types.File`
        """
        if not os.path.exists(filename):
            return None

        name = os.path.basename(filename)
        path = os.path.dirname(filename)
        atime = os.path.getatime(filename)
        mtime = os.path.getmtime(filename)

        new_file = File(name=name, path=path, meta={
            'mime_type': mimetypes.guess_type(filename)[0],
            'created': datetime.datetime.utcfromtimestamp(atime),
            'modified': datetime.datetime.utcfromtimestamp(mtime),
            'size': os.path.getsize(filename),
            'md5': self._get_md5(filename),
        })

        logger.debug('Try to create file %s in folder %s', new_file.to_save(), path or self.cwd)
        try:
            self.storage.save(new_file.to_save())
        except DuplicateKeyError as e:
            logger.debug(e)
            raise DuplicatedFileError(e.message)

        self.touch(path=path)
        return new_file

    def listdir(self, path, sort=None, folder_first=True):
        """Return list of files inside given path

        :param path: path to directory
        :type path: str
        :param sort: field name to sort
        :type sort: str
        :param folder_first: folders first. default is `True`
        :type folder_first: bool
        :return: list of files inside given directory
        :rtype: list
        """
        logger.debug('Directory %s listing', path)
        if not sort or sort[1:] not in self.SORTFIELDS:
            sort = 'name'
        sort_direction = ASCENDING if not sort or sort[1] != '+' else DESCENDING

        sort_list = [(sort, sort_direction)]
        if folder_first:
            sort_list.insert(0, ('type', DESCENDING))

        logger.debug('Path %s, Sort %s', path, sort_list)

        res = self.storage.find({'path': path or self.cwd}).sort(sort_list)
        docs = [doc for doc in res]

        return docs

    def info(self, path):
        """Return file info for given path.

        :param path: file path
        :type path: str
        :return: Return dict with metadata for given path
        :rtype: dict or None
        """
        logger.debug('File %s metadata', path)
        _filter = {
            'path': path[:path.rindex('/')] or '/',
            'name': path[path.rindex('/') + 1:]
        }
        metadata = self.storage.find_one(filter=_filter)
        return metadata

    def touch(self, path):
        """Update modified time for given file `path`

        :param path: file path. Could point both on file or folder
        :return: updated object's as dict
        :rtype: dict
        """
        _filter = {
            'path': path[:path.rindex('/')] or '/',
            'name': path[path.rindex('/') + 1:]
        }
        logger.debug('Touch %s', _filter)

        return self.storage.find_one_and_update(
            filter=_filter,
            update={'$set': {'modified': datetime.datetime.utcnow()}},
            return_document=ReturnDocument.AFTER
        )
