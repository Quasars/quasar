#!/usr/bin/env python3

from os import path

from setuptools import setup, find_packages, Command

NAME = "Quasar"

VERSION = "1.11.0"

DESCRIPTION = "Quasar is a collection of data analysis toolboxes extending the Orange suite."
LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.pypi')).read()
AUTHOR = 'Canadian Light Source, Biolab UL, Soleil, Elettra'
AUTHOR_EMAIL = 'marko@toplak.io'
URL = "https://quasar.codes"

KEYWORDS = [
    'orange3',
    'spectroscopy',
    'infrared'
]
PACKAGES = find_packages()

PACKAGE_DATA = {
    'quasar.tutorials': ['*.ows', '*.tab'],
    'quasar.tests': ['*'],
    'quasar.launcher': ['icons/*.ows', 'icons/*.png', 'icons/*.svg'],
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]

INSTALL_REQUIRES =  \
    [line.strip()
     for line in open(path.join(path.dirname(__file__), 'requirements.txt'))
     if line.strip() and not line.strip().startswith("#")]

ENTRY_POINTS = {
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        'quasartutorials = quasar.tutorials',
    ),
    "gui_scripts": (
        "quasar = quasar.__main__:main",
    ),
}

TEST_SUITE = "quasar.tests.suite"

if __name__ == '__main__':

    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        keywords=KEYWORDS,
        test_suite=TEST_SUITE,
        include_package_data=True,
        zip_safe=False,
        license='GPLv3+',
    )
