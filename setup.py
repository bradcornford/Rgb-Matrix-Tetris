from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rgb-matrix-tetris',

    version='1.0.0',

    description='Raspberry Pi Python rgb matrix tetris',
    long_description=long_description,

    url='https://github.com/bradcornford/Rgb-Matrix-Tetris',

    author='Bradley Cornford',
    author_email='me@bradleycornford.co.uk',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='rgb matrix tetris raspberry pi',

    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    install_requires=['pygame', 'RPi.GPIO', 'rgbmatrix', 'tinydb', 'mock'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={},

    data_files=[],

    entry_points={
        'console_scripts': []
    },
)
