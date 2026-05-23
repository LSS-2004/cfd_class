"""
有限体积数值格式包

Supported schemes:
- First-Order Upwind: Robust but diffusive
- Lax-Friedrichs: Centered diffusion
- HLL: Approximate Riemann solver
- Lax-Wendroff: Second-order predictor-corrector
- MacCormack: NASA predictor-corrector
- Beam-Warming: One-sided backward difference
- Fromm: Averaged scheme
- Godunov: Exact Riemann solver
- MUSCL-Hancock: TVD high-resolution
"""

from src.core.schemes.base_scheme import BaseScheme, SimulationResult
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.muscl import MUSCLScheme

__all__ = [
    "BaseScheme",
    "SimulationResult",
    "UpwindScheme",
    "LaxFriedrichsScheme",
    "HLLScheme",
    "LaxWendroffScheme",
    "MacCormackScheme",
    "BeamWarmingScheme",
    "FrommScheme",
    "GodunovScheme",
    "MUSCLScheme",
    "get_scheme",
    "get_all_schemes",
]

_SCHEME_REGISTRY = {
    "Upwind": UpwindScheme,
    "Lax-Friedrichs": LaxFriedrichsScheme,
    "HLL": HLLScheme,
    "Lax-Wendroff": LaxWendroffScheme,
    "MacCormack": MacCormackScheme,
    "Beam-Warming": BeamWarmingScheme,
    "Fromm": FrommScheme,
    "Godunov": GodunovScheme,
    "MUSCL-Hancock": MUSCLScheme,
}


def get_scheme(name: str) -> BaseScheme:
    """Get a scheme instance by name.

    Args:
        name: Scheme name

    Returns:
        Scheme instance

    Raises:
        ValueError: If scheme name is not recognized
    """
    if name not in _SCHEME_REGISTRY:
        raise ValueError(f"Unknown scheme: {name}. Available schemes: {list(_SCHEME_REGISTRY.keys())}")
    return _SCHEME_REGISTRY[name]()


def get_all_schemes() -> list:
    """Get list of all available scheme names.

    Returns:
        List of scheme names
    """
    return list(_SCHEME_REGISTRY.keys())
