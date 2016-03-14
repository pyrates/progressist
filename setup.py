from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = (0, 0, 4)

setup(
    name='progressist',
    version=".".join(map(str, VERSION)),
    description='Minimalist and pythonic progress bar',
    long_description=long_description,
    url="https://github.com/yohanboniface/progressist",
    author='Yohan Boniface',
    author_email="hi@yohanboniface.me",
    license='WTFPL',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='progress bar',
    packages=find_packages(exclude=['tests']),
    py_modules=['progressist'],
    extras_require={
        'test': ['pytest'],
    },
)
