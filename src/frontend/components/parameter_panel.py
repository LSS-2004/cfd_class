"""
参数面板组件

提供参数配置和验证功能
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable
import numpy as np


def render_parameter_panel(
    params: Optional[Dict[str, Any]] = None,
    on_change: Optional[Callable] = None
) -> Dict[str, Any]:
    """渲染参数配置面板

    Args:
        params: 默认参数值
        on_change: 参数变化回调函数

    Returns:
        Dict[str, Any]: 当前参数值
    """
    if params is None:
        params = {}

    st.sidebar.header("⚙️ 物理参数配置")

    # 域参数
    with st.sidebar.expander("📐 域参数", expanded=True):
        L = st.number_input(
            "Domain Length L (m)",
            min_value=1.0,
            max_value=100.0,
            value=params.get("L", 10.0),
            step=1.0,
            help="计算域长度"
        )
        nx = st.slider(
            "网格数 nx",
            min_value=50,
            max_value=500,
            value=params.get("nx", 200),
            step=10,
            help="空间网格数量"
        )
        x_dam = st.number_input(
            "溃坝位置 x_dam (m)",
            min_value=0.0,
            max_value=L,
            value=params.get("x_dam", L / 2),
            step=0.5,
            help="溃坝位置（相对于domain左端）"
        )

    # 初始条件
    with st.sidebar.expander("🌊 初始条件", expanded=True):
        h_L = st.number_input(
            "左侧水深 h_L (m)",
            min_value=0.01,
            max_value=20.0,
            value=params.get("h_L", 2.0),
            step=0.1,
            help="溃坝左侧初始水深"
        )
        h_R = st.number_input(
            "右侧水深 h_R (m)",
            min_value=0.01,
            max_value=20.0,
            value=params.get("h_R", 1.0),
            step=0.1,
            help="溃坝右侧初始水深"
        )
        u_L = st.number_input(
            "左侧速度 u_L (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=params.get("u_L", 0.0),
            step=0.1,
            help="溃坝左侧初始速度"
        )
        u_R = st.number_input(
            "右侧速度 u_R (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=params.get("u_R", 0.0),
            step=0.1,
            help="溃坝右侧初始速度"
        )

    # 时间参数
    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        g = st.number_input(
            "重力加速度 g (m/s²)",
            min_value=1.0,
            max_value=20.0,
            value=params.get("g", 9.81),
            step=0.01,
            help="重力加速度（默认9.81）"
        )
        t_end = st.number_input(
            "终止时间 t_end (s)",
            min_value=0.1,
            max_value=10.0,
            value=params.get("t_end", 1.0),
            step=0.1,
            help="模拟终止时间"
        )
        cfl = st.slider(
            "CFL数",
            min_value=0.1,
            max_value=0.9,
            value=params.get("cfl", 0.5),
            step=0.05,
            help="Courant-Friedrichs-Lewy条件数"
        )

    current_params = {
        "L": L,
        "nx": nx,
        "x_dam": x_dam,
        "h_L": h_L,
        "h_R": h_R,
        "u_L": u_L,
        "u_R": u_R,
        "g": g,
        "t_end": t_end,
        "cfl": cfl
    }

    # 参数验证
    validate_params(current_params)

    # 回调
    if on_change:
        on_change(current_params)

    return current_params


def validate_params(params: Dict[str, Any]) -> bool:
    """验证参数合法性

    Args:
        params: 参数字典

    Returns:
        bool: 验证是否通过
    """
    errors = []

    if params["h_L"] <= 0 or params["h_R"] <= 0:
        errors.append("水深必须大于0")

    if params["x_dam"] < 0 or params["x_dam"] > params["L"]:
        errors.append("溃坝位置必须在域内")

    if params["t_end"] <= 0:
        errors.append("终止时间必须大于0")

    if params["cfl"] <= 0 or params["cfl"] > 1:
        errors.append("CFL数必须在(0,1]之间")

    if errors:
        st.sidebar.error("⚠️ 参数错误:\n" + "\n".join(errors))
        return False

    return True


def render_preset_selector() -> Optional[Dict[str, Any]]:
    """渲染预设参数选择器

    Returns:
        Optional[Dict[str, Any]]: 选择的预设参数
    """
    presets = {
        "经典溃坝": {
            "L": 10.0,
            "nx": 200,
            "x_dam": 5.0,
            "h_L": 2.0,
            "h_R": 1.0,
            "u_L": 0.0,
            "u_R": 0.0,
            "g": 9.81,
            "t_end": 1.0,
            "cfl": 0.5
        },
        "大水深比": {
            "L": 10.0,
            "nx": 200,
            "x_dam": 5.0,
            "h_L": 5.0,
            "h_R": 1.0,
            "u_L": 0.0,
            "u_R": 0.0,
            "g": 9.81,
            "t_end": 1.0,
            "cfl": 0.5
        },
        "小水深比": {
            "L": 10.0,
            "nx": 200,
            "x_dam": 5.0,
            "h_L": 1.5,
            "h_R": 1.0,
            "u_L": 0.0,
            "u_R": 0.0,
            "g": 9.81,
            "t_end": 1.0,
            "cfl": 0.5
        },
        "长时模拟": {
            "L": 20.0,
            "nx": 400,
            "x_dam": 10.0,
            "h_L": 2.0,
            "h_R": 1.0,
            "u_L": 0.0,
            "u_R": 0.0,
            "g": 9.81,
            "t_end": 5.0,
            "cfl": 0.5
        }
    }

    selected = st.sidebar.selectbox(
        "📋 快速预设",
        ["自定义"] + list(presets.keys()),
        help="选择预设参数配置"
    )

    if selected != "自定义":
        return presets[selected]

    return None
