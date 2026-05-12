"""Unit tests for error analysis tools."""

import numpy as np
import pytest

from src.core.analysis.errors import (
    compute_error,
    compute_l1_error,
    compute_l2_error,
    compute_linf_error,
    estimate_order,
    compute_all_errors,
)


class TestComputeError:
    """Test suite for compute_error function."""

    def test_l1_error(self):
        """Test L1 error computation."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.1, 3.1])
        error = compute_error(numerical, exact, p=1, dx=1.0)
        assert error == pytest.approx(0.3)

    def test_l2_error(self):
        """Test L2 error computation."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.1, 3.1])
        error = compute_error(numerical, exact, p=2, dx=1.0)
        expected = np.sqrt(0.03)
        assert error == pytest.approx(expected)

    def test_linf_error(self):
        """Test L-infinity error computation."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.2, 3.1])
        error = compute_error(numerical, exact, p=float("inf"))
        assert error == pytest.approx(0.2)

    def test_zero_error(self):
        """Test zero error when numerical equals exact."""
        arr = np.array([1.0, 2.0, 3.0])
        error = compute_error(arr, arr, p=2)
        assert error == 0.0

    def test_shape_mismatch(self):
        """Test error on shape mismatch."""
        with pytest.raises(ValueError, match="Shape mismatch"):
            compute_error(np.array([1.0]), np.array([1.0, 2.0]))

    def test_invalid_p(self):
        """Test error on invalid p value."""
        with pytest.raises(ValueError, match="p must be positive"):
            compute_error(np.array([1.0]), np.array([1.0]), p=0)


class TestConvenienceFunctions:
    """Test suite for convenience error functions."""

    def test_compute_l1_error(self):
        """Test L1 error convenience function."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.1, 3.1])
        error = compute_l1_error(numerical, exact, dx=1.0)
        assert error == pytest.approx(0.3)

    def test_compute_l2_error(self):
        """Test L2 error convenience function."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.1, 3.1])
        error = compute_l2_error(numerical, exact, dx=1.0)
        expected = np.sqrt(0.03)
        assert error == pytest.approx(expected)

    def test_compute_linf_error(self):
        """Test L-infinity error convenience function."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.2, 3.1])
        error = compute_linf_error(numerical, exact)
        assert error == pytest.approx(0.2)

    def test_compute_all_errors(self):
        """Test compute_all_errors function."""
        numerical = np.array([1.0, 2.0, 3.0])
        exact = np.array([1.1, 2.1, 3.1])
        errors = compute_all_errors(numerical, exact, dx=1.0)
        assert "l1" in errors
        assert "l2" in errors
        assert "linf" in errors
        assert errors["l1"] == pytest.approx(0.3)


class TestEstimateOrder:
    """Test suite for convergence order estimation."""

    def test_first_order(self):
        """Test first-order convergence detection."""
        dx = np.array([0.1, 0.05, 0.025])
        errors = np.array([0.1, 0.05, 0.025])
        order = estimate_order(dx, errors)
        assert order == pytest.approx(1.0, abs=0.1)

    def test_second_order(self):
        """Test second-order convergence detection."""
        dx = np.array([0.1, 0.05, 0.025])
        errors = np.array([0.01, 0.0025, 0.000625])
        order = estimate_order(dx, errors)
        assert order == pytest.approx(2.0, abs=0.1)

    def test_length_mismatch(self):
        """Test error on length mismatch."""
        with pytest.raises(ValueError, match="Length mismatch"):
            estimate_order(np.array([0.1]), np.array([0.1, 0.05]))

    def test_insufficient_points(self):
        """Test error with insufficient points."""
        with pytest.raises(ValueError, match="at least 2 points"):
            estimate_order(np.array([0.1]), np.array([0.1]))

    def test_invalid_values(self):
        """Test error with invalid values."""
        with pytest.raises(ValueError, match="must be positive"):
            estimate_order(np.array([0.1, 0.0]), np.array([0.1, 0.05]))
