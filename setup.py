import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

requests = 'requests >= 0.8.8'
if sys.version_info < (2, 6):
    requests += ', < 0.10.1'
install_requires = [requests]

if sys.version_info < (2, 6):
    install_requires.append('ssl')

install_requires.append('simplejson')


# Don't import eagleeyenetworks module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'eagleeyenetworks'))
from version import VERSION

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')

setup(
    name='eagleeyenetworks',
    cmdclass={'build_py': build_py},
    version=VERSION,
    description='Eagleeyenetworks python bindings',
    author='Eagleeyenetworks',
    author_email='support@eagleeyenetworks.com',
    url='https://eagleeyenetworks.com/',
    packages=['eagleeyenetworks', 'eagleeyenetworks.test'],
    package_data={'eagleeyenetworks': ['data/ca-certificates.crt', '../VERSION']},
    install_requires=install_requires,
    test_suite='eagleeyenetworks.test.all',
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])