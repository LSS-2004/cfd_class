"""
Riemann求解器模块

实现精确Riemann求解器和HLL近似求解器
"""

from typing import Dict, Tuple

import numpy as np


def exact_riemann_solution(
    q_left: np.ndarray, q_right: np.ndarray, g: float = 9.81
) -> Dict:
    """
    浅水方程精确Riemann求解器

    处理湿底和干底两种情况

    Args:
        q_left: 左侧状态 [h_l, h_l*u_l]
        q_right: 右侧状态 [h_r, h_r*u_r]
        g: 重力加速度

    Returns:
        包含波速、星区状态等信息的字典
    """
    h_l, hu_l = q_left[0], q_left[1]
    h_r, hu_r = q_right[0], q_right[1]

    u_l = hu_l / h_l if h_l > 0 else 0.0
    u_r = hu_r / h_r if h_r > 0 else 0.0

    c_l = np.sqrt(g * h_l) if h_l > 0 else 0.0
    c_r = np.sqrt(g * h_r) if h_r > 0 else 0.0

    # 判断是否为干底情况
    is_dry_left = h_l < 1e-12
    is_dry_right = h_r < 1e-12

    if is_dry_right:
        # 右干底：Ritter解
        h_star = (2 / 3) * (h_l + (u_l * np.sqrt(h_l)) / (2 * np.sqrt(g)))
        u_star = (2 / 3) * (u_l + 2 * c_l)
        s_l = u_l - c_l
        s_r = u_star + np.sqrt(g * h_star)

        result = {
            "type": "dry_right",
            "h_star": h_star,
            "u_star": u_star,
            "s_l": s_l,
            "s_r": s_r,
            "s_contact": u_star,
            "h_l": h_l,
            "h_r": h_r,
            "u_l": u_l,
            "u_r": u_r,
            "c_l": c_l,
            "c_r": c_r,
        }

    elif is_dry_left:
        # 左干底
        h_star = (2 / 3) * (h_r - (u_r * np.sqrt(h_r)) / (2 * np.sqrt(g)))
        u_star = (2 / 3) * (u_r - 2 * c_r)
        s_l = u_star - np.sqrt(g * h_star)
        s_r = u_r + c_r

        result = {
            "type": "dry_left",
            "h_star": h_star,
            "u_star": u_star,
            "s_l": s_l,
            "s_r": s_r,
            "s_contact": u_star,
            "h_l": h_l,
            "h_r": h_r,
            "u_l": u_l,
            "u_r": u_r,
            "c_l": c_l,
            "c_r": c_r,
        }

    else:
        # 湿底情况：完整Riemann解
        # 迭代求解h_star
        def f(h):
            if h <= h_l:
                term_l = (2 * c_l) / (g * h_l) * (h_l - h)
            else:
                term_l = 2 * np.sqrt(g) * (np.sqrt(h_l) - np.sqrt(h))

            if h <= h_r:
                term_r = (2 * c_r) / (g * h_r) * (h - h_r)
            else:
                term_r = 2 * np.sqrt(g) * (np.sqrt(h) - np.sqrt(h_r))

            return term_l + term_r + u_l - u_r

        def df_dh(h):
            if h <= h_l:
                d_l = -2 * c_l / (g * h_l)
            else:
                d_l = -2 * np.sqrt(g) / (2 * np.sqrt(h))

            if h <= h_r:
                d_r = 2 * c_r / (g * h_r)
            else:
                d_r = 2 * np.sqrt(g) / (2 * np.sqrt(h))

            return d_l + d_r

        # 牛顿迭代
        h_guess = max(h_l, h_r)
        for _ in range(20):
            f_val = f(h_guess)
            df_val = df_dh(h_guess)
            if abs(df_val) < 1e-15:
                break
            h_guess -= f_val / df_val
            if h_guess < 0:
                h_guess = 1e-12

        h_star = max(h_guess, 1e-12)

        # 计算星区速度
        if h_star <= h_l:
            u_star = u_l + (2 * c_l / (g * h_l)) * (h_l - h_star)
        else:
            u_star = u_l + 2 * (c_l - np.sqrt(g * h_star))

        # 计算波速
        if h_star <= h_l:
            s_l = u_l - c_l * np.sqrt(1 + (g * (h_star - h_l)) / (2 * c_l**2))
        else:
            s_l = u_l - c_l

        if h_star <= h_r:
            s_r = u_r + c_r * np.sqrt(1 + (g * (h_star - h_r)) / (2 * c_r**2))
        else:
            s_r = u_r + c_r

        result = {
            "type": "wet",
            "h_star": h_star,
            "u_star": u_star,
            "s_l": s_l,
            "s_r": s_r,
            "s_contact": u_star,
            "h_l": h_l,
            "h_r": h_r,
            "u_l": u_l,
            "u_r": u_r,
            "c_l": c_l,
            "c_r": c_r,
        }

    return result


