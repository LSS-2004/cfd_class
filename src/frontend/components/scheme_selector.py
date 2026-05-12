"""
格式选择器组件

提供数值格式选择功能
"""

from typing import Dict, List, Optional

import streamlit as st


def render_scheme_selector(
    selected: Optional[List[str]] = None, allow_multiple: bool = True
) -> List[str]:
    """渲染格式选择器

    Args:
        selected: 默认选中的格式
        allow_multiple: 是否允许多选

    Returns:
        List[str]: 选中的格式列表
    """
    if selected is None:
        selected = ["Lax-Friedrichs"]

    schemes = {
        "Lax-Friedrichs": {
            "desc": "一阶格式，强稳定，适合基准对比",
            "order": 1,
            "tvd": True,
            "icon": "🟢",
        },
        "Lax-Wendroff": {
            "desc": "二阶格式，适合光滑解测试",
            "order": 2,
            "tvd": False,
            "icon": "🟡",
        },
        "MacCormack": {
            "desc": "二阶格式，高效预测校正",
            "order": 2,
            "tvd": False,
            "icon": "🟡",
        },
        "Godunov": {
            "desc": "一阶+格式，精确Riemann求解",
            "order": 1,
            "tvd": True,
            "icon": "🟢",
        },
        "HLL": {
            "desc": "一阶+格式，近似Riemann求解",
            "order": 1,
            "tvd": True,
            "icon": "🟢",
        },
        "MUSCL-Hancock": {
            "desc": "二阶TVD格式，高精度推荐",
            "order": 2,
            "tvd": True,
            "icon": "🔵",
        },
    }

    st.sidebar.header("📐 数值格式选择")

    selected_schemes = []

    if allow_multiple:
        st.sidebar.markdown("**选择格式（可多选）:**")
        for name, info in schemes.items():
            if st.sidebar.checkbox(
                f"{info['icon']} {name}", value=(name in selected), help=info["desc"]
            ):
                selected_schemes.append(name)
                st.sidebar.caption(
                    f"   精度: {info['order']}阶 | TVD: {'是' if info['tvd'] else '否'}"
                )
    else:
        selected_name = st.sidebar.radio(
            "选择格式",
            list(schemes.keys()),
            index=list(schemes.keys()).index(selected[0]) if selected else 0,
        )
        selected_schemes = [selected_name]

    if not selected_schemes:
        st.sidebar.warning("⚠️ 请至少选择一个格式")

    return selected_schemes


def render_scheme_info(schemes: List[str]) -> None:
    """显示格式信息

    Args:
        schemes: 格式列表
    """
    scheme_data = {
        "格式名称": schemes,
        "精度阶数": [
            "一阶" if s in ["Lax-Friedrichs", "Godunov", "HLL"] else "二阶"
            for s in schemes
        ],
        "TVD稳定性": [
            (
                "✅ 是"
                if s in ["Lax-Friedrichs", "Godunov", "HLL", "MUSCL-Hancock"]
                else "❌ 否"
            )
            for s in schemes
        ],
        "推荐场景": [
            (
                "基准对比"
                if s == "Lax-Friedrichs"
                else (
                    "光滑解"
                    if s in ["Lax-Wendroff", "MacCormack"]
                    else "高精度" if s == "MUSCL-Hancock" else "工程实用"
                )
            )
            for s in schemes
        ],
    }

    st.table(scheme_data)


def render_scheme_comparison_card() -> None:
    """渲染格式对比卡片"""
    st.markdown("""
    ### 📊 格式特性对比

    | 特性 | Lax-Friedrichs | Lax-Wendroff | MacCormack | Godunov | HLL | MUSCL-Hancock |
    |------|----------------|--------------|------------|---------|-----|---------------|
    | 精度 | 一阶 | 二阶 | 二阶 | 一阶+ | 一阶+ | 二阶 |
    | TVD | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
    | 激波捕捉 | 模糊 | 震荡 | 震荡 | 精确 | 平滑 | 平滑 |
    | 计算效率 | 高 | 高 | 高 | 中 | 高 | 中 |
    | 推荐度 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
    """)
