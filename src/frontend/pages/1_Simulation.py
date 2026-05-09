"""
模拟运行页面

参数配置、物理模拟、结果展示
"""

import streamlit as st
import numpy as np
from typing import Dict, Any, Optional

# 页面配置
st.set_page_config(
    page_title="模拟运行 | CFD-Class",
    page_icon="📊",
    layout="wide"
)


def load_core_modules():
    """延迟加载核心模块"""
    try:
        from src.core.config import DamBreakConfig
        from src.core.schemes import (
            LaxFriedrichs, LaxWendroff, MacCormack,
            Godunov, HLL, MUSCLHancock
        )
        return True
    except ImportError as e:
        st.error(f"⚠️ 核心模块加载失败: {e}")
        st.info("💡 请确保后端开发已完成 #5-#14 Issue")
        return False


def create_parameter_panel() -> Dict[str, Any]:
    """创建参数配置面板

    Returns:
        Dict[str, Any]: 参数字典
    """
    st.sidebar.header("⚙️ 物理参数配置")

    with st.sidebar.expander("📐 域参数", expanded=True):
        L = st.number_input(
            "Domain Length L (m)",
            min_value=1.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
            help="计算域长度"
        )
        nx = st.slider(
            "网格数 nx",
            min_value=50,
            max_value=500,
            value=200,
            step=10,
            help="空间网格数量"
        )
        x_dam = st.number_input(
            "溃坝位置 x_dam (m)",
            min_value=0.0,
            max_value=L,
            value=L / 2,
            step=0.5,
            help="溃坝位置（相对于domain左端）"
        )

    with st.sidebar.expander("🌊 初始条件", expanded=True):
        h_L = st.number_input(
            "左侧水深 h_L (m)",
            min_value=0.01,
            max_value=20.0,
            value=2.0,
            step=0.1,
            help="溃坝左侧初始水深"
        )
        h_R = st.number_input(
            "右侧水深 h_R (m)",
            min_value=0.01,
            max_value=20.0,
            value=1.0,
            step=0.1,
            help="溃坝右侧初始水深"
        )
        u_L = st.number_input(
            "左侧速度 u_L (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=0.1,
            help="溃坝左侧初始速度"
        )
        u_R = st.number_input(
            "右侧速度 u_R (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=0.1,
            help="溃坝右侧初始速度"
        )

    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        g = st.number_input(
            "重力加速度 g (m/s²)",
            min_value=1.0,
            max_value=20.0,
            value=9.81,
            step=0.01,
            help="重力加速度（默认9.81）"
        )
        t_end = st.number_input(
            "终止时间 t_end (s)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="模拟终止时间"
        )
        cfl = st.slider(
            "CFL数",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
            help="Courant-Friedrichs-Lewy条件数"
        )

    return {
        "L": L,
        "nx": nx,
        "x_dam": x_dam,
        "h_L": h_L,
        "h_R": h_R,
        "u_L": u_L,
        "u_R": u_R,
        "g": g,
        "t_end": t_end,
        "cfl": cfl
    }


def create_scheme_selector() -> list:
    """创建格式选择器

    Returns:
        list: 选择的格式列表
    """
    st.sidebar.header("📐 数值格式选择")

    schemes = {
        "Lax-Friedrichs": {
            "desc": "一阶格式，强稳定，适合基准对比",
            "order": 1,
            "tvd": True
        },
        "Lax-Wendroff": {
            "desc": "二阶格式，适合光滑解测试",
            "order": 2,
            "tvd": False
        },
        "MacCormack": {
            "desc": "二阶格式，高效预测校正",
            "order": 2,
            "tvd": False
        },
        "Godunov": {
            "desc": "一阶+格式，精确Riemann求解",
            "order": 1,
            "tvd": True
        },
        "HLL": {
            "desc": "一阶+格式，近似Riemann求解",
            "order": 1,
            "tvd": True
        },
        "MUSCL-Hancock": {
            "desc": "二阶TVD格式，高精度推荐",
            "order": 2,
            "tvd": True
        }
    }

    selected_schemes = []

    st.sidebar.markdown("**选择格式（可多选）:**")
    for name, info in schemes.items():
        if st.sidebar.checkbox(
            f"✅ {name}",
            value=(name == "Lax-Friedrichs"),
            help=info["desc"]
        ):
            selected_schemes.append(name)
            st.sidebar.caption(f"   精度: {info['order']}阶 | TVD: {'是' if info['tvd'] else '否'}")

    if not selected_schemes:
        st.sidebar.warning("⚠️ 请至少选择一个格式")

    return selected_schemes


