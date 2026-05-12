"""
HLL格式

Harten-Lax-van Leer近似Riemann求解器格式
"""

import numpy as np

from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.riemann_solver import hll_flux


class HLLScheme(BaseScheme):
    """
    HLL格式

    格式特点：
    - 一阶+精度
    - TVD稳定（近似）
    - 使用HLL近似Riemann求解器
    - 工程实用，计算效率高

    通量公式：
    F_{i+1/2} = (S_r * F(Q_i) - S_l * F(Q_{i+1}) + S_l * S_r * (Q_{i+1} - Q_i)) / (S_r - S_l)
    其中 S_l 和 S_r 是估计的左右波速
    """

    name = "HLL"
    order = 1
    is_tvd = True

    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算HLL数值通量

        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]

        Returns:
            数值通量
        """
        return hll_flux(q_left, q_right, self.g)
