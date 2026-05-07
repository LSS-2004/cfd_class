# Core computation engine
"""
核心计算引擎模块

包含：
- config: 运行参数配置管理
- schemes: 6种有限体积数值格式
- solvers: Riemann求解器与精确解
- analysis: 误差分析与收敛性评估
"""

from src.core.config import DamBreakConfig

__all__ = ["DamBreakConfig"]
