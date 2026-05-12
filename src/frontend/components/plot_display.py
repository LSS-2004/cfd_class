"""
绑图显示组件

提供绑图渲染、动画和交互功能
"""

import base64
import io
from typing import Dict, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from numpy.typing import NDArray

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def render_plot(
    x: NDArray[np.float64],
    y_data: Dict[str, NDArray[np.float64]],
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    figsize: Tuple[int, int] = (10, 6),
    show_grid: bool = True,
    show_legend: bool = True,
    fill_between: Optional[Dict[str, Tuple[float, float]]] = None,
) -> None:
    """渲染绑图

    Args:
        x: x轴数据
        y_data: y轴数据字典 {名称: 数据}
        title: 绑图标题
        xlabel: x轴标签
        ylabel: y轴标签
        figsize: 绑图尺寸
        show_grid: 是否显示网格
        show_legend: 是否显示图例
        fill_between: 填充区域 {名称: (下限, 上限)}
    """
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=figsize)

        colors = plt.cm.tab10(np.linspace(0, 1, len(y_data)))

        for idx, (name, y) in enumerate(y_data.items()):
            ax.plot(x, y, label=name, color=colors[idx], linewidth=2)

            # 填充区域
            if fill_between and name in fill_between:
                lower, upper = fill_between[name]
                ax.fill_between(x, lower, upper, alpha=0.2, color=colors[idx])

        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        if title:
            ax.set_title(title, fontsize=14, fontweight="bold")

        if show_grid:
            ax.grid(True, alpha=0.3, linestyle="--")

        if show_legend:
            ax.legend(loc="best", fontsize=10)

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")
        st.info("请运行: pip install matplotlib")


