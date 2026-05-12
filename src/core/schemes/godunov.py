"""
Godunov格式

使用精确Riemann求解器的一阶+格式，精确捕捉激波
"""

import numpy as np

from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.riemann_solver import godunov_flux


class GodunovScheme(BaseScheme):
    """
    Godunov格式

    格式特点：
    - 一阶+精度
    - TVD稳定
    - 使用精确Riemann求解器
    - 激波捕捉精确

    通量公式：
    F_{i+1/2} = F(Q(R(Q_i, Q_{i+1})))
    其中 R(Q_i, Q_{i+1}) 是Riemann问题的解
    """

    name = "Godunov"
    order = 1
    is_tvd = True

    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算Godunov数值通量（使用精确Riemann求解器）

        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]

        Returns:
            数值通量
        """
        return godunov_flux(q_left, q_right, self.g)
