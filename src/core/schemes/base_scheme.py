"""
数值格式基类

定义所有FVM格式的公共接口和功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Callable, Optional
import numpy as np
from src.core.config import DamBreakConfig
from src.core.utils import compute_max_speed, apply_boundary_conditions, positivity_fix


class BaseScheme(ABC):
    """
    有限体积法数值格式基类
    
    所有具体格式都必须实现 flux 方法
    """
    
    name: str = "BaseScheme"
    order: int = 1
    is_tvd: bool = False
    
    def __init__(self, g: float = 9.81):
        """
        初始化数值格式
        
        Args:
            g: 重力加速度
        """
        self.g = g
    
    @abstractmethod
    def flux(self, q_left: np.ndarray, q_right: np.ndarray) -> np.ndarray:
        """
        计算数值通量
        
        Args:
            q_left: 左侧状态 [h, hu]
            q_right: 右侧状态 [h, hu]
        
        Returns:
            数值通量
        """
        pass
    
    def evolve(self, config: DamBreakConfig, 
               progress_callback: Optional[Callable[[float], None]] = None) -> Dict[float, np.ndarray]:
        """
        时间演化主函数
        
        Args:
            config: 溃坝问题配置
            progress_callback: 进度回调函数
        
        Returns:
            快照字典 {时间: 状态向量}
        """
        q = config.q_initial.copy()
        dx = config.dx
        cfl = config.cfl
        t_end = config.t_end
        
        t = 0.0
        snapshots = {t: q.copy()}
        
        if config.snapshot_times is not None:
            snapshot_times = sorted(set([0.0, t_end] + config.snapshot_times))
            next_snapshot_idx = 1
        else:
            snapshot_times = None
        
        while t < t_end:
            # 计算时间步长
            max_speed = compute_max_speed(q, self.g)
            dt = min(cfl * dx / max_speed, t_end - t)
            
            if dt <= 0:
                break
            
            # 计算通量
            F = self.compute_fluxes(q, dx)
            
            # 更新状态
            q_new = q - (dt / dx) * (F[:, 1:] - F[:, :-1])
            
            # 应用边界条件
            q_new = apply_boundary_conditions(q_new, config.boundary_type)
            
            # 正性保持
            q_new = positivity_fix(q_new)
            
            q = q_new
            t += dt
            
            # 记录快照
            if snapshot_times is not None and next_snapshot_idx < len(snapshot_times):
                while next_snapshot_idx < len(snapshot_times) and t >= snapshot_times[next_snapshot_idx]:
                    snapshots[snapshot_times[next_snapshot_idx]] = q.copy()
                    next_snapshot_idx += 1
            else:
                # 每10步记录一次
                if int(t / dt) % 10 == 0:
                    snapshots[t] = q.copy()
            
            # 进度回调
            if progress_callback is not None:
                progress_callback(t / t_end)
        
        # 确保记录最终时刻
        if t not in snapshots:
            snapshots[t] = q.copy()
        
        return snapshots
    
    def compute_fluxes(self, q: np.ndarray, dx: float) -> np.ndarray:
        """
        计算所有界面的数值通量
        
        Args:
            q: 当前状态向量
            dx: 网格间距
        
        Returns:
            通量数组，形状为 (2, nx+1)
        """
        nx = q.shape[1]
        F = np.zeros((2, nx + 1))
        
        # 边界外推
        q_extended = np.zeros((2, nx + 2))
        q_extended[:, 1:-1] = q
        q_extended[:, 0] = q[:, 0]
        q_extended[:, -1] = q[:, -1]
        
        # 计算内部通量
        for i in range(nx + 1):
            q_left = q_extended[:, i]
            q_right = q_extended[:, i + 1]
            F[:, i] = self.flux(q_left, q_right)
        
        return F


def get_scheme(name: str) -> BaseScheme:
    """
    根据名称获取数值格式实例
    
    Args:
        name: 格式名称
    
    Returns:
        数值格式实例
    """
    from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
    from src.core.schemes.lax_wendroff import LaxWendroffScheme
    from src.core.schemes.maccormack import MacCormackScheme
    from src.core.schemes.godunov import GodunovScheme
    from src.core.schemes.hll import HLLScheme
    from src.core.schemes.muscl import MUSCLScheme
    
    schemes = {
        "Lax-Friedrichs": LaxFriedrichsScheme,
        "Lax-Wendroff": LaxWendroffScheme,
        "MacCormack": MacCormackScheme,
        "Godunov": GodunovScheme,
        "HLL": HLLScheme,
        "MUSCL-Hancock": MUSCLScheme
    }
    
    if name not in schemes:
        raise ValueError(f"未知的数值格式: {name}")
    
    return schemes[name]()


def get_all_schemes() -> list:
    """获取所有可用格式列表"""
    return [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Godunov",
        "HLL",
        "MUSCL-Hancock"
    ]
