"""
误差分析工具模块

提供误差度量和收敛阶估计功能
"""

import numpy as np
from scipy import stats
from typing import Dict, Tuple


def compute_l1_error(numerical: np.ndarray, exact: np.ndarray, dx: float = 1.0) -> float:
    """
    计算L1误差范数
    
    L1 = ∫|u_num - u_exact| dx / ∫|u_exact| dx
    
    Args:
        numerical: 数值解
        exact: 精确解
        dx: 网格间距（用于积分）
    
    Returns:
        L1相对误差
    """
    if exact.size == 0 or numerical.size == 0:
        return np.nan
    
    # 确保数组形状匹配
    numerical = np.asarray(numerical).flatten()
    exact = np.asarray(exact).flatten()
    
    if len(numerical) != len(exact):
        # 插值到相同网格
        exact = np.interp(
            np.linspace(0, 1, len(numerical)),
            np.linspace(0, 1, len(exact)),
            exact
        )
    
    error = np.sum(np.abs(numerical - exact)) * dx
    norm = np.sum(np.abs(exact)) * dx
    
    if norm < 1e-15:
        return np.nan
    
    return error / norm


def compute_l2_error(numerical: np.ndarray, exact: np.ndarray, dx: float = 1.0) -> float:
    """
    计算L2误差范数
    
    L2 = sqrt(∫(u_num - u_exact)^2 dx / ∫u_exact^2 dx)
    
    Args:
        numerical: 数值解
        exact: 精确解
        dx: 网格间距（用于积分）
    
    Returns:
        L2相对误差
    """
    if exact.size == 0 or numerical.size == 0:
        return np.nan
    
    numerical = np.asarray(numerical).flatten()
    exact = np.asarray(exact).flatten()
    
    if len(numerical) != len(exact):
        exact = np.interp(
            np.linspace(0, 1, len(numerical)),
            np.linspace(0, 1, len(exact)),
            exact
        )
    
    error = np.sqrt(np.sum((numerical - exact)**2) * dx)
    norm = np.sqrt(np.sum(exact**2) * dx)
    
    if norm < 1e-15:
        return np.nan
    
    return error / norm


def compute_linf_error(numerical: np.ndarray, exact: np.ndarray) -> float:
    """
    计算L∞误差范数
    
    L∞ = max|u_num - u_exact| / max|u_exact|
    
    Args:
        numerical: 数值解
        exact: 精确解
    
    Returns:
        L∞相对误差
    """
    if exact.size == 0 or numerical.size == 0:
        return np.nan
    
    numerical = np.asarray(numerical).flatten()
    exact = np.asarray(exact).flatten()
    
    if len(numerical) != len(exact):
        exact = np.interp(
            np.linspace(0, 1, len(numerical)),
            np.linspace(0, 1, len(exact)),
            exact
        )
    
    error = np.max(np.abs(numerical - exact))
    norm = np.max(np.abs(exact))
    
    if norm < 1e-15:
        return np.nan
    
    return error / norm


def estimate_convergence_order(nx_list: list, error_list: list) -> Tuple[float, float]:
    """
    通过log-log拟合估计收敛阶
    
    Args:
        nx_list: 网格数量列表（递增）
        error_list: 对应网格的误差列表
    
    Returns:
        (order, r_squared): 收敛阶和拟合优度
    """
    if len(nx_list) < 3 or len(error_list) < 3:
        return np.nan, np.nan
    
    # 计算网格间距 h = 1/nx
    h_list = [1.0 / nx for nx in nx_list]
    
    # 取对数
    log_h = np.log(h_list)
    log_error = np.log(error_list)
    
    # 线性回归
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_h, log_error)
    
    return slope, r_value**2


def compute_mass_conservation(q_initial: np.ndarray, q_final: np.ndarray, dx: float) -> float:
    """
    计算质量守恒误差
    
    Args:
        q_initial: 初始状态 [h, hu]
        q_final: 最终状态 [h, hu]
        dx: 网格间距
    
    Returns:
        相对质量误差 |Δm| / m0
    """
    mass_initial = np.sum(q_initial[0, :]) * dx
    mass_final = np.sum(q_final[0, :]) * dx
    
    if mass_initial < 1e-15:
        return np.nan
    
    return abs(mass_final - mass_initial) / mass_initial


def compute_all_errors(numerical: np.ndarray, exact: np.ndarray, dx: float = 1.0) -> Dict[str, float]:
    """
    计算所有误差范数
    
    Args:
        numerical: 数值解
        exact: 精确解
        dx: 网格间距
    
    Returns:
        包含L1, L2, L∞误差的字典
    """
    return {
        'L1': compute_l1_error(numerical, exact, dx),
        'L2': compute_l2_error(numerical, exact, dx),
        'L∞': compute_linf_error(numerical, exact)
    }
