"""
MacCormack格式

二阶预测-校正格式，高效且易于实现
"""

import numpy as np
from src.core.schemes.base_scheme import BaseScheme
from src.core.utils import flux, apply_boundary_conditions


class MacCormackScheme(BaseScheme):
    """
    MacCormack格式
    
    格式特点：
    - 二阶精度
    - 非TVD
    - 高效的预测-校正方法
    
    算法：
    预测步: Q* = Q_i - (dt/dx) * (F_{i+1} - F_i)
    校正步: Q^{n+1} = 0.5 * (Q_i + Q*) - 0.5 * (dt/dx) * (F*_i - F*_{i-1})
    """
    
    name = "MacCormack"
    order = 2
    is_tvd = False
    
    def evolve(self, config, progress_callback=None):
        """
        时间演化主函数（重写以实现预测-校正）
        
        Args:
            config: 溃坝问题配置
            progress_callback: 进度回调函数
        
        Returns:
            快照字典
        """
        q = config.q_initial.copy()
        dx = config.dx
        cfl = config.cfl
        t_end = config.t_end
        
        t = 0.0
        snapshots = {t: q.copy()}
        
        while t < t_end:
            # 计算时间步长
            from src.core.utils import compute_max_speed
            max_speed = compute_max_speed(q, self.g)
            dt = min(cfl * dx / max_speed, t_end - t)
            
            if dt <= 0:
                break
            
            # 预测步（前向差分）
            F = flux(q, self.g)
            q_pred = q - (dt / dx) * (F[:, 1:] - F[:, :-1])
            
            # 应用边界条件
            q_pred = apply_boundary_conditions(q_pred.copy(), config.boundary_type)
            
            # 校正步（后向差分）
            F_pred = flux(q_pred, self.g)
            q_new = 0.5 * (q[:, 1:-1] + q_pred[:, 1:-1]) - 0.5 * (dt / dx) * (F_pred[:, 1:-1] - F_pred[:, :-2])
            
            # 边界外推
            q_full = np.zeros_like(q)
            q_full[:, 1:-1] = q_new
            q_full[:, 0] = q_full[:, 1]
            q_full[:, -1] = q_full[:, -2]
            
            # 正性保持
            q_full = self._positivity_fix(q_full)
            
            q = q_full
            t += dt
            
            # 记录快照
            if int(t / dt) % 10 == 0:
                snapshots[t] = q.copy()
            
            if progress_callback is not None:
                progress_callback(t / t_end)
        
        if t not in snapshots:
            snapshots[t] = q.copy()
        
        return snapshots
    
    def _positivity_fix(self, q: np.ndarray, eps: float = 1e-12) -> np.ndarray:
        """正性保持修正"""
        h = q[0, :]
        mask = h < eps
        q[0, mask] = eps
        q[1, mask] = 0.0
        return q
    
    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """MacCormack使用标准通量（实际在evolve中实现）"""
        return flux(q_left, self.g)
