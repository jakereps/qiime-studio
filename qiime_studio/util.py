# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import sys

from contextlib import contextmanager
from functools import wraps

from flask import jsonify

# Taken whole-sale from: http://stackoverflow.com/a/22434262/579416
@contextmanager
def redirected_stdio(to=os.devnull, stdio=None):
    if stdio is None:
        stdio = sys.stdout

    stdio_fd = _get_fileno(stdio)
    # copy stdio_fd before it is overwritten
    # NOTE: `copied` is inheritable on Windows when duplicating a standard
    # stream
    with os.fdopen(os.dup(stdio_fd), 'wb') as copied:
        stdio.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(_get_fileno(to), stdio_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdio_fd)  # $ exec > to
        try:
            yield stdio  # allow code to be run with the redirected stdio
        finally:
            # restore stdio to its previous value
            # NOTE: dup2 makes stdio_fd inheritable unconditionally
            stdio.flush()
            os.dup2(copied.fileno(), stdio_fd)  # $ exec >&copied


def _get_fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd


def fail_gracefully(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            r = jsonify({'error': str(e)})
            r.status_code = 400
            return r
    return func_wrapper
