"""
动画演示页面

提供时间演化动画和对比功能
"""

from typing import Dict, List

import numpy as np
import streamlit as st

st.set_page_config(page_title="动画演示 | CFD-Class", page_icon="🎬", layout="wide")


def generate_animation_data(params: Dict) -> Dict:
    """生成动画数据（模拟后端计算）"""
    domain_length = params.get("domain_length", 1000.0)
    nx = params.get("nx", 100)
    h_l = params.get("h_l", 10.0)
    h_r = params.get("h_r", 1.0)
    t_end = params.get("t_end", 50.0)
    scheme = params.get("scheme", "Lax-Friedrichs")
    
    x = np.linspace(0, domain_length, nx)
    t_steps = 20
    times = np.linspace(0, t_end, t_steps)
    
    result = {}
    for t in times:
        sigma = 50 + t * 10
        peak_factor = max(0.1, 1 - t / t_end * 0.3)
        
        h = h_r + (h_l - h_r) * (
            0.5 * (1 + np.tanh((domain_length/2 - x) / sigma)) * peak_factor +
            0.2 * np.exp(-((x - domain_length/2)**2) / (2 * sigma**2))
        )
        
        if "Lax-Friedrichs" in scheme:
            h += np.random.normal(0, 0.05, len(x)) * h * 0.05
        elif "Lax-Wendroff" in scheme:
            h += np.random.normal(0, 0.03, len(x)) * h * 0.03
        elif "MacCormack" in scheme:
            h += np.random.normal(0, 0.02, len(x)) * h * 0.02
        elif "Godunov" in scheme:
            h = np.maximum(h_r * 0.9, h)
        elif "HLL" in scheme:
            h = np.maximum(h_r * 0.85, h)
        elif "MUSCL" in scheme:
            h += np.random.normal(0, 0.01, len(x)) * h * 0.01
        
        h = np.maximum(h_r * 0.5, h)
        u = np.zeros_like(h) + np.random.normal(0, 0.1, len(x))
        
        result[round(t, 2)] = np.vstack([h, u])
    
    return {"x": x, "result": result}


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
        x_dam = st.slider("大坝位置 [m]", 0.0, domain_length, domain_length / 2, 10.0)
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

    # 初始化session_state
    if "animation_data" not in st.session_state:
        st.session_state.animation_data = None
        st.session_state.current_scheme = None
        st.session_state.current_time_steps = None

    # 主内容区
    st.header("🎥 动画控制")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ 生成动画", type="primary"):
            with st.spinner("🔄 正在生成动画..."):
                try:
                    params = {
                        "domain_length": domain_length,
                        "nx": nx,
                        "_x_dam": domain_length / 2,
                        "h_l": h_l,
                        "h_r": h_r,
                        "t_end": t_end,
                    }
                    
                    data = generate_animation_data(params)
                    
                    if data["result"]:
                        st.success("✅ 动画数据生成完成！")
                        st.session_state.animation_data = data
                        st.session_state.current_scheme = scheme
                        st.session_state.current_time_steps = time_steps
                    else:
                        st.error("❌ 动画生成失败")

                except Exception as e:
                    st.error(f"❌ 动画生成失败: {e}")

    # 如果已有动画数据，显示动画
    if st.session_state.animation_data is not None:
        display_animation(
            st.session_state.animation_data["x"],
            st.session_state.animation_data["result"],
            st.session_state.current_scheme,
            st.session_state.current_time_steps,
        )

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
        import matplotlib
        
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False

        time_points = sorted(result.keys())
        step_size = max(1, len(time_points) // n_steps)
        selected_times = time_points[::step_size][:n_steps]

        # 初始化播放状态
        if "playback_state" not in st.session_state:
            st.session_state.playback_state = {
                "playing": False,
                "current_index": 0,
                "speed": 1.0,
                "play_key": 0
            }

        # 播放控制
        col_control1, col_control2, col_control3, col_control4 = st.columns([1, 1, 1, 2])
        with col_control1:
            if st.button("▶️ 播放", key=f"play_btn_{st.session_state.playback_state['play_key']}"):
                st.session_state.playback_state["playing"] = True
                st.session_state.playback_state["play_key"] += 1
        with col_control2:
            if st.button("⏸️ 暂停"):
                st.session_state.playback_state["playing"] = False
        with col_control3:
            if st.button("🔄 重置"):
                st.session_state.playback_state["playing"] = False
                st.session_state.playback_state["current_index"] = 0
        with col_control4:
            speed = st.slider("播放速度", 0.1, 3.0, 1.0, 0.1)
            st.session_state.playback_state["speed"] = speed

        # 自动播放逻辑 - 在渲染前更新索引
        if st.session_state.playback_state["playing"]:
            if st.session_state.playback_state["current_index"] < len(time_points) - 1:
                st.session_state.playback_state["current_index"] += 1
            else:
                # 播放完成，重置
                st.session_state.playback_state["playing"] = False
                st.session_state.playback_state["current_index"] = 0

        # 获取当前时间索引
        current_idx = st.session_state.playback_state["current_index"]
        selected_time = time_points[current_idx]

        # 时间滑块
        selected_time = st.slider(
            "选择时刻",
            min_value=0.0,
            max_value=max(time_points),
            value=selected_time,
            step=time_points[1] - time_points[0] if len(time_points) > 1 else 0.1,
        )
        # 更新当前索引
        closest_t = min(time_points, key=lambda t: abs(t - selected_time))
        st.session_state.playback_state["current_index"] = max(0, min(len(time_points) - 1, time_points.index(closest_t)))

        # 找到最接近的时间步
        closest_time = min(time_points, key=lambda t: abs(t - selected_time))
        closest_result = result[closest_time]

        col1, col2 = st.columns(2)

        # 水深
        fig, ax = plt.subplots(figsize=(8, 5))
        h = closest_result[0, :]
        ax.fill_between(x, 0, h, alpha=0.3, color="blue")
        ax.plot(x, h, "b-", linewidth=2)
        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Water Depth h (m)")
        ax.set_title(f"水深分布 (t = {closest_time:.3f}s)")
        ax.grid(True, alpha=0.3)
        col1.pyplot(fig)

        # 速度
        fig, ax = plt.subplots(figsize=(8, 5))
        h = closest_result[0, :]
        hu = closest_result[1, :]
        u = hu / np.where(h > 0, h, 1)
        ax.plot(x, u, "r-", linewidth=2)
        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Velocity u (m/s)")
        ax.set_title(f"速度分布 (t = {closest_time:.3f}s)")
        ax.grid(True, alpha=0.3)
        col2.pyplot(fig)

        # 播放状态指示和自动循环触发
        if st.session_state.playback_state["playing"]:
            st.info(f"▶️ 正在播放... ({current_idx + 1}/{len(time_points)})")
            # 使用空按钮触发重新渲染
            st.button("播放中", key=f"play_loop_{current_idx}", disabled=True)
            st.rerun()

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