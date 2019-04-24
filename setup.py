from pathlib import Path
from setuptools import setup, find_packages

VERSION = (0, 1, 0)

setup(
    name='progressist',
    version=".".join(map(str, VERSION)),
    description='Minimalist and pythonic progress bar',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    url="https://github.com/pyrates/progressist",
    author='Yohan Boniface',
    author_email="hi@yohanboniface.me",
    license='WTFPL',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='progress bar',
    packages=find_packages(exclude=['tests']),
    py_modules=['progressist'],
    extras_require={
        'test': ['pytest'],
    },
)
