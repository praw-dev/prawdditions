"""prawdditions setup.py."""

import re
from codecs import open
from os import path
from setuptools import find_packages, setup


PACKAGE_NAME = "prawdditions"
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.rst"), encoding="utf-8") as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, "const.py"), encoding="utf-8") as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)

extras = {
    "ci": ["coveralls"],
    "dev": ["pre-commit"],
    "lint": ["black", "flake8", "pydocstyle", "sphinx", "sphinx_rtd_theme"],
    "test": [
        "betamax >=0.8, <0.9",
        "betamax-matchers >=0.3.0, <0.5",
        "betamax-serializers >=0.2, <0.3",
        "mock >=0.8",
        "pytest >=2.7.3",
    ],
}

extras["dev"] += extras["lint"] + extras["test"]

setup(
    name=PACKAGE_NAME,
    author="PokestarFan",
    author_email="sarkaraoyan@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    description="High-level utilities for PRAW.",
    extras_require=extras,
    install_requires=["praw < 7.0"],
    keywords="praw additions",
    license="Simplified BSD License",
    long_description=README,
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"": ["LICENSE.txt"]},
    test_suite="tests",
    url="https://github.com/praw-dev/prawdditions",
    version=VERSION,
)
