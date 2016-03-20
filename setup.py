from setuptools import setup

setup(
    name='LeaFS',
    version='0.1',
    packages=['leafs'],
    url='https://github.com/amka/leafs/',
    license='BSD',
    author='Andrey Maksimov',
    author_email='meamka@ya.ru',
    description='Python virtual file system',
    long_description=__doc__,
    install_requires=[
        'pymongo==3.2.2',
    ],
)
