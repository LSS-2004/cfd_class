"""Regression tests for numerical schemes.

These tests verify that simulation results match reference solutions
within acceptable tolerances to detect unintended changes.
"""

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.solvers.exact import ExactRiemannSolver
from src.core.analysis.errors import compute_l1_error
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme


class TestRegression:
    """Regression test suite."""

    @pytest.fixture
    def reference_solution(self):
        """Generate reference exact solution."""
        config = DamBreakConfig(nx=200, t_end=0.5)
        exact = ExactRiemannSolver(g=config.g)
        x = config.x
        h_exact, u_exact = exact.sample_solution(
            config.h_l, config.u_l, config.h_r, config.u_r,
            x, config.t_end, config.x_dam
        )
        return h_exact, u_exact, config

    def test_upwind_regression(self, reference_solution):
        """Regression test for Upwind scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        # Upwind is first order, expect moderate error
        assert error < 0.15

    def test_lax_friedrichs_regression(self, reference_solution):
        """Regression test for Lax-Friedrichs scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = LaxFriedrichsScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        assert error < 0.15

    def test_lax_wendroff_regression(self, reference_solution):
        """Regression test for Lax-Wendroff scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = LaxWendroffScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        # Second order should be more accurate
        assert error < 0.12

    def test_maccormack_regression(self, reference_solution):
        """Regression test for MacCormack scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = MacCormackScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        assert error < 0.12

    def test_beam_warming_regression(self, reference_solution):
        """Regression test for Beam-Warming scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = BeamWarmingScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        assert error < 0.12

    def test_fromm_regression(self, reference_solution):
        """Regression test for Fromm scheme."""
        h_exact, _, config = reference_solution
        h0, u0 = config.initial_condition()
        scheme = FrommScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        error = compute_l1_error(result.h[-1], h_exact, config.dx)
        assert error < 0.12

    def test_all_schemes_convergence(self):
        """Test that all schemes converge to exact solution."""
        config = DamBreakConfig(nx=100, t_end=0.1)
        exact = ExactRiemannSolver(g=config.g)
        x = config.x
        h_exact, _ = exact.sample_solution(
            config.h_l, config.u_l, config.h_r, config.u_r,
            x, config.t_end, config.x_dam
        )

        schemes = [
            UpwindScheme(),
            LaxFriedrichsScheme(),
            LaxWendroffScheme(),
            MacCormackScheme(),
            BeamWarmingScheme(),
            FrommScheme(),
        ]

        errors = {}
        h0, u0 = config.initial_condition()

        for scheme in schemes:
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            error = compute_l1_error(result.h[-1], h_exact, config.dx)
            errors[scheme.name] = error

        # All schemes should have reasonable error
        for name, error in errors.items():
            assert error < 0.2, f"{name} error too large: {error}"

    def test_mass_conservation_regression(self):
        """Test mass conservation across all schemes."""
        config = DamBreakConfig(nx=100, t_end=0.5)
        h0, u0 = config.initial_condition()
        initial_mass = np.sum(h0)

        schemes = [
            UpwindScheme(),
            LaxFriedrichsScheme(),
            LaxWendroffScheme(),
            MacCormackScheme(),
            BeamWarmingScheme(),
            FrommScheme(),
        ]

        for scheme in schemes:
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            final_mass = np.sum(result.h[-1])
            mass_error = abs(final_mass - initial_mass) / initial_mass

            assert mass_error < 0.1, (
                f"{scheme.name} mass conservation error: {mass_error}"
            )

    def test_positivity_preservation(self):
        """Test that all schemes preserve positivity."""
        config = DamBreakConfig(nx=100, t_end=0.5)
        h0, u0 = config.initial_condition()

        schemes = [
            UpwindScheme(),
            LaxFriedrichsScheme(),
            LaxWendroffScheme(),
            MacCormackScheme(),
            BeamWarmingScheme(),
            FrommScheme(),
        ]

        for scheme in schemes:
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            assert np.all(result.h >= 0), (
                f"{scheme.name} produced negative depths"
            )

    def test_riemann_solver_regression(self):
        """Regression test for exact Riemann solver."""
        solver = ExactRiemannSolver()

        # Test case 1: Symmetric
        state1 = solver.solve(1.0, 0.0, 1.0, 0.0)
        assert state1.h == pytest.approx(1.0, abs=1e-6)
        assert state1.u == pytest.approx(0.0, abs=1e-6)

        # Test case 2: Dam break
        state2 = solver.solve(1.0, 0.0, 0.1, 0.0)
        assert 0.1 < state2.h < 1.0
        assert state2.wave_speeds[0] < 0
        assert state2.wave_speeds[1] > 0

        # Test case 3: With velocity
        state3 = solver.solve(1.0, 1.0, 0.5, -0.5)
        assert state3.h > 0

    def test_hll_solver_regression(self):
        """Regression test for HLL solver."""
        solver = HLLSolver()

        # Test flux computation
        flux = solver.compute_flux(1.0, 0.0, 0.5, 0.0)
        assert len(flux) == 2
        assert flux[0] > 0  # Mass flux should be positive

        # Test with dry bed
        flux_dry = solver.compute_flux(0.0, 0.0, 1.0, 0.0)
        assert len(flux_dry) == 2
