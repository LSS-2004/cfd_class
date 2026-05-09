"""
参数面板组件

提供参数配置和验证功能
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable, List
import numpy as np


# 预设参数配置
PRESETS = {
    "经典溃坝": {
        "L": 10.0, "nx": 200, "x_dam": 5.0,
        "h_L": 2.0, "h_R": 1.0, "u_L": 0.0, "u_R": 0.0,
        "g": 9.81, "t_end": 1.0, "cfl": 0.5,
        "description": "标准溃坝问题，水深比 2:1"
    },
    "大水深比": {
        "L": 10.0, "nx": 200, "x_dam": 5.0,
        "h_L": 5.0, "h_R": 1.0, "u_L": 0.0, "u_R": 0.0,
        "g": 9.81, "t_end": 1.0, "cfl": 0.5,
        "description": "大水深比 5:1，强间断"
    },
    "小水深比": {
        "L": 10.0, "nx": 200, "x_dam": 5.0,
        "h_L": 1.5, "h_R": 1.0, "u_L": 0.0, "u_R": 0.0,
        "g": 9.81, "t_end": 1.0, "cfl": 0.5,
        "description": "小水深比 1.5:1，弱间断"
    },
    "长时模拟": {
        "L": 20.0, "nx": 400, "x_dam": 10.0,
        "h_L": 2.0, "h_R": 1.0, "u_L": 0.0, "u_R": 0.0,
        "g": 9.81, "t_end": 5.0, "cfl": 0.5,
        "description": "长时间演化，大计算域"
    },
    "非零初速": {
        "L": 10.0, "nx": 200, "x_dam": 5.0,
        "h_L": 2.0, "h_R": 1.0, "u_L": 1.0, "u_R": -0.5,
        "g": 9.81, "t_end": 1.0, "cfl": 0.5,
        "description": "非零初始速度，复杂波系"
    },
    "细网格测试": {
        "L": 10.0, "nx": 1000, "x_dam": 5.0,
        "h_L": 2.0, "h_R": 1.0, "u_L": 0.0, "u_R": 0.0,
        "g": 9.81, "t_end": 1.0, "cfl": 0.5,
        "description": "高分辨率网格，收敛性测试"
    }
}


def render_parameter_panel(
    params: Optional[Dict[str, Any]] = None,
    on_change: Optional[Callable] = None,
    show_scheme_selection: bool = True,
    available_schemes: Optional[List[str]] = None
) -> Dict[str, Any]:
    """渲染参数配置面板

    Args:
        params: 默认参数值
        on_change: 参数变化回调函数
        show_scheme_selection: 是否显示方案选择
        available_schemes: 可用方案列表

    Returns:
        Dict[str, Any]: 当前参数值
    """
    if params is None:
        params = {}

    if available_schemes is None:
        available_schemes = [
            "Lax-Friedrichs",
            "Lax-Wendroff",
            "MacCormack",
            "Godunov",
            "HLL",
            "MUSCL-Hancock"
        ]

    st.sidebar.header("⚙️ 物理参数配置")

    # 预设选择
    preset = render_preset_selector()
    if preset is not None:
        params.update(preset)
        st.sidebar.success(f"✅ 已应用预设: {preset.get('_preset_name', '自定义')}")
        if "description" in preset:
            st.sidebar.caption(preset["description"])

    st.sidebar.divider()

    # 域参数
    with st.sidebar.expander("📐 域参数", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input(
                "Domain Length L (m)",
                min_value=1.0, max_value=1000.0,
                value=params.get("L", 10.0), step=1.0,
                help="计算域长度 (m)"
            )
        with col2:
            nx = st.number_input(
                "网格数 nx",
                min_value=10, max_value=5000,
                value=params.get("nx", 200), step=10,
                help="空间网格数量"
            )

        x_dam = st.slider(
            "溃坝位置 x_dam (m)",
            min_value=0.0, max_value=L,
            value=params.get("x_dam", L / 2), step=0.1,
            help="溃坝位置（相对于domain左端）"
        )

        dx = L / nx
        st.caption(f"网格间距 dx = {dx:.4f} m")

    # 初始条件
    with st.sidebar.expander("🌊 初始条件", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**左侧 (x < x_dam)**")
            h_L = st.number_input(
                "水深 h_L (m)",
                min_value=0.001, max_value=100.0,
                value=params.get("h_L", 2.0), step=0.1,
                help="溃坝左侧初始水深"
            )
            u_L = st.number_input(
                "速度 u_L (m/s)",
                min_value=-50.0, max_value=50.0,
                value=params.get("u_L", 0.0), step=0.1,
                help="溃坝左侧初始速度"
            )

        with col2:
            st.markdown("**右侧 (x > x_dam)**")
            h_R = st.number_input(
                "水深 h_R (m)",
                min_value=0.001, max_value=100.0,
                value=params.get("h_R", 1.0), step=0.1,
                help="溃坝右侧初始水深"
            )
            u_R = st.number_input(
                "速度 u_R (m/s)",
                min_value=-50.0, max_value=50.0,
                value=params.get("u_R", 0.0), step=0.1,
                help="溃坝右侧初始速度"
            )

        # 可视化初始条件
        if h_L > 0 and h_R > 0:
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.metric("水深比", f"{h_L/h_R:.2f}:1")
            with fig_col2:
                st.metric("Froude数 (左)", f"{u_L/np.sqrt(g*h_L):.3f}")

    # 时间参数
    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            g = st.number_input(
                "g (m/s²)",
                min_value=1.0, max_value=20.0,
                value=params.get("g", 9.81), step=0.01,
                help="重力加速度"
            )
        with col2:
            t_end = st.number_input(
                "t_end (s)",
                min_value=0.01, max_value=100.0,
                value=params.get("t_end", 1.0), step=0.1,
                help="模拟终止时间"
            )
        with col3:
            cfl = st.number_input(
                "CFL",
                min_value=0.01, max_value=1.0,
                value=params.get("cfl", 0.5), step=0.05,
                help="Courant-Friedrichs-Lewy条件数"
            )

        dt = cfl * dx / np.sqrt(g * max(h_L, h_R))
        n_steps = int(t_end / dt)
        st.caption(f"预估时间步长 dt ≈ {dt:.4f} s, 步数 ≈ {n_steps}")

    # 方案选择
    selected_schemes = []
    if show_scheme_selection:
        with st.sidebar.expander("🔢 数值方案", expanded=True):
            selected_schemes = st.multiselect(
                "选择计算方案",
                available_schemes,
                default=[available_schemes[0]] if available_schemes else [],
                help="选择一个或多个数值格式进行计算"
            )

            if len(selected_schemes) > 1:
                st.info(f"✅ 已选择 {len(selected_schemes)} 个方案进行对比")

    current_params = {
        "L": L, "nx": nx, "x_dam": x_dam,
        "h_L": h_L, "h_R": h_R, "u_L": u_L, "u_R": u_R,
        "g": g, "t_end": t_end, "cfl": cfl,
        "dx": dx, "dt": dt, "n_steps": n_steps,
        "schemes": selected_schemes
    }

    # 参数验证
    validation_result = validate_params(current_params)
    if not validation_result["valid"]:
        st.sidebar.error("⚠️ 参数错误:\n" + "\n".join(validation_result["errors"]))

    # 回调
    if on_change:
        on_change(current_params)

    return current_params


def validate_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """验证参数合法性

    Args:
        params: 参数字典

    Returns:
        Dict[str, Any]: 验证结果 {"valid": bool, "errors": List[str], "warnings": List[str]}
    """
    errors = []
    warnings = []

    # 基本验证
    if params["h_L"] <= 0 or params["h_R"] <= 0:
        errors.append("水深必须大于0")

    if params["x_dam"] < 0 or params["x_dam"] > params["L"]:
        errors.append("溃坝位置必须在域内 [0, L]")

    if params["t_end"] <= 0:
        errors.append("终止时间必须大于0")

    if params["cfl"] <= 0 or params["cfl"] > 1:
        errors.append("CFL数必须在 (0, 1] 之间")

    if params["nx"] < 10:
        errors.append("网格数至少为10")

    # 警告
    if params["h_L"] / params["h_R"] > 10:
        warnings.append("水深比过大，可能导致数值不稳定")

    if params["cfl"] > 0.8:
        warnings.append("CFL数较大，建议降低以保证稳定性")

    if params["nx"] > 1000:
        warnings.append("网格数较多，计算时间可能较长")

    if params.get("h_L", 0) > 0 and abs(params.get("u_L", 0)) > 5 * np.sqrt(params.get("g", 9.81) * params["h_L"]):
        warnings.append("左侧流速过大，可能超出浅水方程适用范围")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def render_preset_selector() -> Optional[Dict[str, Any]]:
    """渲染预设参数选择器

    Returns:
        Optional[Dict[str, Any]]: 选择的预设参数
    """
    preset_names = list(PRESETS.keys())

    selected = st.sidebar.selectbox(
        "📋 快速预设",
        ["自定义配置"] + preset_names,
        help="选择预设参数配置"
    )

    if selected != "自定义配置":
        preset = PRESETS[selected].copy()
        preset["_preset_name"] = selected
        return preset

    return None


def render_advanced_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """渲染高级参数配置

    Args:
        params: 当前参数

    Returns:
        Dict[str, Any]: 更新后的参数
    """
    with st.sidebar.expander("🔧 高级参数", expanded=False):
        st.markdown("**数值格式参数**")

        col1, col2 = st.columns(2)
        with col1:
            limiter = st.selectbox(
                "通量限制器",
                ["minmod", "superbee", "van_leer", "MC", "none"],
                help="TVD限制器类型"
            )
        with col2:
            order = st.selectbox(
                "空间精度",
                ["一阶", "二阶"],
                help="空间离散精度"
            )

        st.markdown("**输出控制**")
        col1, col2 = st.columns(2)
        with col1:
            output_interval = st.number_input(
                "输出间隔",
                min_value=1, max_value=1000,
                value=10, step=1,
                help="每多少步输出一次结果"
            )
        with col2:
            save_animation = st.checkbox(
                "保存动画",
                value=False,
                help="是否保存时间演化动画"
            )

        params.update({
            "limiter": limiter,
            "order": 1 if order == "一阶" else 2,
            "output_interval": output_interval,
            "save_animation": save_animation
        })

    return params


def get_parameter_summary(params: Dict[str, Any]) -> str:
    """获取参数摘要

    Args:
        params: 参数字典

    Returns:
        str: 参数摘要文本
    """
    return f"""
    **计算参数摘要**
    - 计算域: [0, {params['L']:.1f}] m, 网格数: {params['nx']}
    - 溃坝位置: {params['x_dam']:.1f} m
    - 初始条件: h_L={params['h_L']:.2f}m, h_R={params['h_R']:.2f}m
    - 终止时间: {params['t_end']:.2f}s, CFL: {params['cfl']:.2f}
    - 选择方案: {', '.join(params.get('schemes', []))}
    """
