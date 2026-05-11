"""
Lax-Wendroff格式

二阶中心格式，在光滑区域精度较高，但不满足TVD条件
"""

import numpy as np
from src.core.schemes.base_scheme import BaseScheme
from src.core.utils import flux


class LaxWendroffScheme(BaseScheme):
    """
    Lax-Wendroff格式
    
    格式特点：
    - 二阶精度
    - 非TVD（在激波附近可能产生振荡）
    - 适合光滑解测试
    
    通量公式：
    F_{i+1/2} = 0.5 * [F(Q_i) + F(Q_{i+1})] - 0.5 * (dt/dx) * [A_{i+1}F(Q_{i+1}) - A_iF(Q_i)]
    其中 A = dF/dQ 是雅可比矩阵
    """
    
    name = "Lax-Wendroff"
    order = 2
    is_tvd = False
    
    def __init__(self, g: float = 9.81):
        super().__init__(g)
        self._dt = None
        self._dx = None
    
    def set_time_step(self, dt: float, dx: float):
        """设置时间步长和网格间距"""
        self._dt = dt
        self._dx = dx
    
    def _jacobian(self, q: np.ndarray) -> np.ndarray:
        """
        计算通量雅可比矩阵
        
        Args:
            q: 状态向量 [h, hu]
        
        Returns:
            雅可比矩阵 A = dF/dQ
        """
        h, hu = q[0], q[1]
        u = hu / h if h > 0 else 0.0
        c = np.sqrt(self.g * h) if h > 0 else 0.0
        
        A = np.array([
            [0, 1],
            [u**2 - c**2, 2 * u]
        ])
        
        return A
    
    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算Lax-Wendroff数值通量
        
        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]
        
        Returns:
            数值通量
        """
        f_l = flux(q_left, self.g)
        f_r = flux(q_right, self.g)
        
        A_l = self._jacobian(q_left)
        A_r = self._jacobian(q_right)
        
        if self._dt is not None and self._dx is not None:
            theta = self._dt / self._dx
            F = 0.5 * (f_l + f_r) - 0.5 * theta * (A_r @ f_r - A_l @ f_l)
        else:
            # 退化为中心差分
            F = 0.5 * (f_l + f_r)
        
        return F
    
    def compute_fluxes(self, q: np.ndarray, dx: float) -> np.ndarray:
        """
        计算所有界面的数值通量（重写以传递时间步长）
        
        Args:
            q: 当前状态向量
            dx: 网格间距
        
        Returns:
            通量数组
        """
        # 估算时间步长用于Lax-Wendroff
        from src.core.utils import compute_max_speed
        max_speed = compute_max_speed(q, self.g)
        self._dt = 0.9 * dx / max_speed
        self._dx = dx
        
        return super().compute_fluxes(q, dx)
