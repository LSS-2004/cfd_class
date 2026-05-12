"""Error analysis and convergence assessment tools.

Provides error metrics and convergence order estimation for
comparing numerical solutions against exact solutions.
"""

from typing import Union

import numpy as np
from numpy.typing import NDArray


def compute_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    p: Union[int, float] = 2,
    dx: float = 1.0,
) -> float:
    """Compute p-norm error between numerical and exact solutions.

    Args:
        numerical: Numerical solution array
        exact: Exact solution array
        p: Norm order (1=L1, 2=L2, inf=L-infinity)
        dx: Grid spacing for integral approximation

    Returns:
        Error value

    Raises:
        ValueError: If arrays have different shapes or p is invalid
    """
    if numerical.shape != exact.shape:
        raise ValueError(
            f"Shape mismatch: {numerical.shape} vs {exact.shape}"
        )

    if p == float("inf"):
        return float(np.max(np.abs(numerical - exact)))

    if p <= 0:
        raise ValueError(f"p must be positive or inf, got {p}")

    diff = np.abs(numerical - exact)
    return float((np.sum(diff**p) * dx) ** (1.0 / p))


def compute_l1_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    dx: float = 1.0,
) -> float:
    """Compute L1 error.

    Args:
        numerical: Numerical solution array
        exact: Exact solution array
        dx: Grid spacing

    Returns:
        L1 error value
    """
    return compute_error(numerical, exact, p=1, dx=dx)


def compute_l2_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    dx: float = 1.0,
) -> float:
    """Compute L2 error.

    Args:
        numerical: Numerical solution array
        exact: Exact solution array
        dx: Grid spacing

    Returns:
        L2 error value
    """
    return compute_error(numerical, exact, p=2, dx=dx)


def compute_linf_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
) -> float:
    """Compute L-infinity (maximum) error.

    Args:
        numerical: Numerical solution array
        exact: Exact solution array

    Returns:
        L-infinity error value
    """
    return compute_error(numerical, exact, p=float("inf"))


def estimate_order(
    dx_values: NDArray[np.float64],
    errors: NDArray[np.float64],
) -> float:
    """Estimate convergence order from error data.

    Uses log-log linear regression:
    error ~ C * dx^p
    log(error) = log(C) + p * log(dx)

    Args:
        dx_values: Array of grid spacings
        errors: Array of corresponding errors

    Returns:
        Estimated convergence order p

    Raises:
        ValueError: If arrays have different lengths or invalid values
    """
    if len(dx_values) != len(errors):
        raise ValueError(
            f"Length mismatch: {len(dx_values)} vs {len(errors)}"
        )

    if len(dx_values) < 2:
        raise ValueError("Need at least 2 points for order estimation")

    # Filter out zero or negative values
    mask = (dx_values > 0) & (errors > 0)
    if not np.all(mask):
        raise ValueError("All dx and error values must be positive")

    log_dx = np.log(dx_values[mask])
    log_err = np.log(errors[mask])

    # Linear regression
    n = len(log_dx)
    if n < 2:
        raise ValueError("Need at least 2 valid points")

    # Slope = convergence order
    x_mean = np.mean(log_dx)
    y_mean = np.mean(log_err)

    numerator = np.sum((log_dx - x_mean) * (log_err - y_mean))
    denominator = np.sum((log_dx - x_mean) ** 2)

    if abs(denominator) < 1e-14:
        raise ValueError("Cannot estimate order: dx values are too similar")

    return float(numerator / denominator)


def compute_all_errors(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    dx: float = 1.0,
) -> dict:
    """Compute all error metrics.

    Args:
        numerical: Numerical solution array
        exact: Exact solution array
        dx: Grid spacing

    Returns:
        Dictionary with L1, L2, and L-infinity errors
    """
    return {
        "l1": compute_l1_error(numerical, exact, dx),
        "l2": compute_l2_error(numerical, exact, dx),
        "linf": compute_linf_error(numerical, exact),
    }
