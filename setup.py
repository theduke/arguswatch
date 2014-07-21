# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION'), 'r') as f:
    version = f.read().strip()

setup(
    name='arguswatch',

    version=version,

    description='Scalable and easy to use service monitoring system',
    long_description=long_description,

    url='https://github.com/theduke/arguswatch',

    author='Christoph Herzog',
    author_email='chris@theduke.at',

    license='GPLv2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

	'Intended Audience :: System Administrators',
	'Topic :: System :: Monitoring',

	'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='monitoring',

    packages=find_packages(exclude=[]),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=[
	# Django + django contrib apps.
	'Django>=1.6,<1.7',
	'South>=1',
	'django-baseline>=0.2.2',
	'django-crispy-forms>=1.4',
	'django-filter>=0.7',
	'django-mptt>=0.6',
	'django-polymorphic>=0.5.5',
	'django-sekizai>=0.7',
	'django-taggit>=0.12',
	'djangorestframework>=2.3',
	'pytz>=2014.4',

	# Celery task queye.
	'celery>=3.1',
	
	# Native python mysql.
	# Needed by sqlquery servyice plugin.
	'PyMySQL>=0.6',
	
	# SSH library for natvie python ssh.
	# Needed by ssh service plugin.
	'paramiko>=1.14',
    ],

    include_package_data=True,

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
        #'sample': ['package_data.dat'],
	#'': ['*.html', '*.js', '*.css'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            #'sample=sample:main',
        ],
    },
)

