"""
配置管理模块

定义溃坝问题的配置参数和初始化状态
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np


@dataclass(frozen=True)
class DamBreakConfig:
    """
    溃坝问题配置类

    参数说明:
        domain_length: 计算域长度 [m]
        nx: 网格单元数量
        x_dam: 大坝位置 [m]，默认为域中心
        h_l: 左侧初始水深 [m]
        h_r: 右侧初始水深 [m]
        u_l: 左侧初始流速 [m/s]
        u_r: 右侧初始流速 [m/s]
        g: 重力加速度 [m/s²]，默认9.81
        t_end: 终止时间 [s]
        cfl: CFL稳定性数
        boundary_type: 边界条件类型 ('transmissive', 'reflective', 'periodic')
        snapshot_times: 快照时间点列表（可选）
        progress_callback: 进度回调函数（可选）
    """

    domain_length: float = 1000.0
    nx: int = 200
    _x_dam: Optional[float] = None
    h_l: float = 10.0
    h_r: float = 1.0
    u_l: float = 0.0
    u_r: float = 0.0
    g: float = 9.81
    t_end: float = 50.0
    cfl: float = 0.9
    boundary_type: str = "transmissive"
    snapshot_times: Optional[list] = None
    progress_callback: Optional[Callable[[float], None]] = None

    @property
    def x_dam(self) -> float:
        """大坝位置，默认为域中心"""
        if self._x_dam is None:
            return self.domain_length / 2
        return self._x_dam

    @property
    def dx(self) -> float:
        """网格间距"""
        return self.domain_length / self.nx

    @property
    def x(self) -> np.ndarray:
        """空间坐标数组（单元中心）"""
        return np.linspace(self.dx / 2, self.domain_length - self.dx / 2, self.nx)

    @property
    def q_initial(self) -> np.ndarray:
        """初始状态向量 [h, h*u]^T"""
        h = np.where(self.x < self.x_dam, self.h_l, self.h_r)
        u = np.where(self.x < self.x_dam, self.u_l, self.u_r)
        q = np.zeros((2, self.nx))
        q[0, :] = h
        q[1, :] = h * u
        return q

    @property
    def dry_tolerance(self) -> float:
        """干底判断阈值"""
        return 1e-12

    def is_dry(self, h: float) -> bool:
        """判断是否为干底"""
        return h < self.dry_tolerance

    def validate(self) -> bool:
        """验证配置参数有效性"""
        if self.domain_length <= 0:
            raise ValueError("域长度必须大于0")
        if self.nx <= 0:
            raise ValueError("网格数量必须大于0")
        if self.h_l <= 0:
            raise ValueError("左侧水深必须大于0")
        if self.h_r < 0:
            raise ValueError("右侧水深不能为负")
        if self.cfl <= 0 or self.cfl >= 1:
            raise ValueError("CFL数必须在(0, 1)范围内")
        if self.t_end <= 0:
            raise ValueError("终止时间必须大于0")
        return True
