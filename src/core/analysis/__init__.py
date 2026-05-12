"""
分析工具包

功能：
- 误差度量（L1, L2, L∞范数）
- 收敛阶估计
"""

from src.core.analysis.error_analysis import (
    compute_l1_error,
    compute_l2_error,
    compute_linf_error,
    compute_mass_conservation,
    estimate_convergence_order,
)

__all__ = [
    "compute_l1_error",
    "compute_l2_error",
    "compute_linf_error",
    "estimate_convergence_order",
    "compute_mass_conservation",
]
