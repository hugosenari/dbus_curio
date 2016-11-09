#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "curio>=0.4"
]

test_requirements = [
    "pytest_curio>=0.1.0"
]

setup(
    name='dbus_curio',
    version='0.1.0',
    description="Python dbus lib using Curio (IO lib)",
    long_description=readme + '\n\n' + history,
    author="Hugo Sena Ribeiro",
    author_email='hugosenari@gmail.com',
    url='https://github.com/hugosenari/dbus_curio',
    packages=[
        'dbus_curio',
    ],
    package_dir={'dbus_curio':
                 'dbus_curio'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='dbus_curio',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
