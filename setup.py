from setuptools import setup, find_packages

setup(
    name='Blackjack',
    version='0.1.0',
    description='Bot Discord',
    author='Thibaut Piquerez et Nicolas Kaser',
    author_email='thibaut.piquerez@he-arc.ch',
    url='https://github.com/Thibaut95/ProjetPython.git',
    packages=find_packages(exclude=('tests', 'docs'))
)