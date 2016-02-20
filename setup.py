from setuptools import setup, find_packages
from codecs import open
from os import path

import progresso

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='progresso',
    version=progresso.__version__,
    description='Minimalist and pythonic progress bar',
    long_description=long_description,
    url=progresso.__homepage__,
    author=progresso.__author__,
    author_email=progresso.__contact__,
    license='WTFPL',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='progress bar',
    packages=find_packages(exclude=['tests']),
    py_modules=['progresso'],
    extras_require={
        'test': ['pytest'],
    },
)
