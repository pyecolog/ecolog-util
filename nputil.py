"""Python utilities for numpy applications"""

import numpy as np
import numpy.typing as npt


def is_nan(value) -> bool:
    try:
        return np.isnan(value)
    except TypeError:
        return False


@np.vectorize()
def is_nan_values(value: npt.ArrayLike) -> bool:
    return is_nan(value)


def is_nan_all(values: npt.ArrayLike) -> bool:
    return np.all(is_nan_values(values))
