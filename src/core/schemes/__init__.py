"""
有限体积数值格式包

Supported schemes:
- First-Order Upwind: Robust but diffusive
- Lax-Friedrichs: Centered diffusion
- Lax-Wendroff: Second-order predictor-corrector
- MacCormack: NASA predictor-corrector
- Beam-Warming: One-sided backward difference
- Fromm: Averaged scheme
"""

from src.core.schemes.base_scheme import BaseScheme, SimulationResult
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme

__all__ = [
    "BaseScheme",
    "SimulationResult",
    "UpwindScheme",
    "LaxFriedrichsScheme",
    "LaxWendroffScheme",
    "MacCormackScheme",
    "BeamWarmingScheme",
    "FrommScheme",
]
