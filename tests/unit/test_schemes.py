"""Unit tests for numerical schemes."""

import numpy as np
import pytest

from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.muscl import MUSCLScheme


class TestUpwindScheme:
    """Test suite for UpwindScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = UpwindScheme()
        assert scheme.name == "First-Order Upwind"
        assert scheme.order == 1
        assert scheme.g == 9.81

    def test_compute_time_step(self):
        """Test time step computation."""
        scheme = UpwindScheme()
        h = np.ones(10)
        u = np.zeros(10)
        dt = scheme.compute_time_step(h, u, 0.9, 0.1)
        assert dt > 0

    def test_advance(self):
        """Test single time step advancement."""
        scheme = UpwindScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert len(u_new) == 10
        assert np.all(h_new > 0)

    def test_run_simulation(self):
        """Test full simulation run."""
        scheme = UpwindScheme()
        h0 = np.ones(50)
        h0[:25] = 2.0
        u0 = np.zeros(50)
        result = scheme.run_simulation(h0, u0, 0.9, 0.1, 0.1)
        assert len(result.t) > 1
        assert result.h.shape[0] == len(result.t)


class TestLaxFriedrichsScheme:
    """Test suite for LaxFriedrichsScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = LaxFriedrichsScheme()
        assert scheme.name == "Lax-Friedrichs"
        assert scheme.order == 1

    def test_advance(self):
        """Test single time step advancement."""
        scheme = LaxFriedrichsScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestLaxWendroffScheme:
    """Test suite for LaxWendroffScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = LaxWendroffScheme()
        assert scheme.name == "Lax-Wendroff"
        assert scheme.order == 2

    def test_advance(self):
        """Test single time step advancement."""
        scheme = LaxWendroffScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestMacCormackScheme:
    """Test suite for MacCormackScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = MacCormackScheme()
        assert scheme.name == "MacCormack"
        assert scheme.order == 2

    def test_advance(self):
        """Test single time step advancement."""
        scheme = MacCormackScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestBeamWarmingScheme:
    """Test suite for BeamWarmingScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = BeamWarmingScheme()
        assert scheme.name == "Beam-Warming"
        assert scheme.order == 2

    def test_advance(self):
        """Test single time step advancement."""
        scheme = BeamWarmingScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestFrommScheme:
    """Test suite for FrommScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = FrommScheme()
        assert scheme.name == "Fromm"
        assert scheme.order == 2

    def test_advance(self):
        """Test single time step advancement."""
        scheme = FrommScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestHLLScheme:
    """Test suite for HLLScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = HLLScheme()
        assert scheme.name == "HLL"
        assert scheme.order == 1

    def test_advance(self):
        """Test single time step advancement."""
        scheme = HLLScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestGodunovScheme:
    """Test suite for GodunovScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = GodunovScheme()
        assert scheme.name == "Godunov"
        assert scheme.order == 1

    def test_advance(self):
        """Test single time step advancement."""
        scheme = GodunovScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)


class TestMUSCLScheme:
    """Test suite for MUSCLScheme."""

    def test_init(self):
        """Test scheme initialization."""
        scheme = MUSCLScheme()
        assert scheme.name == "MUSCL-Hancock"
        assert scheme.order == 2

    def test_advance(self):
        """Test single time step advancement."""
        scheme = MUSCLScheme()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)
        h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
        assert len(h_new) == 10
        assert np.all(h_new > 0)

    def test_limiters(self):
        """Test different slope limiters."""
        for limiter in ["minmod", "superbee", "vanleer"]:
            scheme = MUSCLScheme(limiter=limiter)
            h = np.ones(10)
            h[:5] = 2.0
            u = np.zeros(10)
            h_new, u_new = scheme.advance(h, u, 0.01, 0.1)
            assert len(h_new) == 10
            assert np.all(h_new > 0)


class TestAllSchemes:
    """Tests applicable to all schemes."""

    @pytest.fixture
    def schemes(self):
        """Return list of all schemes."""
        return [
            UpwindScheme(),
            LaxFriedrichsScheme(),
            HLLScheme(),
            LaxWendroffScheme(),
            MacCormackScheme(),
            BeamWarmingScheme(),
            FrommScheme(),
            GodunovScheme(),
            MUSCLScheme(),
        ]

    def test_mass_conservation(self, schemes):
        """Test approximate mass conservation."""
        for scheme in schemes:
            h0 = np.ones(50)
            h0[:25] = 2.0
            u0 = np.zeros(50)
            result = scheme.run_simulation(h0, u0, 0.9, 0.1, 0.1)
            initial_mass = np.sum(result.h[0])
            final_mass = np.sum(result.h[-1])
            # Allow small conservation error
            assert abs(final_mass - initial_mass) / initial_mass < 0.1

    def test_positivity(self, schemes):
        """Test water depth remains positive."""
        for scheme in schemes:
            h0 = np.ones(50)
            h0[:25] = 2.0
            u0 = np.zeros(50)
            result = scheme.run_simulation(h0, u0, 0.9, 0.1, 0.1)
            assert np.all(result.h >= 0)

    def test_small_grid(self, schemes):
        """Test with minimum grid size."""
        for scheme in schemes:
            h0 = np.ones(2)
            h0[0] = 2.0
            u0 = np.zeros(2)
            result = scheme.run_simulation(h0, u0, 0.5, 0.5, 0.01)
            assert len(result.t) > 1
            assert np.all(result.h >= 0)

    def test_zero_velocity(self, schemes):
        """Test with zero initial velocity."""
        for scheme in schemes:
            h0 = np.ones(20)
            h0[:10] = 2.0
            u0 = np.zeros(20)
            result = scheme.run_simulation(h0, u0, 0.9, 0.1, 0.05)
            assert np.all(result.h >= 0)
            assert len(result.t) > 1