def render_height_profile(
    x: NDArray[np.float64],
    h: NDArray[np.float64],
    exact: Optional[NDArray[np.float64]] = None,
    title: str = "水深分布",
    fill: bool = True,
) -> None:
    """渲染水深剖面图

    Args:
        x: 空间坐标
        h: 水深数据
        exact: 精确解（可选）
        title: 标题
        fill: 是否填充水下区域
    """
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))

        # 填充水下区域
        if fill:
            ax.fill_between(x, 0, h, alpha=0.3, color="blue", label="Numerical")

        ax.plot(x, h, "b-", linewidth=2, label="Numerical")

        if exact is not None:
            ax.plot(x, exact, "k--", linewidth=2, label="Exact")
            if fill:
                ax.fill_between(x, 0, exact, alpha=0.1, color="gray")

        ax.set_xlabel("Position x (m)", fontsize=12)
        ax.set_ylabel("Water Depth h (m)", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(loc="best", fontsize=10)

        # 添加水平参考线
        ax.axhline(y=0, color="k", linewidth=0.5)

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_velocity_profile(
    x: NDArray[np.float64],
    u: NDArray[np.float64],
    exact: Optional[NDArray[np.float64]] = None,
    title: str = "速度分布",
) -> None:
    """渲染速度剖面图

    Args:
        x: 空间坐标
        u: 速度数据
        exact: 精确解（可选）
        title: 标题
    """
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(x, u, "r-", linewidth=2, label="Numerical")

        if exact is not None:
            ax.plot(x, exact, "k--", linewidth=2, label="Exact")

        ax.set_xlabel("Position x (m)", fontsize=12)
        ax.set_ylabel("Velocity u (m/s)", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(loc="best", fontsize=10)

        # 添加零速度参考线
        ax.axhline(y=0, color="k", linewidth=0.5, linestyle="--")

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_comparison_plot(
    x: NDArray[np.float64],
    results: Dict[str, Dict[float, NDArray[np.float64]]],
    config: Dict,
    exact_solution: Optional[NDArray[np.float64]] = None,
) -> None:
    """渲染对比绑图

    Args:
        x: 空间坐标
        results: 模拟结果 {格式名称: {时刻: 解}}
        config: 配置参数
        exact_solution: 精确解（可选）
    """
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        colors = plt.cm.tab10(np.linspace(0, 1, len(results)))

        # 水深分布
        for idx, (scheme_name, result) in enumerate(results.items()):
            final_t = max(result.keys())
            h = result[final_t][0, :]
            axes[0, 0].plot(x, h, label=scheme_name, color=colors[idx], linewidth=2)

        if exact_solution is not None:
            axes[0, 0].plot(x, exact_solution[0, :], "k--", label="Exact", linewidth=2)

        axes[0, 0].set_xlabel("Position x (m)")
        axes[0, 0].set_ylabel("Water Depth h (m)")
        axes[0, 0].set_title("水深分布")
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # 速度分布
        for idx, (scheme_name, result) in enumerate(results.items()):
            final_t = max(result.keys())
            u = result[final_t][1, :] / result[final_t][0, :]
            axes[0, 1].plot(x, u, label=scheme_name, color=colors[idx], linewidth=2)

        if exact_solution is not None:
            u_exact = exact_solution[1, :] / exact_solution[0, :]
            axes[0, 1].plot(x, u_exact, "k--", label="Exact", linewidth=2)

        axes[0, 1].set_xlabel("Position x (m)")
        axes[0, 1].set_ylabel("Velocity u (m/s)")
        axes[0, 1].set_title("速度分布")
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # 误差分析
        if exact_solution is not None:
            errors = {}
            for scheme_name, result in results.items():
                numerical = result[max(result.keys())][0, :]
                exact = exact_solution[0, :]
                l1 = (
                    np.sum(np.abs(numerical - exact))
                    / len(exact)
                    * config.get("dx", 1.0)
                )
                errors[scheme_name] = l1

            axes[1, 0].bar(
                range(len(errors)),
                list(errors.values()),
                color=colors[: len(errors)],
                alpha=0.7,
            )
            axes[1, 0].set_xticks(range(len(errors)))
            axes[1, 0].set_xticklabels(list(errors.keys()), rotation=45, ha="right")
            axes[1, 0].set_ylabel("L1 Error")
            axes[1, 0].set_title("L1误差对比")
            axes[1, 0].grid(True, alpha=0.3, axis="y")

        # 收敛性分析
        axes[1, 1].text(
            0.5,
            0.5,
            "收敛性分析\n(需要多网格计算)",
            ha="center",
            va="center",
            transform=axes[1, 1].transAxes,
            fontsize=14,
            bbox=dict(boxstyle="round", facecolor="wheat"),
        )
        axes[1, 1].set_title("收敛性分析")
        axes[1, 1].axis("off")

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_animation(
    x: NDArray[np.float64],
    time_steps: List[float],
    results: Dict[float, NDArray[np.float64]],
    scheme_name: str,
    exact_results: Optional[Dict[float, NDArray[np.float64]]] = None,
) -> None:
    """渲染时间演化动画（使用 Streamlit slider）

    Args:
        x: 空间坐标
        time_steps: 时间步列表
        results: 时间演化结果 {时刻: 解}
        scheme_name: 格式名称
        exact_results: 精确解时间演化（可选）
    """
    try:
        import matplotlib.pyplot as plt

        st.subheader(f"🎬 时间演化 - {scheme_name}")

        # 时间滑块
        selected_time = st.slider(
            "选择时刻",
            min_value=0.0,
            max_value=max(time_steps),
            value=0.0,
            step=time_steps[1] - time_steps[0] if len(time_steps) > 1 else 0.1,
            help="拖动滑块查看不同时刻的解",
        )

        # 找到最接近的时间步
        closest_time = min(time_steps, key=lambda t: abs(t - selected_time))

        col1, col2 = st.columns(2)

        with col1:
            # 水深
            fig, ax = plt.subplots(figsize=(8, 5))
            h = results[closest_time][0, :]
            ax.fill_between(x, 0, h, alpha=0.3, color="blue")
            ax.plot(x, h, "b-", linewidth=2, label="Numerical")

            if exact_results and closest_time in exact_results:
                h_exact = exact_results[closest_time][0, :]
                ax.plot(x, h_exact, "k--", linewidth=2, label="Exact")
                ax.fill_between(x, 0, h_exact, alpha=0.1, color="gray")

            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Water Depth h (m)")
            ax.set_title(f"水深分布 (t = {closest_time:.3f}s)")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            # 速度
            fig, ax = plt.subplots(figsize=(8, 5))
            u = results[closest_time][1, :] / results[closest_time][0, :]
            ax.plot(x, u, "r-", linewidth=2, label="Numerical")

            if exact_results and closest_time in exact_results:
                u_exact = (
                    exact_results[closest_time][1, :]
                    / exact_results[closest_time][0, :]
                )
                ax.plot(x, u_exact, "k--", linewidth=2, label="Exact")

            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Velocity u (m/s)")
            ax.set_title(f"速度分布 (t = {closest_time:.3f}s)")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        # 播放控制
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶️ 自动播放", key=f"play_{scheme_name}"):
                st.info("💡 自动播放功能需要 Streamlit 组件支持，当前使用滑块手动控制")

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_time_evolution(
    x: NDArray[np.float64],
    time_steps: List[float],
    results: Dict[float, NDArray[np.float64]],
    scheme_name: str,
) -> None:
    """渲染时间演化静态图

    Args:
        x: 空间坐标
        time_steps: 时间步列表
        results: 时间演化结果 {时刻: 解}
        scheme_name: 格式名称
    """
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))

        for t in time_steps:
            if t in results:
                h = results[t][0, :]
                ax.plot(x, h, label=f"t = {t:.2f}s", alpha=0.7)

        ax.set_xlabel("Position x (m)")
        ax.set_ylabel("Water Depth h (m)")
        ax.set_title(f"时间演化 - {scheme_name}")
        ax.legend()
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_error_table(errors: Dict[str, Dict[str, float]]) -> None:
    """渲染误差表格

    Args:
        errors: 误差数据 {格式名称: {误差类型: 值}}
    """
    error_table = {
        "格式": list(errors.keys()),
        "L1误差": [f"{e.get('l1', 0):.6f}" for e in errors.values()],
        "L2误差": [f"{e.get('l2', 0):.6f}" for e in errors.values()],
        "L∞误差": [f"{e.get('linf', 0):.6f}" for e in errors.values()],
    }

    st.table(error_table)

    # 高亮最佳结果
    if errors:
        best_l1 = min(errors.items(), key=lambda x: x[1].get("l1", float("inf")))
        st.success(f"✅ L1误差最小: **{best_l1[0]}** ({best_l1[1].get('l1', 0):.6f})")


def export_plot_png(fig) -> str:
    """将 matplotlib 图形导出为 PNG base64

    Args:
        fig: matplotlib 图形对象

    Returns:
        str: base64 编码的 PNG 图像
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    return img_str


def export_data_csv(x: NDArray, data: Dict[str, NDArray]) -> str:
    """导出数据为 CSV 格式

    Args:
        x: 空间坐标
        data: 数据字典

    Returns:
        str: CSV 格式字符串
    """
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    headers = ["x"] + list(data.keys())
    writer.writerow(headers)

    # 写入数据
    for i in range(len(x)):
        row = [x[i]] + [data[key][i] for key in data.keys()]
        writer.writerow(row)

    return output.getvalue()
