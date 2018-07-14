import sys
import struct
import binascii

from xxhash_cffi._cffi import ffi, lib

PY3 = sys.version_info[0] == 3

XXHASH_VERSION = "%d.%d.%d" % (lib.XXH_VERSION_MAJOR,
                               lib.XXH_VERSION_MINOR,
                               lib.XXH_VERSION_RELEASE)


def _get_buffer(val):
    """
    Best-effort function to get the pointer and byte length of a buffer-like
    object.
    """
    if PY3 and isinstance(val, str):
        return val.encode('utf8'), len(val)
    if isinstance(val, bytes):
        return val, len(val)
    cdata = ffi.from_buffer(val)
    return cdata, len(cdata)

def xxh32_digest(input, seed=0):
    return struct.pack('>I', xxh32_intdigest(input, seed))

def xxh32_intdigest(input, seed=0):
    seed &= (2 ** 32 -1)
    buf, len = _get_buffer(input)
    return lib.XXH32(buf, len, seed)

def xxh32_hexdigest(input, seed=0):
    return binascii.hexlify(xxh32_digest(input, seed))

class xxh32(object):
    digest_size = digestsize = 4
    block_size = 16

    def __init__(self, input=None, seed=0):
        self.xxhash_state = lib.XXH32_createState()
        self.seed = seed & (2 ** 32 - 1)
        self.reset()
        if input is not None:
            self.update(input)

    def update(self, input):
        lib.XXH32_update(self.xxhash_state, *_get_buffer(input))

    def intdigest(self):
        return lib.XXH32_digest(self.xxhash_state)

    def digest(self):
        return struct.pack('>I', self.intdigest())

    def hexdigest(self):
        return binascii.hexlify(self.digest())

    def reset(self):
        lib.XXH32_reset(self.xxhash_state, self.seed)

    def copy(self):
        new = type(self)()
        lib.XXH32_copyState(new.xxhash_state, self.xxhash_state)
        new.seed = self.seed
        return new

    def __del__(self):
        lib.XXH32_freeState(self.xxhash_state)

def xxh64_digest(input, seed=0):
    return struct.pack('>Q', xxh64_intdigest(input, seed))

def xxh64_intdigest(input, seed=0):
    seed &= (2 ** 64 - 1)
    buf, len = _get_buffer(input)
    return lib.XXH64(buf, len, seed)

def xxh64_hexdigest(input, seed=0):
    return binascii.hexlify(xxh64_digest(input, seed))

class xxh64(object):
    digest_size = digestsize = 8
    block_size = 32

    def __init__(self, input=None, seed=0):
        self.xxhash_state = lib.XXH64_createState()
        self.seed = seed & (2 ** 64 - 1)
        self.reset()
        if input is not None:
            self.update(input)

    def update(self, input):
        lib.XXH64_update(self.xxhash_state, *_get_buffer(input))

    def intdigest(self):
        return lib.XXH64_digest(self.xxhash_state)

    def digest(self):
        return struct.pack('>Q', self.intdigest())

    def hexdigest(self):
        return binascii.hexlify(self.digest())

    def reset(self):
        lib.XXH64_reset(self.xxhash_state, self.seed)

    def copy(self):
        new = type(self)()
        lib.XXH64_copyState(new.xxhash_state, self.xxhash_state)
        new.seed = self.seed
        return new

    def __del__(self):
        lib.XXH64_freeState(self.xxhash_state)
