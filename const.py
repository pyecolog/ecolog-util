
from enum import Enum as PyEnum
from aenum import Enum, StrEnum, EnumMeta
from collections.abc import Hashable
from functools import partialmethod
import inspect
import sys

from typing import TYPE_CHECKING, Any, ClassVar, Self


def is_system_attr(name: str, value: Any) -> bool:
    """Return True if `(name, value)` denotes a *system attribute*

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
    partial method, returns True, else returns False
    """
    return (
        (isinstance(name, str) and name.startswith("_")) or
        inspect.isfunction(value) or
        inspect.isdatadescriptor(value) or
        inspect.ismethoddescriptor(value) or
        isinstance(value, partialmethod)
    )


class MetaConst(EnumMeta):

    def is_system_attr(k: str, v: Any) -> bool:
        return is_system_attr(k, v)

    def __new__(mcls, name: str, *args, **kw):
        zero = int(0)
        name = sys.intern(name)

        if len(args) is zero and len(kw) is zero:
            return mcls[name]

        attrs: dict[str, str] = args[1]
        args = list(args)

        inattrs = dict()
        for k, v in attrs.items():
            if mcls.is_system_attr(k, v):
                inattrs[k] = v
            else:
                try:
                    k = sys.intern(k)
                except TypeError:
                    pass
                try:
                    v = sys.intern(v)
                except TypeError:
                    pass
                inattrs[k] = v

        args[1] = inattrs

        return super().__new__(mcls, name, *args, **kw)

    def __getitem__(self, key: str) -> Self:
        return self._members_[key]


class Const(Enum, metaclass=MetaConst):
    if TYPE_CHECKING:
        name: str
        value: Hashable
        _member_map_: ClassVar[dict[str, Self]]
        _value2member_map_: ClassVar[dict[Hashable, Self]]

    def __hash__(self) -> int:
        try:
            return self._hash
        except AttributeError:
            pass
        _h = hash(self.value)
        self._hash = _h
        return _h

    def __eq__(self, value: Any) -> bool:
        if self.__class__ is value.__class__:
            return self is value
        try:
            return hash(self) == hash(value)
        except TypeError:
            return False


class StrConst(str, Const):
    if TYPE_CHECKING:
        value: str
        _value2member_map_: ClassVar[dict[str, Self]]

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        # must be defined here, for this class to be hashable
        return super().__hash__()

    def __eq__(self, value: Any) -> bool:
        vcls = value.__class__
        if self.__class__ is vcls:
            return self is value
        elif issubclass(vcls, str):
            if issubclass(vcls, PyEnum):
                try:
                    value = sys.intern(str(value))
                except TypeError:
                    return False
            else:
                try:
                    value = sys.intern(value)
                except TypeError:
                    return False
            return self.value is value
        else:
            return False
