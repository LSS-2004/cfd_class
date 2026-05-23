"""
参数面板组件

提供参数配置和验证功能
基于 B1 DamBreakConfig 规范实现
"""

from typing import Any, Callable, Dict, List, Optional

import numpy as np
import streamlit as st

g = 9.81

# 预设参数配置 - 基于 B1 DamBreakConfig 规范
PRESETS = {
    "标准溃坝 (B1默认)": {
        "domain_length": 1000.0,
        "nx": 100,
        "x_dam": 500.0,
        "h_l": 10.0,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 50.0,
        "cfl": 0.9,
        "boundary_type": "transmissive",
        "description": "B1 DamBreakConfig 默认值，大尺度溃坝",
    },
    "经典溃坝": {
        "domain_length": 10.0,
        "nx": 200,
        "x_dam": 5.0,
        "h_l": 2.0,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 1.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "标准溃坝问题，水深比 2:1",
    },
    "大水深比": {
        "domain_length": 10.0,
        "nx": 200,
        "x_dam": 5.0,
        "h_l": 5.0,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 1.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "大水深比 5:1，强间断",
    },
    "小水深比": {
        "domain_length": 10.0,
        "nx": 200,
        "x_dam": 5.0,
        "h_l": 1.5,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 1.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "小水深比 1.5:1，弱间断",
    },
    "长时模拟": {
        "domain_length": 20.0,
        "nx": 400,
        "x_dam": 10.0,
        "h_l": 2.0,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 5.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "长时间演化，大计算域",
    },
    "非零初速": {
        "domain_length": 10.0,
        "nx": 200,
        "x_dam": 5.0,
        "h_l": 2.0,
        "h_r": 1.0,
        "u_l": 1.0,
        "u_r": -0.5,
        "g": 9.81,
        "t_end": 1.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "非零初始速度，复杂波系",
    },
    "细网格测试": {
        "domain_length": 10.0,
        "nx": 1000,
        "x_dam": 5.0,
        "h_l": 2.0,
        "h_r": 1.0,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": 1.0,
        "cfl": 0.5,
        "boundary_type": "transmissive",
        "description": "高分辨率网格，收敛性测试",
    },
}


