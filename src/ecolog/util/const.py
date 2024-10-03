
from enum import Enum as PyEnum
from aenum import Enum, EnumMeta
from collections.abc import Hashable
import sys

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self

from ecolog.util.namespace import is_system_attr


class MetaConst(EnumMeta):
    # metaclass for a Const enum

    def is_system_attr(k: str, v: Any) -> bool:
        return is_system_attr(k, v)

    def __new__(mcls, name: str, *args, **kw):
        zero = int(0)
        name = sys.intern(name)

        if len(args) is zero and len(kw) is zero:
            return mcls[name]

        attrs: Mapping[str, Any] = args[1]
        args = list(args)

        inattrs = dict()
        for k, v in attrs.items():
            # call sys.intern for any name, value pairs
            # for which sys.intern(obj) does not raise a
            # TypeError, excepting any name, value pair
            # interpreted as denoting a system attribute
            # for the class namespace. In effect, this 
            # should sys.intern any string name and any
            # string value provided for an enum member.
            # 
            # It's assumed that any system attribute name 
            # may be automatically sys.intern'd within the 
            # Python implementation.
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
    # Const enum base class
    if TYPE_CHECKING:
        name: str
        value: Hashable
        _member_map_: ClassVar[dict[str, Self]]
        _value2member_map_: ClassVar[dict[Hashable, Self]]

    def __hash__(self) -> int:
        # memoization for hash code
        try:
            return self._hash
        except AttributeError:
            pass
        _h = hash(self.value)
        self._hash = _h
        return _h

    def __eq__(self, value: Any) -> bool:
        # If 'value' is of the same class
        # as self, then it must be the
        # same object as self, in order
        # for the Const 'value' to be
        # __eq__ to self.
        #
        # Otherwise, this will use a 
        # comparison of hash values. 
        # Given the implementation of
        # self.__hash__,  this may allow
        # for comparing the provided 
        # 'value' to the enum member 
        # value for the Const enum
        # member provided here as 'self'.
        # 
        # If a hash code cannot be determined
        # for the value, then it's assumed to
        # not be __eq__ to self
        #
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
        # __hash__ must be defined here, 
        # given the implementaiton of __eq__
        # in this class
        return super().__hash__()

    def __eq__(self, value: Any) -> bool:
        # hash-based comparison under
        # sys.intern, optimized for
        # when the value is of the same
        # class as self
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
