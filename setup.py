#!/usr/bin/env python


from setuptools import setup, Extension
import os

with open('xxhash_cffi/__init__.py') as f:
    for line in f:
        if line.startswith('VERSION = '):
            VERSION = eval(line.rsplit(None, 1)[-1])
            break

setup(
    name='xxhash-cffi',
    version=VERSION,
    description="Python binding for xxHash",
    long_description=open('README.rst', 'r').read(),
    long_description_content_type="text/x-rst",
    author='Yue Du',
    author_email='ifduyue@gmail.com',
    url='https://github.com/ifduyue/python-xxhash-cffi',
    license='BSD',
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    packages=['xxhash_cffi'],
    ext_package='xxhash_cffi',
    install_requires = ['cffi'],
    setup_requires = ['cffi'],
    cffi_modules = ['ffibuild.py:ffi'],
    test_suite='nose.collector',
    tests_require=['nose>1.3.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