def render_parameter_panel(
    params: Optional[Dict[str, Any]] = None,
    on_change: Optional[Callable] = None,
    show_scheme_selection: bool = True,
    available_schemes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """渲染参数配置面板

    基于 B1 DamBreakConfig 规范:
    - domain_length: 计算域长度 [m] (默认 1000.0)
    - nx: 网格数量 (默认 100)
    - g: 重力加速度 [m/s²] (默认 9.81)
    - x_dam: 大坝位置 [m] (默认 500.0)
    - h_l: 左侧水深 [m] (默认 10.0)
    - h_r: 右侧水深 [m] (默认 1.0)
    - cfl: CFL数 (默认 0.9)
    - t_end: 结束时间 [s] (默认 50.0)
    - boundary_type: 边界条件类型 (默认 "transmissive")

    Args:
        params: 默认参数值
        on_change: 参数变化回调函数
        show_scheme_selection: 是否显示方案选择
        available_schemes: 可用方案列表

    Returns:
        Dict[str, Any]: 当前参数值 (符合 DamBreakConfig 规范)
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
            "MUSCL-Hancock",
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

    # 域参数 - 基于 B1 规范
    with st.sidebar.expander("📐 域参数", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            domain_length = st.number_input(
                "计算域长度 [m]",
                min_value=100.0,
                max_value=5000.0,
                value=params.get("domain_length", 1000.0),
                step=100.0,
                help="计算域长度 (B1默认: 1000.0m)",
            )
        with col2:
            nx = st.number_input(
                "网格数量",
                min_value=10,
                max_value=5000,
                value=params.get("nx", 100),
                step=10,
                help="空间网格数量 (B1默认: 100)",
            )

        x_dam = st.slider(
            "大坝位置 [m]",
            min_value=0.0,
            max_value=domain_length,
            value=params.get("x_dam", domain_length / 2),
            step=10.0,
            help="大坝位置（相对于domain左端）(B1默认: 500.0m)",
        )

        dx = domain_length / nx
        st.caption(f"网格间距 dx = {dx:.4f} m")

    # 初始条件 - 基于 B1 规范 (h_l, h_r)
    with st.sidebar.expander("🌊 初始条件", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**左侧 (x < x_dam)**")
            h_l = st.number_input(
                "左侧水深 h_l [m]",
                min_value=0.001,
                max_value=100.0,
                value=params.get("h_l", 10.0),
                step=0.1,
                help="溃坝左侧初始水深 (B1默认: 10.0m)",
            )
            u_l = st.number_input(
                "左侧速度 u_l [m/s]",
                min_value=-50.0,
                max_value=50.0,
                value=params.get("u_l", 0.0),
                step=0.1,
                help="溃坝左侧初始速度",
            )

        with col2:
            st.markdown("**右侧 (x > x_dam)**")
            h_r = st.number_input(
                "右侧水深 h_r [m]",
                min_value=0.001,
                max_value=100.0,
                value=params.get("h_r", 1.0),
                step=0.1,
                help="溃坝右侧初始水深 (B1默认: 1.0m)",
            )
            u_r = st.number_input(
                "右侧速度 u_r [m/s]",
                min_value=-50.0,
                max_value=50.0,
                value=params.get("u_r", 0.0),
                step=0.1,
                help="溃坝右侧初始速度",
            )

        # 可视化初始条件
        if h_l > 0 and h_r > 0:
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.metric("水深比", f"{h_l/h_r:.2f}:1")
            with fig_col2:
                st.metric("Froude数 (左)", f"{u_l/np.sqrt(g*h_l):.3f}")

    # 时间参数 - 基于 B1 规范 (t_end=50.0, cfl=0.9)
    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            g = st.number_input(
                "g [m/s²]",
                min_value=1.0,
                max_value=20.0,
                value=params.get("g", 9.81),
                step=0.01,
                help="重力加速度 (B1默认: 9.81)",
            )
        with col2:
            t_end = st.number_input(
                "结束时间 [s]",
                min_value=0.01,
                max_value=200.0,
                value=params.get("t_end", 50.0),
                step=1.0,
                help="模拟结束时间 (B1默认: 50.0s)",
            )
        with col3:
            cfl = st.number_input(
                "CFL",
                min_value=0.01,
                max_value=1.0,
                value=params.get("cfl", 0.9),
                step=0.05,
                help="Courant-Friedrichs-Lewy条件数 (B1默认: 0.9)",
            )

        dt = cfl * dx / np.sqrt(g * max(h_l, h_r))
        n_steps = int(t_end / dt)
        st.caption(f"预估时间步长 dt ≈ {dt:.4f} s, 步数 ≈ {n_steps}")

    # 边界条件 - B1 新增
    with st.sidebar.expander("🔒 边界条件", expanded=False):
        boundary_type = st.selectbox(
            "边界条件类型",
            ["transmissive", "reflective", "periodic"],
            index=0,
            help="边界条件类型 (B1默认: transmissive)",
        )

    # 方案选择
    selected_schemes = []
    if show_scheme_selection:
        with st.sidebar.expander("🔢 数值方案", expanded=True):
            selected_schemes = st.multiselect(
                "选择计算方案",
                available_schemes,
                default=[available_schemes[0]] if available_schemes else [],
                help="选择一个或多个数值格式进行计算",
            )

            if len(selected_schemes) > 1:
                st.info(f"✅ 已选择 {len(selected_schemes)} 个方案进行对比")

    # 返回符合 DamBreakConfig 规范的参数
    current_params = {
        "domain_length": domain_length,
        "nx": nx,
        "_x_dam": x_dam,
        "h_l": h_l,
        "h_r": h_r,
        "u_l": u_l,
        "u_r": u_r,
        "g": g,
        "t_end": t_end,
        "cfl": cfl,
        "boundary_type": boundary_type,
        "dx": dx,
        "dt": dt,
        "n_steps": n_steps,
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
        params: 参数字典 (符合 DamBreakConfig 规范)

    Returns:
        Dict[str, Any]: 验证结果 {"valid": bool, "errors": List[str], "warnings": List[str]}
    """
    errors = []
    warnings = []

    # 基本验证
    if params["h_l"] <= 0 or params["h_r"] <= 0:
        errors.append("水深必须大于0")

    if params["x_dam"] < 0 or params["x_dam"] > params["domain_length"]:
        errors.append("大坝位置必须在域内 [0, domain_length]")

    if params["t_end"] <= 0:
        errors.append("结束时间必须大于0")

    if params["cfl"] <= 0 or params["cfl"] > 1:
        errors.append("CFL数必须在 (0, 1] 之间")

    if params["nx"] < 10:
        errors.append("网格数至少为10")

    # 警告
    if params["h_l"] / params["h_r"] > 10:
        warnings.append("水深比过大，可能导致数值不稳定")

    if params["cfl"] > 0.9:
        warnings.append("CFL数较大，建议降低以保证稳定性 (B1默认: 0.9)")

    if params["nx"] > 1000:
        warnings.append("网格数较多，计算时间可能较长")

    if params.get("h_l", 0) > 0 and abs(params.get("u_l", 0)) > 5 * np.sqrt(
        params.get("g", 9.81) * params["h_l"]
    ):
        warnings.append("左侧流速过大，可能超出浅水方程适用范围")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def render_preset_selector() -> Optional[Dict[str, Any]]:
    """渲染预设参数选择器

    Returns:
        Optional[Dict[str, Any]]: 选择的预设参数
    """
    preset_names = list(PRESETS.keys())

    selected = st.sidebar.selectbox(
        "📋 快速预设", ["自定义配置"] + preset_names, help="选择预设参数配置"
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
                help="TVD限制器类型",
            )
        with col2:
            order = st.selectbox("空间精度", ["一阶", "二阶"], help="空间离散精度")

        st.markdown("**输出控制**")
        col1, col2 = st.columns(2)
        with col1:
            output_interval = st.number_input(
                "输出间隔",
                min_value=1,
                max_value=1000,
                value=10,
                step=1,
                help="每多少步输出一次结果",
            )
        with col2:
            save_animation = st.checkbox(
                "保存动画", value=False, help="是否保存时间演化动画"
            )

        params.update(
            {
                "limiter": limiter,
                "order": 1 if order == "一阶" else 2,
                "output_interval": output_interval,
                "save_animation": save_animation,
            }
        )

    return params


def get_parameter_summary(params: Dict[str, Any]) -> str:
    """获取参数摘要

    Args:
        params: 参数字典 (符合 DamBreakConfig 规范)

    Returns:
        str: 参数摘要文本
    """
    return f"""
    **计算参数摘要 (DamBreakConfig)**
    - 计算域: [0, {params['domain_length']:.1f}] m, 网格数: {params['nx']}
    - 大坝位置: {params['x_dam']:.1f} m
    - 初始条件: h_l={params['h_l']:.2f}m, h_r={params['h_r']:.2f}m
    - 结束时间: {params['t_end']:.2f}s, CFL: {params['cfl']:.2f}
    - 边界条件: {params.get('boundary_type', 'transmissive')}
    - 选择方案: {', '.join(params.get('schemes', []))}
    """
