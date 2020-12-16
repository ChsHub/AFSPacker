import setuptools
from distutils.core import setup
from afs_extractor.__main__ import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='afs_extractor',
    version=__version__,
    description=long_description.split('\n')[1],  # First line of description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ChsHub/AFSPacker',
    author='ChsHub',
    packages=['afs_extractor'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3'],
)
