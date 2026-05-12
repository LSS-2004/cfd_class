"""Unit tests for exact Riemann solver."""

import numpy as np
import pytest

from src.core.solvers.exact import ExactRiemannSolver, RiemannState


class TestExactRiemannSolver:
    """Test suite for ExactRiemannSolver."""

    def test_init(self):
        """Test solver initialization."""
        solver = ExactRiemannSolver()
        assert solver.g == 9.81
        assert solver.tol == 1e-6
        assert solver.max_iter == 100

    def test_dry_bed_left(self):
        """Test dry bed on left side."""
        solver = ExactRiemannSolver()
        state = solver.solve(0.0, 0.0, 1.0, 0.0)
        assert state.h == 0.0
        assert state.wave_speeds[1] > 0

    def test_dry_bed_right(self):
        """Test dry bed on right side."""
        solver = ExactRiemannSolver()
        state = solver.solve(1.0, 0.0, 0.0, 0.0)
        assert state.h == 0.0
        assert state.wave_speeds[0] < 0

    def test_dry_bed_both(self):
        """Test dry bed on both sides."""
        solver = ExactRiemannSolver()
        state = solver.solve(0.0, 0.0, 0.0, 0.0)
        assert state.h == 0.0
        assert state.u == 0.0

    def test_wet_bed_symmetric(self):
        """Test symmetric wet bed case."""
        solver = ExactRiemannSolver()
        state = solver.solve(1.0, 0.0, 1.0, 0.0)
        assert state.h == pytest.approx(1.0, abs=1e-6)
        assert state.u == pytest.approx(0.0, abs=1e-6)

    def test_wet_bed_dam_break(self):
        """Test classic dam break problem."""
        solver = ExactRiemannSolver()
        state = solver.solve(1.0, 0.0, 0.1, 0.0)
        assert state.h > 0.1
        assert state.h < 1.0
        assert state.wave_speeds[0] < 0
        assert state.wave_speeds[1] > 0

    def test_riemann_state_dataclass(self):
        """Test RiemannState dataclass."""
        state = RiemannState(1.0, 0.5, (-1.0, 1.0, 0.0))
        assert state.h == 1.0
        assert state.u == 0.5
        assert state.wave_speeds == (-1.0, 1.0, 0.0)

    def test_sample_solution_t0(self):
        """Test sample solution at t=0."""
        solver = ExactRiemannSolver()
        x = np.linspace(-1, 1, 100)
        h, u = solver.sample_solution(1.0, 0.0, 0.1, 0.0, x, 0.0)
        assert np.all(h[x < 0] == 1.0)
        assert np.all(h[x >= 0] == 0.1)
        assert np.all(u == 0.0)

    def test_sample_solution_positive_time(self):
        """Test sample solution at positive time."""
        solver = ExactRiemannSolver()
        x = np.linspace(-1, 1, 100)
        h, u = solver.sample_solution(1.0, 0.0, 0.1, 0.0, x, 0.5)
        assert len(h) == 100
        assert len(u) == 100
        assert np.all(h >= 0)

    def test_riemann_state_immutable(self):
        """Test RiemannState is immutable."""
        state = RiemannState(1.0, 0.5, (-1.0, 1.0, 0.0))
        with pytest.raises(AttributeError):
            state.h = 2.0

    def test_sample_solution_dry_bed(self):
        """Test sample solution with dry bed."""
        solver = ExactRiemannSolver()
        x = np.linspace(-1, 1, 100)
        h, u = solver.sample_solution(1.0, 0.0, 0.0, 0.0, x, 0.5)
        assert len(h) == 100
        assert np.all(h >= 0)

    def test_newton_iteration_convergence(self):
        """Test Newton iteration converges for various cases."""
        solver = ExactRiemannSolver()

        test_cases = [
            (1.0, 0.0, 0.5, 0.0),
            (2.0, 1.0, 1.0, -0.5),
            (1.0, 0.0, 0.1, 0.0),
            (0.5, 0.0, 1.0, 0.0),
        ]

        for h_l, u_l, h_r, u_r in test_cases:
            state = solver.solve(h_l, u_l, h_r, u_r)
            assert state.h > 0
            assert state.wave_speeds[0] < state.wave_speeds[1]
