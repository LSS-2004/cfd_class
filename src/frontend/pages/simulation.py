"""
模拟运行页面

提供交互式溃坝模拟运行功能
"""

from typing import Any, Dict

import numpy as np
import streamlit as st

st.set_page_config(page_title="模拟运行 | CFD-Class", page_icon="📊", layout="wide")


def generate_simulation_data(x: np.ndarray, params: Dict) -> Dict[str, Dict]:
    """生成模拟数据（模拟后端计算）
    
    Args:
        x: 空间坐标
        params: 参数字典
        
    Returns:
        模拟结果字典
    """
    h_l = params.get("h_l", 10.0)
    h_r = params.get("h_r", 1.0)
    domain_length = params.get("domain_length", 1000.0)
    t_end = params.get("t_end", 50.0)
    
    results = {}
    schemes = params.get("schemes", ["Lax-Friedrichs"])
    
    for scheme_name in schemes:
        t_steps = 10
        times = np.linspace(0, t_end, t_steps)
        result = {}
        
        for t in times:
            # 生成模拟的溃坝波形
            sigma = 100 + t * 5
            peak_factor = max(0.1, 1 - t / t_end * 0.3)
            
            # 基础波形
            h = h_r + (h_l - h_r) * (
                0.5 * (1 + np.tanh((domain_length/2 - x) / sigma)) * peak_factor +
                0.2 * np.exp(-((x - domain_length/2)**2) / (2 * sigma**2))
            )
            
            # 添加方案特定的扰动
            if "Lax-Friedrichs" in scheme_name:
                h += np.random.normal(0, 0.05, len(x)) * h * 0.05
            elif "Lax-Wendroff" in scheme_name:
                h += np.random.normal(0, 0.03, len(x)) * h * 0.03
            elif "MacCormack" in scheme_name:
                h += np.random.normal(0, 0.02, len(x)) * h * 0.02
            elif "Godunov" in scheme_name:
                h = np.maximum(h_r * 0.9, h)
            elif "HLL" in scheme_name:
                h = np.maximum(h_r * 0.85, h)
            elif "MUSCL" in scheme_name:
                h += np.random.normal(0, 0.01, len(x)) * h * 0.01
            
            h = np.maximum(h_r * 0.5, h)
            
            result[round(t, 2)] = np.vstack([h, np.zeros_like(h)])
        
        results[scheme_name] = result
    
    return results


def main():
    """模拟运行页面主函数"""
    st.title("📊 交互式溃坝模拟")
    st.markdown("配置参数并运行一维溃坝数值模拟")
    st.divider()

    # 参数配置
    st.sidebar.header("⚙️ 物理参数配置")

    with st.sidebar.expander("📐 域参数", expanded=True):
        domain_length = st.number_input("计算域长度 [m]", 100.0, 5000.0, 1000.0, 100.0)
        nx = st.number_input("网格数量", 10, 5000, 100, 10)

    with st.sidebar.expander("🌊 初始条件", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            h_l = st.number_input("左侧水深 h_l [m]", 0.001, 100.0, 10.0, 0.1)
            u_l = st.number_input("左侧速度 u_l [m/s]", -50.0, 50.0, 0.0, 0.1)
        with col2:
            h_r = st.number_input("右侧水深 h_r [m]", 0.001, 100.0, 1.0, 0.1)
            u_r = st.number_input("右侧速度 u_r [m/s]", -50.0, 50.0, 0.0, 0.1)

    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        g = st.number_input("g [m/s²]", 1.0, 20.0, 9.81, 0.01)
        t_end = st.number_input("结束时间 [s]", 0.01, 200.0, 50.0, 1.0)
        cfl = st.number_input("CFL", 0.01, 1.0, 0.9, 0.05)

    with st.sidebar.expander("🔒 边界条件", expanded=False):
        boundary_type = st.selectbox(
            "边界条件类型", ["transmissive", "reflective", "periodic"]
        )

    # 方案选择
    st.sidebar.divider()
    st.sidebar.header("🔢 数值方案")
    available_schemes = [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Godunov",
        "HLL",
        "MUSCL-Hancock",
    ]
    selected_schemes = st.sidebar.multiselect(
        "选择计算方案", available_schemes, default=["Lax-Friedrichs"]
    )

    # 主内容区
    st.header("🚀 运行模拟")

    params = {
        "domain_length": domain_length,
        "nx": nx,
        "h_l": h_l,
        "h_r": h_r,
        "u_l": u_l,
        "u_r": u_r,
        "g": g,
        "t_end": t_end,
        "cfl": cfl,
        "boundary_type": boundary_type,
        "schemes": selected_schemes,
    }

    # 参数摘要
    with st.expander("📋 参数摘要", expanded=False):
        st.json(params)

    # 运行按钮
    if st.button("▶️ 开始模拟", type="primary"):
        if not selected_schemes:
            st.error("❌ 请至少选择一个数值方案")
        else:
            with st.spinner("🔄 正在运行模拟..."):
                try:
                    x = np.linspace(0, domain_length, nx)
                    results = generate_simulation_data(x, params)

                    st.success("✅ 模拟完成！")
                    display_results(x, results, params)

                except Exception as e:
                    st.error(f"❌ 模拟运行失败: {e}")

    else:
        st.info("👈 配置参数后点击「开始模拟」")


def display_results(x: np.ndarray, results: Dict, params: Dict[str, Any]):
    """显示模拟结果

    Args:
        x: 空间坐标
        results: 模拟结果字典
        params: 参数字典
    """
    st.divider()
    st.header("📈 模拟结果")

    try:
        import matplotlib.pyplot as plt

        # 水深分布
        fig, ax = plt.subplots(figsize=(10, 6))
        for scheme_name, result in results.items():
            if result:
                final_t = max(result.keys())
                final_result = result[final_t]
                if final_result.ndim >= 2 and final_result.shape[0] >= 1:
                    h = final_result[0, :]
                    ax.plot(x, h, label=scheme_name, linewidth=2)

        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Water Depth h (m)")
        ax.set_title("水深分布")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # 速度分布
        fig, ax = plt.subplots(figsize=(10, 6))
        for scheme_name, result in results.items():
            if result:
                final_t = max(result.keys())
                final_result = result[final_t]
                if final_result.ndim >= 2 and final_result.shape[0] >= 2:
                    h = final_result[0, :]
                    hu = final_result[1, :]
                    u = hu / np.where(h > 0, h, 1)
                    ax.plot(x, u, label=scheme_name, linewidth=2)

        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Velocity u (m/s)")
        ax.set_title("速度分布")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


if __name__ == "__main__":
    main()