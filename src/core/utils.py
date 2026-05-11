"""
工具函数模块

提供通用的辅助函数
"""

import numpy as np


def flux(q: np.ndarray, g: float = 9.81) -> np.ndarray:
    """
    计算浅水方程的通量向量
    
    Args:
        q: 状态向量 [h, h*u]^T，形状为 (2, nx)
        g: 重力加速度
    
    Returns:
        通量向量 F(q) = [h*u, h*u² + 0.5*g*h²]^T
    """
    h = q[0, :]
    hu = q[1, :]
    u = hu / np.where(h > 0, h, 1)
    
    F = np.zeros_like(q)
    F[0, :] = hu
    F[1, :] = hu * u + 0.5 * g * h * h
    
    return F


def roe_average(q_left: np.ndarray, q_right: np.ndarray, g: float = 9.81) -> tuple:
    """
    计算Roe平均状态
    
    Args:
        q_left: 左侧状态
        q_right: 右侧状态
        g: 重力加速度
    
    Returns:
        (h_avg, u_avg, c_avg): 平均水深、平均速度、平均声速
    """
    h_left, hu_left = q_left[0], q_left[1]
    h_right, hu_right = q_right[0], q_right[1]
    
    u_left = hu_left / h_left if h_left > 0 else 0.0
    u_right = hu_right / h_right if h_right > 0 else 0.0
    
    sqrt_h_left = np.sqrt(h_left) if h_left > 0 else 0.0
    sqrt_h_right = np.sqrt(h_right) if h_right > 0 else 0.0
    
    h_avg = (sqrt_h_left * h_right + sqrt_h_right * h_left) / (sqrt_h_left + sqrt_h_right) if (sqrt_h_left + sqrt_h_right) > 0 else 0.0
    u_avg = (sqrt_h_left * u_left + sqrt_h_right * u_right) / (sqrt_h_left + sqrt_h_right) if (sqrt_h_left + sqrt_h_right) > 0 else 0.0
    c_avg = np.sqrt(g * h_avg) if h_avg > 0 else 0.0
    
    return h_avg, u_avg, c_avg


def compute_max_speed(q: np.ndarray, g: float = 9.81) -> float:
    """
    计算最大波速（用于CFL条件）
    
    Args:
        q: 状态向量 [h, h*u]^T
        g: 重力加速度
    
    Returns:
        最大特征速度
    """
    h = q[0, :]
    hu = q[1, :]
    u = hu / np.where(h > 0, h, 1)
    c = np.sqrt(g * np.maximum(h, 0))
    
    return np.max(np.abs(u) + c)


def apply_boundary_conditions(q: np.ndarray, boundary_type: str) -> np.ndarray:
    """
    应用边界条件
    
    Args:
        q: 状态向量
        boundary_type: 边界条件类型 ('transmissive', 'reflective', 'periodic')
    
    Returns:
        应用边界条件后的状态向量
    """
    nx = q.shape[1]
    
    if boundary_type == 'transmissive':
        # 透射边界（外推）
        q[:, 0] = q[:, 1]
        q[:, -1] = q[:, -2]
    
    elif boundary_type == 'reflective':
        # 反射边界
        # 左边界：u -> -u
        q[1, 0] = -q[1, 0]
        # 右边界：u -> -u
        q[1, -1] = -q[1, -1]
    
    elif boundary_type == 'periodic':
        # 周期边界
        q[:, 0] = q[:, -2]
        q[:, -1] = q[:, 1]
    
    return q


def positivity_fix(q: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """
    正性保持修正，防止出现负水深
    
    Args:
        q: 状态向量
        eps: 最小水深阈值
    
    Returns:
        修正后的状态向量
    """
    h = q[0, :]
    mask = h < eps
    q[0, mask] = eps
    q[1, mask] = 0.0  # 干底区域速度为0
    
    return q
