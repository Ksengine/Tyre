import __future__

# 1. Version - python version as float(eg:-3.9 or 4.0(=3.10)) ---
from sys import version_info
version = version_info[0] + version_info[1] / 10
# ---

# Types - for check(eg:-`isinstance(100, integer_types)`) or convert types ---
string_types = (str, ) if version >= 3 else (basestring,
                                             )  # 1. Version required

integer_types = (int, ) if version >= 3 else (int, long)  # 1. Version required

## ClassTypes # 1. Version required---
try:
    from types import ClassType
except ImportError:
    ClassType = None
class_types = (type, ) if version >= 3 else (type, ClassType)
## ---

text_type = str if version >= 3 else (unicode)  # 1. Version required

binary_type = bytes if version >= 3 else (type, str)  # 1. Version required
# ---

# Maxsize ---
try:
    from sys import maxsize as MAXSIZE

except ImportError:
    from sys import platform
    if platform.startswith("java"):
        # Jython always uses 32 bits.
        MAXSIZE = int((1 << 31) - 1)

    else:
        # It's possible to have sizeof(long) != sizeof(Py_ssize_t).
        class X(object):
            def __len__(self):
                return 1 << 31

        try:
            len(X())

        except OverflowError:
            # 32-bit
            MAXSIZE = int((1 << 31) - 1)

        else:
            # 64-bit
            MAXSIZE = int((1 << 63) - 1)

        del X
# ----
