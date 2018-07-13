#!/usr/bin/env python


from setuptools import setup, Extension
import os

with open('xxhash_cffi/__init__.py') as f:
    for line in f:
        if line.startswith('VERSION = '):
            VERSION = eval(line.rsplit(None, 1)[-1])
            break

setup_kwargs = {}

if os.name == 'posix':
    extra_compile_args = [
        "-std=c99",
        "-O3",
        "-Wall",
        "-W",
        "-Wundef",
        # ref: http://bugs.python.org/issue21121
        "-Wno-error=declaration-after-statement",
    ]
else:
    extra_compile_args = None

setup_kwargs['install_requires'] = ['cffi']
setup_kwargs['setup_requires'] = ['cffi']
setup_kwargs['cffi_modules'] = ['ffibuild.py:ffi']

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
    packages=['xxhash_cffi'],
    ext_package='xxhash_cffi',
    test_suite='nose.collector',
    tests_require=['nose>1.3.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    **setup_kwargs
)