def display_scheme_info(schemes: list):
    """显示格式信息表格

    Args:
        schemes: 选择的格式列表
    """
    st.subheader("📐 已选格式信息")

    scheme_data = {
        "格式名称": schemes,
        "精度阶数": [
            "一阶" if s in ["Lax-Friedrichs", "Godunov", "HLL"] else "二阶"
            for s in schemes
        ],
        "TVD稳定性": [
            "✅ 是" if s in ["Lax-Friedrichs", "Godunov", "HLL", "MUSCL-Hancock"]
            else "❌ 否"
            for s in schemes
        ],
        "适用场景": [
            "基准对比" if s == "Lax-Friedrichs"
            else "光滑解" if s in ["Lax-Wendroff", "MacCormack"]
            else "高精度" if s == "MUSCL-Hancock"
            else "工程实用"
            for s in schemes
        ]
    }

    st.table(scheme_data)


def run_simulation(params: Dict[str, Any], schemes: list) -> Optional[Dict]:
    """运行模拟

    Args:
        params: 参数字典
        schemes: 选择的格式列表

    Returns:
        Optional[Dict]: 模拟结果
    """
    if not schemes:
        return None

    with st.spinner("🔄 正在运行模拟..."):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import get_scheme

            config = DamBreakConfig(**params)

            results = {}
            for idx, scheme_name in enumerate(schemes):
                status_text.text(f"📊 计算 {scheme_name}...")
                progress_bar.progress((idx + 1) / len(schemes))

                scheme = get_scheme(scheme_name)
                result = scheme.evolve(config)

                results[scheme_name] = result

            progress_bar.empty()
            status_text.empty()

            return {
                "config": config,
                "results": results,
                "success": True
            }

        except ImportError:
            st.error("❌ 核心模块未实现，请先完成 #5-#14 Issue")
            return None
        except Exception as e:
            st.error(f"❌ 模拟出错: {str(e)}")
            return None


def display_results(results: Dict):
    """显示模拟结果

    Args:
        results: 模拟结果字典
    """
    st.success("✅ 模拟完成！")

    config = results["config"]
    schemes_results = results["results"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 水深分布")

        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(10, 6))

            x = config.x

            for scheme_name, result in schemes_results.items():
                final_t = max(result.keys())
                h = result[final_t][0, :]

                ax.plot(x, h, label=scheme_name, linewidth=2)

            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Water Depth h (m)")
            ax.set_title(f"t = {config.t_end} s")
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

        except ImportError:
            st.info("📊 Matplotlib 未安装，结果以文本显示")
            for scheme_name, result in schemes_results.items():
                final_t = max(result.keys())
                st.write(f"**{scheme_name}**: {final_t}")

    with col2:
        st.subheader("📊 误差统计")

        try:
            from src.core.solvers.exact_riemann import ExactRiemann

            exact_solver = ExactRiemann(config)
            exact_solution = exact_solver.solve(config)

            error_data = {
                "格式": [],
                "L1误差": [],
                "L2误差": [],
                "L∞误差": []
            }

            for scheme_name, result in schemes_results.items():
                numerical = result[max(result.keys())][0, :]
                exact = exact_solution[0, :]

                l1 = np.sum(np.abs(numerical - exact)) / len(exact) * config.dx
                l2 = np.sqrt(np.sum((numerical - exact) ** 2) / len(exact)) * config.dx
                linf = np.max(np.abs(numerical - exact))

                error_data["格式"].append(scheme_name)
                error_data["L1误差"].append(f"{l1:.6f}")
                error_data["L2误差"].append(f"{l2:.6f}")
                error_data["L∞误差"].append(f"{linf:.6f}")

            st.table(error_data)

        except Exception as e:
            st.caption(f"误差计算: {str(e)}")


def main():
    """模拟运行页面主函数"""

    st.title("📊 模拟运行")
    st.markdown("配置参数、选择格式、运行一维溃坝模拟")

    params = create_parameter_panel()

    selected_schemes = create_scheme_selector()

    st.divider()

    if st.button("🚀 开始模拟", type="primary", disabled=not bool(selected_schemes)):
        results = run_simulation(params, selected_schemes)

        if results and results["success"]:
            display_scheme_info(selected_schemes)
            display_results(results)

            with st.expander("💾 导出选项"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📥 导出CSV"):
                        st.info("CSV导出功能开发中...")

                with col2:
                    if st.button("📄 生成报告"):
                        st.info("HTML报告生成功能开发中...")

    else:
        st.info("👈 请在左侧配置参数并选择格式后点击「开始模拟」")

        with st.expander("📖 参数说明", expanded=False):
            st.markdown("""
            **物理参数说明**:

            - **h_L, h_R**: 溃坝前后的初始水深，典型值为 h_L = 2m, h_R = 1m
            - **L**: 计算域长度，通常取 10m
            - **t_end**: 模拟时间，典型值为 1-2s
            - **CFL**: 稳定性条件参数，建议取 0.5

            **数值格式说明**:

            - **Lax-Friedrichs**: 最稳定的格式，适合教学演示
            - **MUSCL-Hancock**: 精度最高的格式，适合科研应用
            """)


if __name__ == "__main__":
    main()
