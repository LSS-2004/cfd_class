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

    # 初始化session_state
    if 'animation_data' not in st.session_state:
        st.session_state.animation_data = None
    if 'animation_config' not in st.session_state:
        st.session_state.animation_config = None
    if 'animation_scheme' not in st.session_state:
        st.session_state.animation_scheme = ""
    if 'animation_nsteps' not in st.session_state:
        st.session_state.animation_nsteps = 20
    if 'animation_playing' not in st.session_state:
        st.session_state.animation_playing = False
    if 'animation_index' not in st.session_state:
        st.session_state.animation_index = 0
    if 'animation_speed' not in st.session_state:
        st.session_state.animation_speed = 1.0

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
                        # 保存到session_state
                        st.session_state.animation_data = result
                        st.session_state.animation_config = config
                        st.session_state.animation_scheme = scheme
                        st.session_state.animation_nsteps = time_steps
                        st.session_state.animation_index = 0
                        st.session_state.animation_playing = False
                        st.success("✅ 动画数据生成完成！")
                    else:
                        st.error("❌ 动画生成失败")

                except ImportError as e:
                    st.error(f"❌ 核心模块未实现: {e}")
                    st.info("💡 请先完成后端开发")

    # 显示动画（如果有数据）
    if st.session_state.animation_data is not None:
        display_animation(
            st.session_state.animation_config.x,
            st.session_state.animation_data,
            st.session_state.animation_scheme,
            st.session_state.animation_nsteps
        )
    else:
        st.info("👈 配置参数后点击「生成动画」")

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
        4. 使用播放按钮自动播放或滑块手动控制
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
        import time

        time_points = sorted(result.keys())
        step_size = max(1, len(time_points) // n_steps)
        selected_times = time_points[::step_size][:n_steps]

        # 播放控制
        col_play, col_speed, col_slider = st.columns([1, 1, 3])
        
        with col_play:
            play_key = f"play_btn_{scheme_name}"
            if st.button("▶️ 播放" if not st.session_state.animation_playing else "⏸️ 暂停", key=play_key):
                st.session_state.animation_playing = not st.session_state.animation_playing
        
        with col_speed:
            st.session_state.animation_speed = st.slider("速度", 0.5, 3.0, st.session_state.animation_speed, 0.5, label_visibility="collapsed")
        
        with col_slider:
            # 如果播放中，自动更新index
            if st.session_state.animation_playing:
                st.session_state.animation_index = (st.session_state.animation_index + 1) % len(time_points)
            
            selected_time_idx = st.slider(
                "选择时刻",
                min_value=0,
                max_value=len(time_points) - 1,
                value=st.session_state.animation_index,
                step=1,
                label_visibility="collapsed"
            )
            st.session_state.animation_index = selected_time_idx
            closest_time = time_points[selected_time_idx]

        # 找到最接近的时间步
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
            ax.set_ylim(0, max(h) * 1.2 if len(h) > 0 else 10)
            st.pyplot(fig)

        with col2:
            # 速度
            fig, ax = plt.subplots(figsize=(8, 5))
            u = np.zeros_like(x)
            mask = closest_result[0, :] > 1e-6
            u[mask] = closest_result[1, mask] / closest_result[0, mask]
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

        # 自动播放（使用st.rerun）
        if st.session_state.animation_playing:
            time.sleep(0.5 / st.session_state.animation_speed)
            st.rerun()

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


if __name__ == "__main__":
    main()
