"""
核心计算引擎模块

包含：
- 配置管理 (config)
- 数值格式 (schemes)
- Riemann求解器 (solvers)
- 分析工具 (analysis)
- 工具函数 (utils)
"""

from src.core.config import DamBreakConfig
from src.core.utils import flux, roe_average, compute_max_speed, apply_boundary_conditions, positivity_fix

__all__ = [
    "DamBreakConfig",
    "flux",
    "roe_average",
    "compute_max_speed",
    "apply_boundary_conditions",
    "positivity_fix"
]
