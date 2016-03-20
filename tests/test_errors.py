# coding: utf-8
import unittest

from leafs import FileSystem
from leafs.errors import DuplicatedFileError, NotFoundError

__author__ = 'Andrey Maksimov <meamka@ya.ru>'
__date__ = '20.03.16'


class Test(unittest.TestCase):
    def setUp(self):
        config = {

        }
        fs = FileSystem(config=config)

    def test_duplication_error(self):
        File(name='New File', path='/', meta={'mime_type': 'text/plain'})

        self.assertRaises(File(name='New File', path='/'), DuplicatedFileError)


class TestFolder(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_init(self):
        new_folder = Folder(name='New Folder', path='/')

        self.assertEqual(new_folder.name, 'New Folder')
        self.assertEqual(new_folder.path, '/')


if __name__ == '__main__':
    unittest.main()
