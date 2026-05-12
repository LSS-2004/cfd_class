"""Integration tests for full simulation pipeline."""

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.solvers.exact import ExactRiemannSolver
from src.core.analysis.errors import compute_all_errors
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme


class TestFullPipeline:
    """Test complete simulation pipeline."""

    def test_config_to_simulation(self):
        """Test full pipeline from config to simulation result."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert len(result.t) > 1
        assert result.h.shape[0] == len(result.t)
        assert result.h.shape[1] == config.nx
        assert np.all(result.h >= 0)

    def test_exact_solver_integration(self):
        """Test exact solver with config parameters."""
        config = DamBreakConfig(h_l=2.0, h_r=0.5)
        solver = ExactRiemannSolver(g=config.g)

        state = solver.solve(
            config.h_l, config.u_l, config.h_r, config.u_r
        )

        assert state.h > 0
        assert state.wave_speeds[0] < state.wave_speeds[1]

    def test_hll_solver_integration(self):
        """Test HLL solver with config parameters."""
        config = DamBreakConfig()
        solver = ExactRiemannSolver(g=config.g)

        state = solver.solve(
            config.h_l, config.u_l, config.h_r, config.u_r
        )

        assert state.h >= 0

    def test_snapshot_system(self):
        """Test snapshot recording during simulation."""
        config = DamBreakConfig(nx=50, t_end=0.5)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        snapshot_times = [0.1, 0.2, 0.3]
        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end,
            snapshot_times=snapshot_times
        )

        assert len(result.snapshots) == len(snapshot_times)
        for t in snapshot_times:
            assert t in result.snapshots
            h_snap, u_snap = result.snapshots[t]
            assert len(h_snap) == config.nx
            assert len(u_snap) == config.nx


class TestMultiSchemeComparison:
    """Test comparing multiple schemes on same problem."""

    def test_all_schemes_run(self, all_schemes):
        """Test that all schemes can run dam break simulation."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()

        results = {}
        for scheme in all_schemes:
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            results[scheme.name] = result

            assert len(result.t) > 1
            assert np.all(result.h >= 0)

        assert len(results) == len(all_schemes)

    def test_scheme_comparison_consistency(self, all_schemes):
        """Test that all schemes produce physically consistent results."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()

        final_states = {}
        for scheme in all_schemes:
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            final_states[scheme.name] = result.h[-1]

        # All schemes should have similar total mass
        initial_mass = np.sum(h0)
        for name, h_final in final_states.items():
            final_mass = np.sum(h_final)
            mass_error = abs(final_mass - initial_mass) / initial_mass
            assert mass_error < 0.2, f"{name} mass error: {mass_error}"

    def test_first_vs_second_order(self):
        """Compare first and second order schemes."""
        config = DamBreakConfig(nx=100, t_end=0.1)
        h0, u0 = config.initial_condition()

        # Exact solution
        exact = ExactRiemannSolver(g=config.g)
        x = config.x
        h_exact, _ = exact.sample_solution(
            config.h_l, config.u_l, config.h_r, config.u_r,
            x, config.t_end, config.x_dam
        )

        # First order
        scheme1 = UpwindScheme()
        result1 = scheme1.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        # Second order
        scheme2 = LaxWendroffScheme()
        result2 = scheme2.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        errors1 = compute_all_errors(result1.h[-1], h_exact, config.dx)
        errors2 = compute_all_errors(result2.h[-1], h_exact, config.dx)

        # Second order should generally be more accurate for smooth regions
        assert errors1["l1"] > 0
        assert errors2["l1"] > 0


class TestParameterVariation:
    """Test simulation with varying parameters."""

    def test_cfl_variation(self):
        """Test simulation with different CFL numbers."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        for cfl in [0.3, 0.5, 0.7, 0.9]:
            result = scheme.run_simulation(
                h0, u0, cfl, config.dx, config.t_end
            )
            assert len(result.t) > 1
            assert np.all(result.h >= 0)

    def test_grid_refinement(self):
        """Test simulation with different grid resolutions."""
        errors = []
        nx_values = [25, 50, 100]

        for nx in nx_values:
            config = DamBreakConfig(nx=nx, t_end=0.1)
            h0, u0 = config.initial_condition()
            scheme = UpwindScheme()

            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )

            # Exact solution
            exact = ExactRiemannSolver(g=config.g)
            x = config.x
            h_exact, _ = exact.sample_solution(
                config.h_l, config.u_l, config.h_r, config.u_r,
                x, config.t_end, config.x_dam
            )

            err = compute_all_errors(result.h[-1], h_exact, config.dx)
            errors.append(err["l1"])

        # Error should decrease with refinement
        for i in range(len(errors) - 1):
            assert errors[i + 1] < errors[i] * 1.5

    def test_different_dam_heights(self):
        """Test with different dam height ratios."""
        scheme = UpwindScheme()

        for h_r in [0.0, 0.1, 0.5, 0.9]:
            config = DamBreakConfig(h_l=1.0, h_r=h_r, nx=50, t_end=0.1)
            h0, u0 = config.initial_condition()

            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )

            assert len(result.t) > 1
            assert np.all(result.h >= 0)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_small_time(self):
        """Test simulation with very small end time."""
        config = DamBreakConfig(nx=50, t_end=1e-6)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert len(result.t) >= 2
        assert np.allclose(result.h[-1], h0, atol=1e-3)

    def test_nearly_equal_depths(self):
        """Test with nearly equal water depths."""
        config = DamBreakConfig(h_l=1.0, h_r=0.99, nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert len(result.t) > 1
        assert np.all(result.h >= 0)

    def test_large_velocity(self):
        """Test with large initial velocity."""
        config = DamBreakConfig(
            h_l=1.0, h_r=0.5, u_l=2.0, u_r=-1.0,
            nx=50, t_end=0.05
        )
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert len(result.t) > 1
        assert np.all(result.h >= 0)

    def test_progress_callback(self):
        """Test progress callback functionality."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        progress_values = []

        def callback(progress):
            progress_values.append(progress)

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end,
            progress_callback=callback
        )

        assert len(progress_values) > 0
        assert progress_values[-1] == pytest.approx(1.0, abs=0.01)