def hll_flux(q_left: np.ndarray, q_right: np.ndarray, g: float = 9.81) -> np.ndarray:
    """
    HLL近似Riemann通量计算

    Args:
        q_left: 左侧状态 [h, hu]
        q_right: 右侧状态 [h, hu]
        g: 重力加速度

    Returns:
        HLL数值通量
    """
    h_l, hu_l = q_left[0], q_left[1]
    h_r, hu_r = q_right[0], q_right[1]

    u_l = hu_l / h_l if h_l > 0 else 0.0
    u_r = hu_r / h_r if h_r > 0 else 0.0

    c_l = np.sqrt(g * np.maximum(h_l, 0))
    c_r = np.sqrt(g * np.maximum(h_r, 0))

    # 估计波速
    s_l = min(u_l - c_l, u_r - c_r)
    s_r = max(u_l + c_l, u_r + c_r)

    # 计算通量
    f_l = np.array([hu_l, hu_l * u_l + 0.5 * g * h_l**2])
    f_r = np.array([hu_r, hu_r * u_r + 0.5 * g * h_r**2])

    if s_l >= 0:
        flux = f_l
    elif s_r <= 0:
        flux = f_r
    else:
        flux = (s_r * f_l - s_l * f_r + s_l * s_r * (q_right - q_left)) / (s_r - s_l)

    return flux


def godunov_flux(
    q_left: np.ndarray, q_right: np.ndarray, g: float = 9.81
) -> np.ndarray:
    """
    Godunov精确Riemann通量

    Args:
        q_left: 左侧状态
        q_right: 右侧状态
        g: 重力加速度

    Returns:
        Godunov数值通量
    """
    sol = exact_riemann_solution(q_left, q_right, g)

    h_l, hu_l = q_left[0], q_left[1]
    u_l = hu_l / h_l if h_l > 0 else 0.0

    s_l = sol["s_l"]
    s_contact = sol["s_contact"]
    h_star = sol["h_star"]
    u_star = sol["u_star"]

    # 根据波结构选择通量
    if s_l >= 0:
        # 使用左侧通量
        f = np.array([hu_l, hu_l * u_l + 0.5 * g * h_l**2])
    elif s_contact >= 0:
        # 使用星区通量（稀疏波）
        f = np.array([h_star * u_star, h_star * u_star**2 + 0.5 * g * h_star**2])
    else:
        # 使用右侧通量
        h_r, hu_r = q_right[0], q_right[1]
        u_r = hu_r / h_r if h_r > 0 else 0.0
        f = np.array([hu_r, hu_r * u_r + 0.5 * g * h_r**2])

    return f


def evaluate_riemann_solution(
    sol: Dict, x: np.ndarray, t: float, g: float = 9.81
) -> Tuple[np.ndarray, np.ndarray]:
    """
    在给定位置和时间评估Riemann解

    Args:
        sol: Riemann求解器返回的解字典
        x: 空间坐标数组
        t: 时间

    Returns:
        (h, u): 水深和速度数组
    """
    if t <= 0:
        # t=0时返回初始状态
        h = np.where(x < 0, sol["h_l"], sol["h_r"])
        u = np.where(x < 0, sol["u_l"], sol["u_r"])
        return h, u

    xi = x / t

    h = np.zeros_like(xi)
    u = np.zeros_like(xi)

    s_l = sol["s_l"]
    s_r = sol["s_r"]
    s_contact = sol["s_contact"]

    h_star = sol["h_star"]
    u_star = sol["u_star"]

    c_l = sol["c_l"]
    c_r = sol["c_r"]

    # 根据xi所在区域确定解
    if sol["type"] == "dry_right":
        # 右干底Ritter解
        # 区域1: xi <= s_l (左侧未受扰)
        mask = xi <= s_l
        h[mask] = sol["h_l"]
        u[mask] = sol["u_l"]

        # 区域2: s_l < xi <= s_contact (稀疏波)
        mask = (xi > s_l) & (xi <= s_contact)
        h[mask] = (2 / (9 * g)) * (2 * c_l + sol["u_l"] - xi[mask]) ** 2
        u[mask] = (2 / 3) * (sol["u_l"] + 2 * c_l + xi[mask])

        # 区域3: xi > s_contact (干底)
        mask = xi > s_contact
        h[mask] = 0
        u[mask] = 0

    elif sol["type"] == "dry_left":
        # 左干底
        # 区域1: xi <= s_l (干底)
        mask = xi <= s_l
        h[mask] = 0
        u[mask] = 0

        # 区域2: s_l < xi <= s_contact (稀疏波)
        mask = (xi > s_l) & (xi <= s_contact)
        h[mask] = (2 / (9 * g)) * (2 * c_r - sol["u_r"] + xi[mask]) ** 2
        u[mask] = (2 / 3) * (sol["u_r"] - 2 * c_r - xi[mask])

        # 区域3: xi > s_contact (右侧未受扰)
        mask = xi > s_contact
        h[mask] = sol["h_r"]
        u[mask] = sol["u_r"]

    else:
        # 湿底情况
        # 区域1: xi <= s_l (左侧未受扰)
        mask = xi <= s_l
        h[mask] = sol["h_l"]
        u[mask] = sol["u_l"]

        # 区域2: s_l < xi <= s_contact (左稀疏波或激波)
        if h_star > sol["h_l"]:
            # 激波
            mask = (xi > s_l) & (xi <= s_contact)
            h[mask] = h_star
            u[mask] = u_star
        else:
            # 稀疏波
            mask = (xi > s_l) & (xi <= s_contact)
            h[mask] = (2 / (9 * g)) * (2 * c_l + sol["u_l"] - xi[mask]) ** 2
            u[mask] = (2 / 3) * (sol["u_l"] + 2 * c_l + xi[mask])

        # 区域3: s_contact < xi <= s_r (接触间断右侧，星区)
        mask = (xi > s_contact) & (xi <= s_r)
        h[mask] = h_star
        u[mask] = u_star

        # 区域4: xi > s_r (右侧未受扰)
        mask = xi > s_r
        h[mask] = sol["h_r"]
        u[mask] = sol["u_r"]

    return h, u
