"""
Lax-Friedrichs格式

一阶稳定格式，具有强稳定性，作为基准对比格式
"""

import numpy as np

from src.core.schemes.base_scheme import BaseScheme
from src.core.utils import flux


class LaxFriedrichsScheme(BaseScheme):
    """
    Lax-Friedrichs格式

    格式特点：
    - 一阶精度
    - TVD稳定
    - 数值耗散较大
    - 适合作为基准对比

    通量公式：
    F_{i+1/2} = 0.5 * [F(Q_i) + F(Q_{i+1})] - 0.5 * alpha * (Q_{i+1} - Q_i)
    其中 alpha = max|特征速度|
    """

    name = "Lax-Friedrichs"
    order = 1
    is_tvd = True

    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算Lax-Friedrichs数值通量

        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]

        Returns:
            数值通量
        """
        h_l, hu_l = q_left[0], q_left[1]
        h_r, hu_r = q_right[0], q_right[1]

        u_l = hu_l / h_l if h_l > 0 else 0.0
        u_r = hu_r / h_r if h_r > 0 else 0.0

        # 计算左右通量
        f_l = flux(q_left, self.g)
        f_r = flux(q_right, self.g)

        # 计算最大特征速度
        c_l = np.sqrt(self.g * np.maximum(h_l, 0))
        c_r = np.sqrt(self.g * np.maximum(h_r, 0))
        alpha = max(np.abs(u_l) + c_l, np.abs(u_r) + c_r)

        # Lax-Friedrichs通量
        F = 0.5 * (f_l + f_r) - 0.5 * alpha * (q_right - q_left)

        return F
