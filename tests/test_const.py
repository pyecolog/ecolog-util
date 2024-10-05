
import enum
import aenum
import sys

from types import new_class
import typing as t

from ecolog.util.const import Const, StrConst, IntConst, FlagConst


const_obj = object()


class ConstA(Const):
    # check without member conversion
    A = "a"
    B = 0xb
    C = b'c'
    D = const_obj


def check_enum_new_class(ecls: enum.Enum):
    # returns a class with the same bases as ecls
    #
    # presently, a subclass of ecls cannot be
    # defined if ecls is an enum class with
    # defined members
    #
    clsname = "".join((ecls.__name__, "Prime"))
    bases = ecls.__bases__
    #
    # create the enum class, then extend
    # with each name, value pair
    #
    ne = new_class(clsname, bases)
    #
    # a simple iterator onto ecls may not capture
    # all members for the flag enum, so iterating
    # directly onto ecls._member_map_
    #
    for name, member in ecls._member_map_.items():
        aenum.extend_enum(ne, name, member.value)
    check_enum_members(ne)
    assert ne._member_map_ == ecls._member_map_
    return ne


def check_enum_members(ecls: enum.Enum):
    for member in ecls:
        name = member.name
        assert name is sys.intern(name)
        assert member is getattr(ecls, name)
        assert member is ecls[name]
        assert isinstance(member, ecls)


def check_enum(ecls: enum.Enum):
    assert issubclass(ecls, enum.Enum)
    assert issubclass(ecls, aenum.Enum)
    for bc in ecls.__bases__:
        assert issubclass(ecls, bc)
        bcb = bc.__bases__
        assert bcb
        for bcprime in bcb:
            assert issubclass(ecls, bcprime)

    check_enum_members(ecls)
    eprime = check_enum_new_class(ecls)
    check_enum_members(eprime)


def test_const():
    check_enum(ConstA)
    assert ConstA.A == "a"
    assert ConstA.A.value is sys.intern("a")
    assert ConstA.B == 0xb
    assert ConstA.C == b'c'
    assert ConstA.D == const_obj
    assert ConstA.D.value is const_obj


class ConstB(StrConst):
    # test with intrinsic conversion to string
    A = "a"
    B = b'bstr'
    C = False


def test_str_const():
    check_enum(ConstB)
    assert ConstB.A == 'a'
    assert ConstB.B != b'bstr'
    assert ConstB.B == str(b'bstr')
    assert ConstC.C != False
    assert ConstB.C == str(False)


class ConstC(IntConst):
    # test with intrinsic conversion to int
    A = 0xa
    B = -0xb
    C = "5"
    D = False


def test_int_const():
    check_enum(ConstC)
    assert ConstC.A == 0xa
    assert ConstC.B == -0xb
    assert ConstC.C == 5
    ac_union = ConstC.A | ConstC.C
    assert isinstance(ac_union, int)
    assert not isinstance(ac_union, ConstC)
    assert ac_union == ConstC.A.value | ConstC.C.value
    assert ConstC.D == 0


class ConstD(FlagConst):
    # test with intrinsic conversion to int
    # and logical operations onto member values
    # such that may return a new enum member
    NONE = 0
    A = 1
    B = 2
    C = 4
    AB = 3
    D = "5"
    # the following would generally not be
    # recommended for a flag value, but this
    # will not fail in this implementation
    E = -5


def test_flag_const():
    check_enum(ConstD)
    assert ConstD.NONE == 0
    assert ConstD.NONE == False
    assert ConstD.A == 1
    assert ConstD.B == 2
    assert ConstD.C == 4
    ab_union = ConstD.A | ConstD.B
    assert isinstance(ab_union, ConstD)
    assert ConstD.AB == ab_union
    assert ConstD.D == 5
    assert ConstD.E == -5


if __name__ == "__main__":
    test_const()
    test_str_const()
    test_int_const()
    test_flag_const()
