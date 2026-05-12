"""
分析工具包

Features:
- Error metrics (L1, L2, L-infinity norms)
- Convergence order estimation
"""

from src.core.analysis.errors import compute_error, estimate_order

__all__ = ["compute_error", "estimate_order"]
