import inspect
from functools import partialmethod
from typing import Any


def is_system_attr(name: str, value: Any) -> bool:
    """Return True if `(name, value)` denotes a *system attribute* 
    for some form of a Python *namespace*.

    Parameters
    ----------
    name : str
        attribute name
    value : Any
        attribute value

    Returns
    -------
    bool
        estimation of whether `(name, value)` denotes a _system attribute_

    Description
    -------
    If `name` is prefixed with the string `"_"` or if  `value` is one of a
    function, data descriptor, method descriptor (as per {:py:mod:}`inspect`), or
    partial method, returns True, else returns False.

    Contrasted to a test onto `callable(value)` this function will not return True
    if  `value` is provided as a *type* and `name` does not start with `"_"`.
    """
    return (
        (isinstance(name, str) and name.startswith("_")) or
        # callable(value) or # returns True if value is a type
        inspect.isfunction(value) or
        inspect.isdatadescriptor(value) or
        inspect.ismethoddescriptor(value) or
        isinstance(value, partialmethod)
    )
