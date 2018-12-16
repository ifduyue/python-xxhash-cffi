python-xxhash-cffi
==================

.. image:: https://travis-ci.org/ifduyue/python-xxhash-cffi.svg?branch=master
    :target: https://travis-ci.org/ifduyue/python-xxhash-cffi
    :alt: Travis CI Build Status

.. image:: https://ci.appveyor.com/api/projects/status/si9lt6bteol5op7q/branch/master?svg=true
    :target: https://ci.appveyor.com/project/duyue/python-xxhash-cffi
    :alt: Appveyor Build Status

.. image:: https://img.shields.io/pypi/v/xxhash-cffi.svg
    :target: https://pypi.org/project/xxhash-cffi/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/xxhash-cffi.svg
    :target: https://pypi.org/project/xxhash-cffi/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/xxhash-cffi.svg
    :target: https://pypi.org/project/xxhash-cffi/
    :alt: License


.. _HMAC: http://en.wikipedia.org/wiki/Hash-based_message_authentication_code
.. _xxHash: https://github.com/Cyan4973/xxHash
.. _Cyan4973: https://github.com/Cyan4973


xxhash-cffi is a Python binding for the xxHash_ library by `Yann Collet`__.

__ Cyan4973_

Installation
------------

.. code-block:: bash

   $ pip install xxhash-cffi

Installation Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're installing xxhash-cffi from source, you probably want to install the following packages.

On Debian/Ubuntu:

.. code-block:: bash

   $ apt-get install libcffi-dev python-dev gcc

On CentOS/Fedora:

.. code-block:: bash

   $ yum install libcffi-devel python-devel gcc redhat-rpm-config


Usage
--------

Module version and its backend xxHash library version can be retrieved using
the module properties ``VERSION`` AND ``XXHASH_VERSION`` respectively.

.. code-block:: python

    >>> import xxhash_cffi as xxhash
    >>> xxhash.VERSION
    '1.0.1'
    >>> xxhash.XXHASH_VERSION
    '0.6.2'

This module is hashlib-compliant, which means you can use it in the same way as ``hashlib.md5``.

    | update() -- update the current digest with an additional string
    | digest() -- return the current digest value
    | hexdigest() -- return the current digest as a string of hexadecimal digits
    | intdigest() -- return the current digest as an integer
    | copy() -- return a copy of the current xxhash object
    | reset() -- reset state

md5 digest returns bytes, but the original xxh32 and xxh64 C APIs return integers.
While this module is made hashlib-compliant, ``intdigest()`` is also provided to
get the integer digest.

Constructors for hash algorithms provided by this module are ``xxh32()`` and ``xxh64()``.

For example, to obtain the digest of the byte string ``b'Nobody inspects the spammish repetition'``:

.. code-block:: python

    >>> import xxhash_cffi as xxhash
    >>> x = xxhash.xxh32()
    >>> x.update(b'Nobody inspects')
    >>> x.update(b' the spammish repetition')
    >>> x.digest()
    b'\xe2);/'
    >>> x.digest_size
    4
    >>> x.block_size
    16

More condensed:

.. code-block:: python

    >>> xxhash.xxh32(b'Nobody inspects the spammish repetition').hexdigest()
    'e2293b2f'
    >>> xxhash.xxh32(b'Nobody inspects the spammish repetition').digest() == x.digest()
    True

An optional seed (default is 0) can be used to alter the result predictably:

.. code-block:: python

    >>> import xxhash_cffi as xxhash
    >>> xxhash.xxh64('xxhash').hexdigest()
    '32dd38952c4bc720'
    >>> xxhash.xxh64('xxhash', seed=20141025).hexdigest()
    'b559b98d844e0635'
    >>> x = xxhash.xxh64(seed=20141025)
    >>> x.update('xxhash')
    >>> x.hexdigest()
    'b559b98d844e0635'
    >>> x.intdigest()
    13067679811253438005

Be careful that xxh32 takes an unsigned 32-bit integer as seed, while xxh64
takes an unsigned 64-bit integer. Although unsigned integer overflow is
defined behavior, it's better to not to let it happen:

