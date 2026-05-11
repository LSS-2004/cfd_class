"""
MUSCL-Hancock格式

二阶TVD格式，使用minmod限制器，高精度且稳定
"""

import numpy as np
from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.riemann_solver import godunov_flux
from src.core.utils import flux


class MUSCLScheme(BaseScheme):
    """
    MUSCL-Hancock格式
    
    格式特点：
    - 二阶精度
    - TVD稳定（使用限制器）
    - 高精度推荐格式
    - 使用minmod限制器防止振荡
    
    算法：
    1. 重构：在界面处构造高阶重构值
    2. 时间推进：使用预测-校正或两步法
    
    重构公式：
    Q_{i+1/2}^L = Q_i + (1/4) * [(1 - k) * ΔQ_{i-1/2} + (1 + k) * ΔQ_{i+1/2}]
    Q_{i+1/2}^R = Q_{i+1} - (1/4) * [(1 + k) * ΔQ_{i+1/2} + (1 - k) * ΔQ_{i+3/2}]
    
    其中 k = 1 为中心差分，k = -1 为迎风格式
    """
    
    name = "MUSCL-Hancock"
    order = 2
    is_tvd = True
    
    def __init__(self, g: float = 9.81):
        super().__init__(g)
        self.limiter = 'minmod'
    
    def _minmod(self, a: float, b: float) -> float:
        """minmod限制器"""
        if a * b <= 0:
            return 0.0
        return np.sign(a) * min(abs(a), abs(b))
    
    def _superbee(self, a: float, b: float) -> float:
        """superbee限制器"""
        return np.sign(a) * max(0, min(2 * abs(a), abs(b)), min(abs(a), 2 * abs(b)))
    
    def _van_leer(self, a: float, b: float) -> float:
        """van Leer限制器"""
        if a * b <= 0:
            return 0.0
        return 2 * a * b / (a + b)
    
    def _limiter(self, r: float) -> float:
        """
        应用限制器
        
        Args:
            r: 梯度比
        
        Returns:
            限制器值
        """
        if self.limiter == 'minmod':
            return self._minmod(1, r)
        elif self.limiter == 'superbee':
            return self._superbee(1, r)
        elif self.limiter == 'van_leer':
            return self._van_leer(1, r)
        else:
            return self._minmod(1, r)
    
    def _reconstruct(self, q: np.ndarray) -> tuple:
        """
        MUSCL重构
        
        Args:
            q: 当前状态向量 (2, nx)
        
        Returns:
            (q_l, q_r): 界面处的左右重构值
        """
        nx = q.shape[1]
        q_l = np.zeros((2, nx + 1))
        q_r = np.zeros((2, nx + 1))
        
        # 计算梯度
        delta_q = np.zeros((2, nx - 1))
        delta_q[:, :] = q[:, 1:] - q[:, :-1]
        
        for i in range(nx + 1):
            for j in range(2):
                if i == 0:
                    # 左边界外推
                    q_l[j, i] = q[j, 0]
                    q_r[j, i] = q[j, 0]
                elif i == nx:
                    # 右边界外推
                    q_l[j, i] = q[j, -1]
                    q_r[j, i] = q[j, -1]
                else:
                    # MUSCL重构
                    if i == 1:
                        # 第一格点
                        delta_left = delta_q[j, 0]
                        delta_right = delta_q[j, 0]
                    elif i == nx - 1:
                        # 最后一格点
                        delta_left = delta_q[j, i - 2]
                        delta_right = delta_q[j, i - 2]
                    else:
                        delta_left = delta_q[j, i - 2]
                        delta_right = delta_q[j, i - 1]
                    
                    # 计算限制器参数
                    eps = 1e-15
                    if abs(delta_right) > eps:
                        r = delta_left / delta_right
                    else:
                        r = 0.0
                    
                    phi = self._limiter(r)
                    
                    q_l[j, i] = q[j, i - 1] + 0.5 * phi * delta_right
                    q_r[j, i] = q[j, i] - 0.5 * phi * delta_right
        
        return q_l, q_r
    
    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算MUSCL-Hancock通量（使用Godunov通量）
        
        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]
        
        Returns:
            数值通量
        """
        return godunov_flux(q_left, q_right, self.g)
    
    def compute_fluxes(self, q: np.ndarray, dx: float) -> np.ndarray:
        """
        计算所有界面的数值通量（重写以实现MUSCL重构）
        
        Args:
            q: 当前状态向量
            dx: 网格间距
        
        Returns:
            通量数组
        """
        nx = q.shape[1]
        F = np.zeros((2, nx + 1))
        
        # MUSCL重构
        q_l, q_r = self._reconstruct(q)
        
        # 计算通量
        for i in range(nx + 1):
            F[:, i] = self.flux(q_l[:, i], q_r[:, i])
        
        return F
