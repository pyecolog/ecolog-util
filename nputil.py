"""Python utilities for numpy applications"""

from typing import Any
import numpy as np
import numpy.typing as npt


def is_nan(value: Any) -> bool:
    try:
        return np.isnan(value)
    except TypeError:
        return False


@np.vectorize()
def is_nan_vec(value: npt.ArrayLike) -> npt.ArrayLike:
    return is_nan(value)


def is_nan_all(values: npt.ArrayLike) -> bool:
    return np.all(is_nan_vec(values))
