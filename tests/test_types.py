# coding: utf-8
import unittest

from leafs.types import File, Folder

__author__ = 'Andrey Maksimov <meamka@ya.ru>'
__date__ = '20.03.16'


class TestFile(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_init(self):
        new_file = File(name='New File', path='/', meta={'mime_type': 'text/plain'})

        self.assertEqual(new_file.name, 'New File')
        self.assertEqual(new_file.path, '/')
        self.assertEqual(new_file.mime_type, 'text/plain')


class TestFolder(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_init(self):
        new_folder = Folder(name='New Folder', path='/')

        self.assertEqual(new_folder.name, 'New Folder')
        self.assertEqual(new_folder.path, '/')


if __name__ == '__main__':
    unittest.main()
