import __future__
# 1. Import Version (replace by all/base/Version section)
from .base import version
# ----------------------------------------------------

# 2. Import MethodType from types------------------------
from types import MethodType
# ----------------------------------------------------


def get_unbound_function(unbound):  # 1 and 2 required
    """Get the function out of a possibly unbound function"""
    return unbound if version >= 3 else unbound.im_func


def create_bound_method(func, obj):  # 1 and 2 required
    """Return a method object wrapping func and bound to obj"""
    return MethodType(func, obj) if version >= 3 else MethodType(
        func, obj, obj.__class__)


def create_unbound_method(func, cls):  # 1 and 2 required
    """Return an unbound method object wrapping func."""
    return func if version >= 3 else MethodType(func, None, cls)


# 3. Import attrgetter from operators-----------------
from operator import attrgetter
# ----------------------------------------------------

get_method_function = attrgetter(
    "__func__" if version >= 3 else "im_func")  # 1 and 3 required

get_method_self = attrgetter(
    "__self__" if version >= 3 else "im_self")  # 1 and 3 required

get_function_closure = attrgetter(
    "__closure__" if version >= 3 else "func_closure")  # 1 and 3 required

get_function_code = attrgetter(
    "__code__" if version >= 3 else "func_code")  # 1 and 3 required

get_function_defaults = attrgetter(
    "__defaults__" if version >= 3 else "func_defaults")  # 1 and 3 required

get_function_globals = attrgetter(
    "__globals__" if version >= 3 else "func_globals")  # 1 and 3 required

# 4. python `next` method -------------------------------
try:
    next = next
except NameError:

    def next(iterator, *args):
        """
        next(iterator[, default])

        Return the next item from the iterator. If default is given and the iterator
        is exhausted, it is returned instead of raising StopIteration.
        """
        if len(args) > 2:
            raise TypeError("next expected at most 2 arguments, got {}".format(
                len(args)))
        try:
            return iterator.__next__()
        except StopIteration:
            if len(args) == 2:
                return args[1]
            raise


# ----------------------------------------------------

# 3. python `callable` method ---------------------------
try:
    callable = callable
except NameError:

    def callable(obj):
        """
        Return whether the object is callable (i.e., some kind of function).

        Note that classes are callable, as are instances of classes with a
        __call__() method.
        """
        return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)


# ----------------------------------------------------


def iterkeys(d, **kw):  # 1 required
    """Return an iterator over the keys of a dictionary."""
    return iter(d.keys(**kw)) if version >= 3 else d.iterkeys(**kw)


def itervalues(d, **kw):  # 1 required
    """Return an iterator over the values of a dictionary."""
    return iter(d.values(**kw)) if version >= 3 else d.itervalues(**kw)


def iteritems(d, **kw):  # 1 required
    """Return an iterator over the (key, value) pairs of a dictionary."""
    return iter(d.items(**kw)) if version >= 3 else d.iteritems(**kw)


def iterlists(d, **kw):  # 1 required
    """Return an iterator over the (key, [values]) pairs of a dictionary."""
    return iter(d.lists(**kw)) if version >= 3 else d.iterlists(**kw)


# 4. Import attrgetter from operators-----------------
from operator import methodcaller
# ----------------------------------------------------

viewkeys = methodcaller(
    "keys" if version >= 3 else "viewkeys")  # 1 and 4 required

viewvalues = methodcaller(
    "values" if version >= 3 else "viewvalues")  # 1 and 4 required

viewitems = methodcaller(
    "items" if version >= 3 else "viewitems")  # 1 and 4 required


# python `iter` method -------------------------------
class Iterator(object):
    def next(self, *args):
        return type(self).__next__(self, args)


if version >= 3: Iterator = object
# ----------------------------------------------------

# `functools.wraps` method ---------------------------
from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES, update_wrapper, partial, wraps
if version < 3.4:
    # This does exactly the same what the :func:`py3:functools.update_wrapper`
    # function does on Python versions after 3.2. It sets the ``__wrapped__``
    # attribute on ``wrapper`` object and it doesn't raise an error if any of
    # the attributes mentioned in ``assigned`` and ``updated`` are missing on
    # ``wrapped`` object.
    def _update_wrapper(wrapper,
                        wrapped,
                        assigned=WRAPPER_ASSIGNMENTS,
                        updated=WRAPPER_UPDATES):
        for attr in assigned:
            if hasattr(wrapped, attr): setattr(wrapper, attr, value)
        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
        wrapper.__wrapped__ = wrapped
        return wrapper

    _update_wrapper.__doc__ = update_wrapper.__doc__

    def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
        return partial(_update_wrapper,
                       wrapped=wrapped,
                       assigned=assigned,
                       updated=updated)

    wraps.__doc__ = wraps.__doc__
else:
    wraps = wraps
# ----------------------------------------------------
