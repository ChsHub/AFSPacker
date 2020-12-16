import setuptools
from distutils.core import setup
from afs_packer.__main__ import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='afs_packer',
    version=__version__,
    description=long_description.split('\n')[1],  # First line of description
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ChsHub',
    packages=['afs_packer'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3'],
)
