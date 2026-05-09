"""
绑图显示组件

提供绑图渲染和交互功能
"""

import streamlit as st
import numpy as np
from typing import Dict, List, Optional, Tuple
from numpy.typing import NDArray


def render_plot(
    x: NDArray[np.float64],
    y_data: Dict[str, NDArray[np.float64]],
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    figsize: Tuple[int, int] = (10, 6),
    show_grid: bool = True,
    show_legend: bool = True
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
    """
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=figsize)

        colors = plt.cm.tab10(np.linspace(0, 1, len(y_data)))

        for idx, (name, y) in enumerate(y_data.items()):
            ax.plot(x, y, label=name, color=colors[idx], linewidth=2)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if title:
            ax.set_title(title)

        if show_grid:
            ax.grid(True, alpha=0.3)

        if show_legend:
            ax.legend()

        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")
        st.info("请运行: pip install matplotlib")


def render_comparison_plot(
    x: NDArray[np.float64],
    results: Dict[str, Dict[float, NDArray[np.float64]]],
    config: Dict,
    exact_solution: Optional[NDArray[np.float64]] = None
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
            axes[0, 0].plot(x, exact_solution[0, :], 'k--', label='Exact', linewidth=2)

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
            axes[0, 1].plot(x, u_exact, 'k--', label='Exact', linewidth=2)

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
                l1 = np.sum(np.abs(numerical - exact)) / len(exact) * config.get("dx", 1.0)
                errors[scheme_name] = l1

            axes[1, 0].bar(range(len(errors)), list(errors.values()),
                          color=colors[:len(errors)], alpha=0.7)
            axes[1, 0].set_xticks(range(len(errors)))
            axes[1, 0].set_xticklabels(list(errors.keys()), rotation=45, ha="right")
            axes[1, 0].set_ylabel("L1 Error")
            axes[1, 0].set_title("L1误差对比")
            axes[1, 0].grid(True, alpha=0.3, axis="y")

        # 收敛性分析
        axes[1, 1].text(0.5, 0.5, "收敛性分析\n(需要多网格计算)",
                       ha="center", va="center", transform=axes[1, 1].transAxes,
                       fontsize=14, bbox=dict(boxstyle="round", facecolor="wheat"))
        axes[1, 1].set_title("收敛性分析")
        axes[1, 1].axis("off")

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def render_time_evolution(
    x: NDArray[np.float64],
    time_steps: List[float],
    results: Dict[float, NDArray[np.float64]],
    scheme_name: str
) -> None:
    """渲染时间演化动画帧

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


def render_error_table(
    errors: Dict[str, Dict[str, float]]
) -> None:
    """渲染误差表格

    Args:
        errors: 误差数据 {格式名称: {误差类型: 值}}
    """
    error_table = {
        "格式": list(errors.keys()),
        "L1误差": [f"{e.get('l1', 0):.6f}" for e in errors.values()],
        "L2误差": [f"{e.get('l2', 0):.6f}" for e in errors.values()],
        "L∞误差": [f"{e.get('linf', 0):.6f}" for e in errors.values()]
    }

    st.table(error_table)

    # 高亮最佳结果
    if errors:
        best_l1 = min(errors.items(), key=lambda x: x[1].get("l1", float("inf")))
        st.success(f"✅ L1误差最小: **{best_l1[0]}** ({best_l1[1].get('l1', 0):.6f})")