.. code-block:: python

    >>> xxhash.xxh32('I want an unsigned 32-bit seed!', seed=0).hexdigest()
    'f7a35af8'
    >>> xxhash.xxh32('I want an unsigned 32-bit seed!', seed=2**32).hexdigest()
    'f7a35af8'
    >>> xxhash.xxh32('I want an unsigned 32-bit seed!', seed=1).hexdigest()
    'd8d4b4ba'
    >>> xxhash.xxh32('I want an unsigned 32-bit seed!', seed=2**32+1).hexdigest()
    'd8d4b4ba'
    >>>
    >>> xxhash.xxh64('I want an unsigned 64-bit seed!', seed=0).hexdigest()
    'd4cb0a70a2b8c7c1'
    >>> xxhash.xxh64('I want an unsigned 64-bit seed!', seed=2**64).hexdigest()
    'd4cb0a70a2b8c7c1'
    >>> xxhash.xxh64('I want an unsigned 64-bit seed!', seed=1).hexdigest()
    'ce5087f12470d961'
    >>> xxhash.xxh64('I want an unsigned 64-bit seed!', seed=2**64+1).hexdigest()
    'ce5087f12470d961'


``digest()`` returns bytes of the **big-endian** representation of the integer
digest:

.. code-block:: python

    >>> import xxhash_cffi as xxhash
    >>> h = xxhash.xxh64()
    >>> h.digest()
    b'\xefF\xdb7Q\xd8\xe9\x99'
    >>> h.intdigest().to_bytes(8, 'big')
    b'\xefF\xdb7Q\xd8\xe9\x99'
    >>> h.hexdigest()
    'ef46db3751d8e999'
    >>> format(h.intdigest(), '016x')
    'ef46db3751d8e999'
    >>> h.intdigest()
    17241709254077376921
    >>> int(h.hexdigest(), 16)
    17241709254077376921

Besides xxh32/xxh64 mentioned above, oneshot functions are also provided.
By using oneshot functions we can avoid allocating XXH32/64_state on heap:

    | xxh32_digest(bytes, seed=0)
    | xxh32_intdigest(bytes, seed=0)
    | xxh32_hexdigest(bytes, seed=0)
    | xxh64_digest(bytes, seed=0)
    | xxh64_intdigest(bytes, seed=0)
    | xxh64_hexdigest(bytes, seed=0)

.. code-block:: python

    >>> import xxhash_cffi as xxhash
    >>> xxhash.xxh64('a').digest() == xxhash.xxh64_digest('a')
    True
    >>> xxhash.xxh64('a').intdigest() == xxhash.xxh64_intdigest('a')
    True
    >>> xxhash.xxh64('a').hexdigest() == xxhash.xxh64_hexdigest('a')
    True
    >>> xxhash.xxh64_hexdigest('xxhash', seed=20141025)
    'b559b98d844e0635'
    >>> xxhash.xxh64_intdigest('xxhash', seed=20141025)
    13067679811253438005L
    >>> xxhash.xxh64_digest('xxhash', seed=20141025)
    '\xb5Y\xb9\x8d\x84N\x065'


Caveats
-------

SEED OVERFLOW
~~~~~~~~~~~~~~

xxh32 takes an unsigned 32-bit integer as seed, and xxh64 takes
an unsigned 64-bit integer as seed. Make sure that the seed is greater than
or equal to ``0``.

DONT USE XXHASH IN HMAC
~~~~~~~~~~~~~~~~~~~~~~~
Though you can use xxhash as an HMAC_ hash function, but it's
highly recommended not to.

xxhash is **NOT** a cryptographic hash function, it is a
non-cryptographic hash algorithm aimed at speed and quality.
Do not put xxhash in any position where cryptographic hash
functions are required.


Copyright and License
---------------------

Copyright (c) 2014-2018 Yue Du - https://github.com/ifduyue

Licensed under `BSD 2-Clause License <http://opensource.org/licenses/BSD-2-Clause>`_

v1.3.0 2018-12-16
~~~~~~~~~~~~~~~~~

- Wheels are now built automatically
- Split CFFI variant into a separate package `ifduyue/python-xxhash-cffi <https://github.com/ifduyue/python-xxhash-cffi>`_
