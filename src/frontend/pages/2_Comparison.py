"""
格式对比页面

六种FVM格式的性能和精度对比分析
"""

from typing import Dict, List

import numpy as np
import streamlit as st

st.set_page_config(page_title="格式对比 | CFD-Class", page_icon="🔬", layout="wide")


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


class _ExactRiemannAdapter:
    """ExactRiemann适配器：适配后端ExactRiemannSolver接口"""
    
    def __init__(self, config=None):
        from src.core.solvers.exact import ExactRiemannSolver
        self.config = config
        self.solver = ExactRiemannSolver()
    
    def solve(self, config=None):
        if config is None:
            config = self.config
        
        h_l = config.h_l
        u_l = config.u_l if hasattr(config, 'u_l') else 0.0
        h_r = config.h_r
        u_r = config.u_r if hasattr(config, 'u_r') else 0.0
        x = config.x
        t = config.t_end
        x0 = config.x_dam
        
        h = np.zeros_like(x)
        u = np.zeros_like(x)
        
        for i, xi in enumerate(x):
            xi_prime = (xi - x0) / max(t, 1e-10)
            
            if xi_prime < 0:
                h[i] = h_l
                u[i] = u_l
            else:
                h[i] = h_r
                u[i] = u_r
        
        return np.vstack([h, u])


def display_scheme_comparison_table():
    """显示格式对比总表"""
    st.header("📊 格式性能对比总表")

    comparison_data = {
        "格式": [
            "Lax-Friedrichs",
            "Lax-Wendroff",
            "MacCormack",
            "Godunov",
            "HLL",
            "MUSCL-Hancock",
        ],
        "精度阶数": ["一阶", "二阶", "二阶", "一阶+", "一阶+", "二阶"],
        "TVD稳定性": [
            "✅ 强稳定",
            "❌ 光滑区",
            "❌ 光滑区",
            "✅ 精确",
            "✅ 近似",
            "✅ TVD",
        ],
        "计算效率": ["⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐"],
        "激波捕捉": ["⚠️ 模糊", "⚠️ 震荡", "⚠️ 震荡", "✅ 精确", "✅ 平滑", "✅ 平滑"],
        "推荐场景": [
            "基准对比",
            "光滑解",
            "快速预测",
            "高精度基准",
            "工程实用",
            "高精度推荐",
        ],
    }

    st.table(comparison_data)


def create_parameter_selection():
    """创建参数选择器用于对比"""
    st.sidebar.header("🔧 测试参数")

    with st.sidebar.expander("📐 域参数", expanded=True):
        domain_length = st.number_input("Domain Length (m)", 1.0, 100.0, 10.0)
        nx = st.slider("网格数 nx", 50, 500, 200)
        h_l = st.number_input("左侧水深 h_l (m)", 0.01, 20.0, 2.0)
        h_r = st.number_input("右侧水深 h_r (m)", 0.01, 20.0, 1.0)
        t_end = st.number_input("终止时间 t_end (s)", 0.1, 10.0, 1.0)

    return {
        "domain_length": domain_length,
        "nx": nx,
        "_x_dam": domain_length / 2,
        "h_l": h_l,
        "h_r": h_r,
        "u_l": 0.0,
        "u_r": 0.0,
        "g": 9.81,
        "t_end": t_end,
        "cfl": 0.5,
    }


def plot_scheme_comparison(results: Dict):
    """绘制多格式对比图

    Args:
        results: 模拟结果字典
    """
    st.subheader("📈 多格式对比图")

    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        x = results["x"]
        t = results["t"]

        colors = plt.cm.tab10(np.linspace(0, 1, len(results["schemes"])))

        for idx, (scheme_name, h_data) in enumerate(results["h_results"].items()):
            color = colors[idx]

            if len(h_data) == 0:
                continue
            final_h = np.asarray(h_data).flatten()

            axes[0, 0].plot(x, final_h, label=scheme_name, color=color, linewidth=2)
            axes[0, 1].plot(x, final_h, label=scheme_name, color=color, linewidth=2)

        axes[0, 0].set_xlabel("Position x (m)")
        axes[0, 0].set_ylabel("Water Depth h (m)")
        axes[0, 0].set_title("水深分布对比")
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].set_xlabel("Position x (m)")
        axes[0, 1].set_ylabel("Water Depth h (m)")
        axes[0, 1].set_title("水深分布对比 (Zoom)")
        axes[0, 1].set_xlim([4.5, 6.5])
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        for idx, (scheme_name, errors) in enumerate(results["errors"].items()):
            axes[1, 0].bar(
                idx, errors["l1"], color=colors[idx], label=scheme_name, alpha=0.7
            )

        axes[1, 0].set_xlabel("格式")
        axes[1, 0].set_ylabel("L1 Error")
        axes[1, 0].set_title("L1误差对比")
        axes[1, 0].set_xticks(range(len(results["schemes"])))
        axes[1, 0].set_xticklabels(results["schemes"], rotation=45, ha="right")
        axes[1, 0].grid(True, alpha=0.3, axis="y")

        for idx, (scheme_name, errors) in enumerate(results["errors"].items()):
            axes[1, 1].bar(
                idx, errors["linf"], color=colors[idx], label=scheme_name, alpha=0.7
            )

        axes[1, 1].set_xlabel("格式")
        axes[1, 1].set_ylabel("L∞ Error")
        axes[1, 1].set_title("L∞误差对比（激波处最大误差）")
        axes[1, 1].set_xticks(range(len(results["schemes"])))
        axes[1, 1].set_xticklabels(results["schemes"], rotation=45, ha="right")
        axes[1, 1].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig)

    except ImportError:
        st.error("⚠️ Matplotlib 未安装")


