"""prawdditions setup.py."""

import re
from codecs import open
from os import path
from setuptools import setup


PACKAGE_NAME = 'prawdditions'
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, 'const.py'),
          encoding='utf-8') as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)


setup(name=PACKAGE_NAME,
      author='Randall Goodman',
      author_email='randy@kindofabigdeal.org',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython'],
      description='DESCRIPTION.',
      install_requires=['requests >=4.0.0, <5.0'],['praw >=4.0.0']
      keywords='praw additions',
      license='Simplified BSD License',
      long_description=README,
      packages=[PACKAGE_NAME],
      url='https://github.com/praw-dev/prawdditions',
      version=VERSION)
