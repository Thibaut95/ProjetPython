from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Blackjack',
    python_requires='>=3.6',
    author='Thibaut Piquerez et Nicolas Kaser',
    author_email='thibaut.piquerez@he-arc.ch',
    url='https://github.com/Thibaut95/ProjetPython.git',
    license='https://opensource.org/licenses/BSD-3-Clause',
    packages=find_packages(exclude=('contrib', 'docs', 'tests')),
    classifiers=(
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: entertainment'
    ),
    install_requires=(
        'aiohttp>=2.1.0',
    )
)
