# Distroless Python ctypes bug

I attempted to run gunicorn using the Distroless Python image and got the following traceback. It comes from [gunicorn's sendfile compatibility code](https://github.com/benoitc/gunicorn/blob/master/gunicorn/http/_sendfile.py), which uses the Python standard library's ctypes.util.find_library("c"). On Linux, this attempts to do two things:

1. Call `ldconfig -p` and search the output to find the library. Distroless does not include `ldconfig` or the `/etc/ld.so.cache` file used to generate the results.
2. If that fails, it runs a shell script that tries to execute GCC. This fails because Distroless does not include a shell or GCC.

I've reproduced this error here, and have included two fixes
* `//:hello_py_with_ldconfig_and_cache` includes `ldconfig` and `/etc/ld.so.cache`. This is problematic because `ld.so.cache` should be regenerated if the set of libraries changes.
* `//:hello_py_with_dash` includes `dash`. This makes the shell command run but exit with a failure code, which means `find_library` returns `None`. Through some miraculous bug, `ctypes` treats `None` like the C library, so this makes gunicorn work!

I think the "best" fix would be to somehow generate the `/etc/ld.so.cache` file. On Linux, this could be done by writing a Bazel rule to unpack the file system image, run `ldconfig -r (ROOT DIR)` then take the output file out. However, this seems like a lot of work.

I filed a [Distroless bug for this issue](https://github.com/GoogleCloudPlatform/distroless/issues/150).


## Original Gunicorn trace

```
Traceback (most recent call last):
  File "/tmp/install/gunicorn-19.7.1-py2.py3-none-any.whl.9d2a2d914e9838232744d125e8d8a41509c11c9d/gunicorn-19.7.1-py2.py3-none-any.whl/gunicorn/util.py", line 134, in load_class
    mod = import_module('.'.join(components))
  File "/usr/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
  File "/tmp/install/gunicorn-19.7.1-py2.py3-none-any.whl.9d2a2d914e9838232744d125e8d8a41509c11c9d/gunicorn-19.7.1-py2.py3-none-any.whl/gunicorn/workers/sync.py", line 16, in <module>
    import gunicorn.http.wsgi as wsgi
  File "/tmp/install/gunicorn-19.7.1-py2.py3-none-any.whl.9d2a2d914e9838232744d125e8d8a41509c11c9d/gunicorn-19.7.1-py2.py3-none-any.whl/gunicorn/http/wsgi.py", line 24, in <module>
    from ._sendfile import sendfile
  File "/tmp/install/gunicorn-19.7.1-py2.py3-none-any.whl.9d2a2d914e9838232744d125e8d8a41509c11c9d/gunicorn-19.7.1-py2.py3-none-any.whl/gunicorn/http/_sendfile.py", line 27, in <module>
    _libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
  File "/usr/lib/python2.7/ctypes/util.py", line 285, in find_library
    return _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name))
  File "/usr/lib/python2.7/ctypes/util.py", line 103, in _findLib_gcc
    stdout=subprocess.PIPE)
  File "/usr/lib/python2.7/subprocess.py", line 390, in __init__
    errread, errwrite)
  File "/usr/lib/python2.7/subprocess.py", line 1024, in _execute_child
    raise child_exception
OSError: [Errno 2] No such file or directory
```