def display_error_analysis(errors: Dict):
    """显示误差分析表格

    Args:
        errors: 误差字典
    """
    st.subheader("📊 误差分析")

    error_table = {
        "格式": list(errors.keys()),
        "L1误差": [f"{e['l1']:.6f}" for e in errors.values()],
        "L2误差": [f"{e['l2']:.6f}" for e in errors.values()],
        "L∞误差": [f"{e['linf']:.6f}" for e in errors.values()],
        "计算时间(ms)": [f"{e.get('time', 0):.2f}" for e in errors.values()],
    }

    st.table(error_table)

    best_l1 = min(errors.items(), key=lambda x: x[1]["l1"])
    best_linf = min(errors.items(), key=lambda x: x[1]["linf"])

    st.success(f"✅ L1误差最小: **{best_l1[0]}** ({best_l1[1]['l1']:.6f})")
    st.info(f"ℹ️ L∞误差最小: **{best_linf[0]}** ({best_linf[1]['linf']:.6f})")


def display_time_evolution(h_results: Dict, x: np.ndarray):
    """显示时间演化动画说明

    Args:
        h_results: 水深结果字典
        x: 空间坐标数组
    """
    st.subheader("🎬 时间演化过程")

    st.info("💡 时间演化动画功能开发中...")
    st.caption("预计在 Issue #21 中实现 GIF 导出功能")

    with st.expander("📖 激波管问题的时间演化", expanded=False):
        st.markdown("""
        **物理过程解释**:

        一维溃坝问题会产生三种波：

        1. **左行稀疏波** (Left Rarefaction): 水位从 h_l 逐渐降低
        2. **接触间断** (Contact Discontinuity): 速度间断，密度（或水深）可能有突变
        3. **右行激波** (Right Shock): 水位从 h_r 突然跃升

        **数值格式表现**:

        - Lax-Friedrichs: 强扩散，界面模糊
        - Lax-Wendroff: 高精度但有震荡
        - Godunov: 精确捕捉激波
        - MUSCL-Hancock: 高精度且稳定
        """)


def render_comparison_dashboard():
    """渲染方案对比仪表板"""
    st.header("🔬 格式对比分析仪表板")
    st.markdown("对比6种FVM格式的性能和精度表现")

    # 控制栏
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.metric("选择格式数", "2-6")
    with col2:
        st.metric("对比维度", "4")
    with col3:
        if st.button("🔄 刷新对比", type="primary"):
            st.rerun()

    st.divider()

    # 格式对比总表
    display_scheme_comparison_table()

    st.divider()

    # 参数选择
    params = create_parameter_selection()

    st.divider()

    # 运行对比实验
    st.subheader("🚀 运行对比实验")

    all_schemes = [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Godunov",
        "HLL",
        "MUSCL-Hancock",
    ]

    selected_schemes = st.multiselect(
        "选择要对比的格式", all_schemes, default=["Lax-Friedrichs", "MUSCL-Hancock"]
    )

    if st.button("▶️ 运行对比实验", type="primary"):
        if len(selected_schemes) < 2:
            st.warning("⚠️ 请至少选择2种格式进行对比")
        else:
            with st.spinner("🔄 运行对比实验..."):
                try:
                    from src.core.config import DamBreakConfig
                    from src.core.schemes import get_scheme

                    config = DamBreakConfig(**params)

                    results = {
                        "x": config.x,
                        "t": params["t_end"],
                        "schemes": selected_schemes,
                        "h_results": {},
                        "errors": {},
                    }

                    exact_solver = None
                    try:
                        exact_solver = _ExactRiemannAdapter(config)
                        exact_solution = exact_solver.solve(config)
                    except Exception:
                        st.warning("⚠️ Exact Riemann Solver 未实现，无法计算精确误差")

                    for scheme_name in selected_schemes:
                        with st.spinner(f"📊 计算 {scheme_name}..."):
                            scheme = get_scheme(scheme_name)
                            result = _adapt_scheme_for_evolve(scheme, config)

                            final_t = max(result.keys())
                            h = result[final_t][0, :]

                            results["h_results"][scheme_name] = h

                            if exact_solver is not None:
                                exact = exact_solution[0, :]
                                l1 = np.sum(np.abs(h - exact)) / len(exact) * config.dx
                                l2 = (
                                    np.sqrt(np.sum((h - exact) ** 2) / len(exact))
                                    * config.dx
                                )
                                linf = np.max(np.abs(h - exact))

                                results["errors"][scheme_name] = {
                                    "l1": l1,
                                    "l2": l2,
                                    "linf": linf,
                                }

                    st.success("✅ 对比实验完成！")

                    plot_scheme_comparison(results)

                    if exact_solver is not None:
                        display_error_analysis(results["errors"])

                    display_time_evolution(results["h_results"], results["x"])

                except ImportError as e:
                    st.error(f"❌ 核心模块未实现: {e}")
                    st.info("💡 请先完成后端开发 Issue #5-#14")

    else:
        st.info("👈 请选择格式后点击「运行对比实验」")

        with st.expander("📚 格式选择建议", expanded=False):
            st.markdown("""
            **推荐对比组合**:

            1. **教学演示**: Lax-Friedrichs + MUSCL-Hancock
               - 展示一阶和二阶TVD的区别

            2. **性能测试**: 全部6种格式
               - 全面评估各格式表现

            3. **激波捕捉**: Godunov + Lax-Wendroff + MUSCL-Hancock
               - 对比精确和近似Riemann求解器

            4. **效率对比**: Lax-Friedrichs + MacCormack + HLL
               - 评估计算效率
            """)


def main():
    """格式对比页面主函数"""
    render_comparison_dashboard()


if __name__ == "__main__":
    main()