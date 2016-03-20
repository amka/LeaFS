# coding: utf-8

__author__ = 'Andrey Maksimov <meamka@ya.ru>'
__date__ = '20.03.16'


class DuplicatedFileError(Exception):
    """File name duplicated error
    """

    def __init__(self, *args, **kwargs):
        super(DuplicatedFileError, self).__init__(*args, **kwargs)


class NotFoundError(Exception):
    """File not found error
    """

    def __init__(self, *args, **kwargs):
        super(NotFoundError, self).__init__(*args, **kwargs)