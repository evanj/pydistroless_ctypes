#!/usr/bin/python

print "hello world"

import ctypes
import ctypes.util
_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
_sendfile = _libc.sendfile
print _libc
print _sendfile

_write = _libc.write
message = "hello a string from write\n"
out = _write(1, message, len(message))
print "write returned:", out

