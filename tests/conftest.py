"""Pytest configuration and shared fixtures."""

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.solvers.exact import ExactRiemannSolver
from src.core.solvers.hll import HLLSolver
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme


@pytest.fixture
def default_config():
    """Return default DamBreakConfig."""
    return DamBreakConfig()


@pytest.fixture
def dam_break_config():
    """Return dam break configuration."""
    return DamBreakConfig(
        h_l=1.0,
        h_r=0.1,
        u_l=0.0,
        u_r=0.0,
        nx=100,
        t_end=0.5,
    )


@pytest.fixture
def exact_solver():
    """Return ExactRiemannSolver instance."""
    return ExactRiemannSolver()


@pytest.fixture
def hll_solver():
    """Return HLLSolver instance."""
    return HLLSolver()


@pytest.fixture
def all_schemes():
    """Return list of all numerical schemes."""
    return [
        UpwindScheme(),
        LaxFriedrichsScheme(),
        LaxWendroffScheme(),
        MacCormackScheme(),
        BeamWarmingScheme(),
        FrommScheme(),
    ]


@pytest.fixture
def first_order_schemes():
    """Return list of first-order schemes."""
    return [
        UpwindScheme(),
        LaxFriedrichsScheme(),
    ]


@pytest.fixture
def second_order_schemes():
    """Return list of second-order schemes."""
    return [
        LaxWendroffScheme(),
        MacCormackScheme(),
        BeamWarmingScheme(),
        FrommScheme(),
    ]


@pytest.fixture
def dam_break_initial_condition():
    """Return initial condition for dam break problem."""
    config = DamBreakConfig(h_l=1.0, h_r=0.1, nx=100)
    return config.initial_condition()


@pytest.fixture
def smooth_initial_condition():
    """Return smooth initial condition."""
    nx = 100
    x = np.linspace(-1, 1, nx)
    h = 1.0 + 0.1 * np.sin(np.pi * x)
    u = np.zeros(nx)
    return h.astype(np.float64), u.astype(np.float64)
