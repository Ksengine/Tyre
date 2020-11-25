import __future__

# 1. Import Version (replace by all/base/Version section) ---
from .base import version
# ---

# 2. Import built-ins ---
try:
    import builtins
except:
    import __builtin__ as builtins
# ---

# 3. python `exec` method (1. required)---
Exec = getattr(builtins, "exec")
if version < 3:
    from sys import _getframe

    def Exec(_code_, _globs_=None, _locs_=None):
        """
        Execute the given source in the context of globals and locals.
        
        The source may be a string representing one or more Python statements
        or a code object as returned by compile().
        The globals must be a dictionary and locals can be any mapping,
        defaulting to the current globals and locals.
        If only globals is given, locals defaults to it.
        """
        if _globs_ is None:
            frame = _getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("""exec _code_ in _globs_, _locs_""")


# ---

# 3. python `print` method (1. required)---
if version >= 3:
    unicode = str


def Print_(*args, **kwargs):
    """
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
    
    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    """
    fp = kwargs.pop("file", stdout)
    if not fp:
        return

    def write(data):
        # If the file has an encoding, encode unicode with it.
        if isinstance(fp, file) and fp.encoding:
            errors = getattr(fp, "errors", "strict")
            data = data.encode(fp.encoding, errors)
        fp.write(data)

    sep = unicode(kwargs.pop("sep", " "))
    end = unicode(kwargs.pop("end", "\n"))
    if kwargs:
        raise TypeError("invalid keyword arguments to print() - {}".format(
            ", ".join(kwargs)))
    for arg in args:
        write(unicode(arg))
    write(end)


Print = getattr(builtins, "print", Print_)

if version < 3.3:

    def Print(*args, **kwargs):
        fp = kwargs.get("file", sys.stdout)
        flush = kwargs.pop("flush", False)
        Print_(*args, **kwargs)
        if flush and fp is not None:
            fp.flush()


# ---


# 4. like python3 raise exc_value from exc_value_from  (1. required) (2. required)---
def raise_from(value, from_value):
    raise value


if version >= 3:
    exec_("""def raise_from(value, from_value):
    try:raise value from from_value
    finally:value = None
""")
# ---


# 3. Reraise an exception (1. required) (2. required)---
def reraise(tp, value, tb=None):
    try:
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None
        tb = None


if version < 3:
    exec_("""def reraise(tp, value, tb=None):
    try:raise tp, value, tb
    finally:tb = None
""")
# ---


# metaclass (1. required) ---
from types import resolve_bases


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            if version >= 3.7:
                # This version introduced PEP 560 that requires a bit
                # of extra care (we mimic what is done by __build_class__).
                resolved_bases = resolve_bases(bases)
                if resolved_bases != bases:
                    d['__orig_bases__'] = bases
            else:
                resolved_bases = bases
            return meta(name, resolved_bases, d)

        @classmethod
        def __prepare__(cls, name, this_bases):
            return meta.__prepare__(name, bases)

    return type.__new__(metaclass, 'temporary_class', (), {})


# ---


# metaclass decorator (1. required) ---
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


# ---
