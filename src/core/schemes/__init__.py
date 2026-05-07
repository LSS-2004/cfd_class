# Numerical schemes package
"""
有限体积数值格式包

支持的格式：
- Lax-Friedrichs: 一阶稳定格式
- Lax-Wendroff: 二阶中心格式
- MacCormack: 二阶预测-校正格式
- Godunov: 精确Riemann求解器格式
- HLL: 近似Riemann求解器格式
- MUSCL-Hancock: 二阶TVD格式
"""

from src.core.schemes.base_scheme import BaseScheme

__all__ = ["BaseScheme"]
