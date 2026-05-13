"""
动画演示页面

提供时间演化动画和对比功能
"""

from typing import Dict, List

import numpy as np
import streamlit as st

st.set_page_config(page_title="动画演示 | CFD-Class", page_icon="🎬", layout="wide")


def _adapt_scheme_for_evolve(scheme, config):
    """适配层：为scheme添加evolve方法兼容"""
    if hasattr(scheme, 'evolve'):
        return scheme.evolve(config)
    
    h0, u0 = config.initial_condition()
    dx = config.dx
    result = scheme.run_simulation(
        h0=h0, u0=u0, cfl=config.cfl, dx=dx, t_end=config.t_end
    )
    
    output = {}
    for i, t in enumerate(result.t):
        h = result.h[i]
        u = result.u[i]
        output[round(float(t), 6)] = np.vstack([h, u])
    return output


def main():
    """动画演示页面主函数"""
    st.title("🎬 时间演化动画")
    st.markdown("查看溃坝问题的动态演化过程")
    st.divider()

    # 参数配置
    st.sidebar.header("⚙️ 动画参数")

    with st.sidebar.expander("📐 物理参数", expanded=True):
        domain_length = st.number_input("计算域长度 [m]", 100.0, 5000.0, 1000.0, 100.0)
        nx = st.number_input("网格数量", 10, 5000, 100, 10)
        _x_dam = st.slider("大坝位置 [m]", 0.0, domain_length, domain_length / 2, 10.0)
        h_l = st.number_input("左侧水深 h_l [m]", 0.001, 100.0, 10.0, 0.1)
        h_r = st.number_input("右侧水深 h_r [m]", 0.001, 100.0, 1.0, 0.1)

    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        t_end = st.number_input("结束时间 [s]", 0.01, 200.0, 50.0, 1.0)
        time_steps = st.slider("显示时间步数", 5, 50, 20, 5)

    # 方案选择
    st.sidebar.divider()
    scheme = st.sidebar.selectbox(
        "选择数值方案",
        [
            "Lax-Friedrichs",
            "Lax-Wendroff",
            "MacCormack",
            "Godunov",
            "HLL",
            "MUSCL-Hancock",
        ],
    )

    # 主内容区
    st.header("🎥 动画控制")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ 生成动画", type="primary"):
            with st.spinner("🔄 正在生成动画..."):
                try:
                    from src.core.config import DamBreakConfig
                    from src.core.schemes import get_scheme

                    config = DamBreakConfig(
                        domain_length=domain_length,
                        nx=nx,
                        x_dam=_x_dam,
                        h_l=h_l,
                        h_r=h_r,
                        t_end=t_end,
                    )

                    selected_scheme = get_scheme(scheme)
                    result = _adapt_scheme_for_evolve(selected_scheme, config)

                    if result:
                        st.success("✅ 动画数据生成完成！")
                        display_animation(config.x, result, scheme, time_steps)
                    else:
                        st.error("❌ 动画生成失败")

                except ImportError as e:
                    st.error(f"❌ 核心模块未实现: {e}")
                    st.info("💡 请先完成后端开发")

    # 动画说明
    with st.expander("📖 动画说明", expanded=False):
        st.markdown("""
        **动画功能说明**:

        1. **时间演化**: 显示水深和速度随时间的变化
        2. **多时刻对比**: 在同一图中显示多个时刻的解
        3. **物理过程**: 观察稀疏波、接触间断和激波的传播

        **使用步骤**:
        1. 配置物理参数
        2. 选择数值方案
        3. 点击「生成动画」
        4. 使用滑块控制时间步
        """)


def display_animation(x: np.ndarray, result: Dict, scheme_name: str, n_steps: int):
    """显示动画

    Args:
        x: 空间坐标
        result: 模拟结果
        scheme_name: 方案名称
        n_steps: 显示的时间步数
    """
    st.divider()
    st.header(f"🎬 {scheme_name} 时间演化")

    try:
        import matplotlib.pyplot as plt

        time_points = sorted(result.keys())
        step_size = max(1, len(time_points) // n_steps)
        selected_times = time_points[::step_size][:n_steps]

        # 时间滑块
        selected_time = st.slider(
            "选择时刻",
            min_value=0.0,
            max_value=max(time_points),
            value=0.0,
            step=time_points[1] - time_points[0] if len(time_points) > 1 else 0.1,
        )

        # 找到最接近的时间步
        closest_time = min(time_points, key=lambda t: abs(t - selected_time))
        closest_result = result[closest_time]

        col1, col2 = st.columns(2)

        with col1:
            # 水深
            fig, ax = plt.subplots(figsize=(8, 5))
            h = closest_result[0, :]
            ax.fill_between(x, 0, h, alpha=0.3, color="blue")
            ax.plot(x, h, "b-", linewidth=2)
            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Water Depth h (m)")
            ax.set_title(f"水深分布 (t = {closest_time:.3f}s)")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            # 速度
            fig, ax = plt.subplots(figsize=(8, 5))
            u = closest_result[1, :] / closest_result[0, :]
            ax.plot(x, u, "r-", linewidth=2)
            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Velocity u (m/s)")
            ax.set_title(f"速度分布 (t = {closest_time:.3f}s)")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        # 多时刻对比图
        st.subheader("📊 多时刻对比")
        fig, ax = plt.subplots(figsize=(10, 6))

        for t in selected_times:
            if t in result:
                h = result[t][0, :]
                ax.plot(x, h, label=f"t = {t:.2f}s", alpha=0.7)

        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Water Depth h (m)")
        ax.set_title(f"时间演化 - {scheme_name}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


if __name__ == "__main__":
    main()