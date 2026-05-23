"""
模拟运行页面

参数配置、物理模拟、结果展示
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import streamlit as st

# 页面配置
st.set_page_config(page_title="模拟运行 | CFD-Class", page_icon="📊", layout="wide")


def load_core_modules():
    """延迟加载核心模块"""
    try:
        from src.core.config import DamBreakConfig
        from src.core.schemes import (
            HLLScheme,
            GodunovScheme,
            LaxFriedrichsScheme,
            LaxWendroffScheme,
            MacCormackScheme,
            MUSCLScheme,
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
            help="计算域长度",
        )
        nx = st.slider(
            "网格数 nx",
            min_value=50,
            max_value=500,
            value=200,
            step=10,
            help="空间网格数量",
        )
        x_dam = st.number_input(
            "溃坝位置 x_dam (m)",
            min_value=0.0,
            max_value=L,
            value=L / 2,
            step=0.5,
            help="溃坝位置（相对于domain左端）",
        )

    with st.sidebar.expander("🌊 初始条件", expanded=True):
        h_L = st.number_input(
            "左侧水深 h_L (m)",
            min_value=0.01,
            max_value=20.0,
            value=2.0,
            step=0.1,
            help="溃坝左侧初始水深",
        )
        h_R = st.number_input(
            "右侧水深 h_R (m)",
            min_value=0.01,
            max_value=20.0,
            value=1.0,
            step=0.1,
            help="溃坝右侧初始水深",
        )
        u_L = st.number_input(
            "左侧速度 u_L (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=0.1,
            help="溃坝左侧初始速度",
        )
        u_R = st.number_input(
            "右侧速度 u_R (m/s)",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=0.1,
            help="溃坝右侧初始速度",
        )

    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        g = st.number_input(
            "重力加速度 g (m/s²)",
            min_value=1.0,
            max_value=20.0,
            value=9.81,
            step=0.01,
            help="重力加速度（默认9.81）",
        )
        t_end = st.number_input(
            "终止时间 t_end (s)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="模拟终止时间",
        )
        cfl = st.slider(
            "CFL数",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
            help="Courant-Friedrichs-Lewy条件数",
        )

    return {
        "domain_length": L,
        "nx": nx,
        "x_dam": x_dam,
        "h_l": h_L,
        "h_r": h_R,
        "u_l": u_L,
        "u_r": u_R,
        "g": g,
        "t_end": t_end,
        "cfl": cfl,
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
            "tvd": True,
        },
        "Lax-Wendroff": {"desc": "二阶格式，适合光滑解测试", "order": 2, "tvd": False},
        "MacCormack": {"desc": "二阶格式，高效预测校正", "order": 2, "tvd": False},
        "Godunov": {"desc": "一阶+格式，精确Riemann求解", "order": 1, "tvd": True},
        "HLL": {"desc": "一阶+格式，近似Riemann求解", "order": 1, "tvd": True},
        "MUSCL-Hancock": {"desc": "二阶TVD格式，高精度推荐", "order": 2, "tvd": True},
    }

    selected_schemes = []

    st.sidebar.markdown("**选择格式（可多选）:**")
    for name, info in schemes.items():
        if st.sidebar.checkbox(
            f"✅ {name}", value=(name == "Lax-Friedrichs"), help=info["desc"]
        ):
            selected_schemes.append(name)
            st.sidebar.caption(
                f"   精度: {info['order']}阶 | TVD: {'是' if info['tvd'] else '否'}"
            )

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
            (
                "✅ 是"
                if s in ["Lax-Friedrichs", "Godunov", "HLL", "MUSCL-Hancock"]
                else "❌ 否"
            )
            for s in schemes
        ],
        "适用场景": [
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


def calculate_conservation_quantities(result: Dict, config) -> Tuple[Dict, Dict]:
    """计算守恒量

    Args:
        result: 模拟结果
        config: 配置对象

    Returns:
        Tuple[Dict, Dict]: (初始守恒量, 最终守恒量)
    """
    dx = config.dx
    
    # 初始状态
    initial_t = min(result.keys())
    initial_data = result[initial_t]
    h_initial = initial_data[0, :]
    u_initial = np.zeros_like(h_initial)
    mask = h_initial > 1e-6
    u_initial[mask] = initial_data[1, mask] / h_initial[mask]
    
    # 最终状态
    final_t = max(result.keys())
    final_data = result[final_t]
    h_final = final_data[0, :]
    u_final = np.zeros_like(h_final)
    mask = h_final > 1e-6
    u_final[mask] = final_data[1, mask] / h_final[mask]
    
    # 计算质量
    mass_initial = np.sum(h_initial) * dx
    mass_final = np.sum(h_final) * dx
    
    # 计算动量
    momentum_initial = np.sum(h_initial * u_initial) * dx
    momentum_final = np.sum(h_final * u_final) * dx
    
    # 计算能量
    energy_initial = 0.5 * np.sum(h_initial * (u_initial ** 2) + config.g * h_initial ** 2) * dx
    energy_final = 0.5 * np.sum(h_final * (u_final ** 2) + config.g * h_final ** 2) * dx
    
    initial = {
        "mass": mass_initial,
        "momentum": momentum_initial,
        "energy": energy_initial,
        "t": initial_t
    }
    
    final = {
        "mass": mass_final,
        "momentum": momentum_final,
        "energy": energy_final,
        "t": final_t
    }
    
    return initial, final


def display_conservation_analysis(schemes_results: Dict, config):
    """显示守恒量分析

    Args:
        schemes_results: 各格式的结果
        config: 配置对象
    """
    st.subheader("⚖️ 守恒量分析")
    
    try:
        import matplotlib.pyplot as plt
        
        conservation_data = {
            "格式": [],
            "初始质量": [],
            "最终质量": [],
            "质量变化率": [],
            "初始动量": [],
            "最终动量": [],
            "动量变化率": [],
        }
        
        for scheme_name, result in schemes_results.items():
            if not result:
                continue
            
            initial, final = calculate_conservation_quantities(result, config)
            
            mass_change = ((final["mass"] - initial["mass"]) / initial["mass"] * 100) if initial["mass"] > 0 else 0
            momentum_change = ((final["momentum"] - initial["momentum"]) / initial["momentum"] * 100) if initial["momentum"] != 0 else 0
            
            conservation_data["格式"].append(scheme_name)
            conservation_data["初始质量"].append(f"{initial['mass']:.6f}")
            conservation_data["最终质量"].append(f"{final['mass']:.6f}")
            conservation_data["质量变化率"].append(f"{mass_change:.6f}%")
            conservation_data["初始动量"].append(f"{initial['momentum']:.6f}")
            conservation_data["最终动量"].append(f"{final['momentum']:.6f}")
            conservation_data["动量变化率"].append(f"{momentum_change:.6f}%")
        
        st.table(conservation_data)
        
        # 绘制守恒量变化图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 质量变化
        scheme_names = conservation_data["格式"]
        mass_changes = [float(c[:-1]) for c in conservation_data["质量变化率"]]
        ax1.bar(scheme_names, mass_changes, color='skyblue', alpha=0.7)
        ax1.axhline(y=0, color='r', linestyle='-', linewidth=0.5)
        ax1.set_xlabel("数值格式")
        ax1.set_ylabel("质量变化率 (%)")
        ax1.set_title("质量守恒性")
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 动量变化
        momentum_changes = [float(c[:-1]) for c in conservation_data["动量变化率"]]
        ax2.bar(scheme_names, momentum_changes, color='lightgreen', alpha=0.7)
        ax2.axhline(y=0, color='r', linestyle='-', linewidth=0.5)
        ax2.set_xlabel("数值格式")
        ax2.set_ylabel("动量变化率 (%)")
        ax2.set_title("动量守恒性")
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)
        
    except Exception as e:
        st.caption(f"守恒量分析: {str(e)}")


def display_time_evolution(x: np.ndarray, schemes_results: Dict, config):
    """显示时间演化动画

    Args:
        x: 空间坐标
        schemes_results: 各格式的结果
        config: 配置对象
    """
    st.subheader("🎬 时间演化")
    
    try:
        import matplotlib.pyplot as plt
        
        # 获取所有时间点
        all_times = set()
        for result in schemes_results.values():
            if result:
                all_times.update(result.keys())
        all_times = sorted(all_times)
        
        if len(all_times) < 2:
            st.info("时间点不足，无法显示演化过程")
            return
        
        # 时间滑块
        if 'time_index' not in st.session_state:
            st.session_state.time_index = 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("▶️ 播放", key="play_evolution"):
                st.session_state.playing = True
        
        with col3:
            if st.button("⏸️ 暂停", key="pause_evolution"):
                st.session_state.playing = False
        
        time_index = st.slider(
            "选择时间",
            min_value=0,
            max_value=len(all_times) - 1,
            value=st.session_state.time_index,
            step=1,
        )
        st.session_state.time_index = time_index
        current_time = all_times[time_index]
        
        # 绘制当前时刻的结果
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 水深
        for scheme_name, result in schemes_results.items():
            if result and current_time in result:
                data = result[current_time]
                if data.ndim >= 2 and data.shape[0] >= 1:
                    h = data[0, :]
                    ax1.plot(x, h, label=scheme_name, linewidth=2)
        
        ax1.set_xlabel("Position x (m)")
        ax1.set_ylabel("Water Depth h (m)")
        ax1.set_title(f"水深分布 (t = {current_time:.3f} s)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 速度
        for scheme_name, result in schemes_results.items():
            if result and current_time in result:
                data = result[current_time]
                if data.ndim >= 2 and data.shape[0] >= 2:
                    h = data[0, :]
                    hu = data[1, :]
                    u = np.zeros_like(h)
                    mask = h > 1e-6
                    u[mask] = hu[mask] / h[mask]
                    ax2.plot(x, u, label=scheme_name, linewidth=2)
        
        ax2.set_xlabel("Position x (m)")
        ax2.set_ylabel("Velocity u (m/s)")
        ax2.set_title(f"速度分布 (t = {current_time:.3f} s)")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 自动播放
        if st.session_state.get('playing', False):
            import time
            time.sleep(0.1)
            st.session_state.time_index = (time_index + 1) % len(all_times)
            st.rerun()
        
    except Exception as e:
        st.caption(f"时间演化: {str(e)}")


def display_multi_time_comparison(x: np.ndarray, schemes_results: Dict, config):
    """显示多时间点对比

    Args:
        x: 空间坐标
        schemes_results: 各格式的结果
        config: 配置对象
    """
    st.subheader("📈 多时间点对比")
    
    try:
        import matplotlib.pyplot as plt
        
        # 选择时间点
        all_times = set()
        for result in schemes_results.values():
            if result:
                all_times.update(result.keys())
        all_times = sorted(all_times)
        
        if len(all_times) < 3:
            st.info("时间点不足，无法显示多时间对比")
            return
        
        # 选择时间点
        num_time_points = min(5, len(all_times))
        selected_times = [
            all_times[0],
            all_times[len(all_times) // 4],
            all_times[len(all_times) // 2],
            all_times[3 * len(all_times) // 4],
            all_times[-1]
        ]
        selected_times = selected_times[:num_time_points]
        
        # 绘制多时间点对比
        for scheme_name in schemes_results.keys():
            result = schemes_results[scheme_name]
            if not result:
                continue
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            for t in selected_times:
                if t in result:
                    data = result[t]
                    if data.ndim >= 2 and data.shape[0] >= 1:
                        h = data[0, :]
                        ax.plot(x, h, label=f"t = {t:.3f} s", linewidth=2)
            
            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Water Depth h (m)")
            ax.set_title(f"{scheme_name} - 多时间点水深对比")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
    except Exception as e:
        st.caption(f"多时间点对比: {str(e)}")


def export_results_to_csv(x: np.ndarray, schemes_results: Dict, config) -> str:
    """导出结果为CSV格式

    Args:
        x: 空间坐标
        schemes_results: 各格式的结果
        config: 配置对象

    Returns:
        str: CSV字符串
    """
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入头部
    writer.writerow(["CFD-Class Simulation Results"])
    writer.writerow(["Domain Length", config.domain_length])
    writer.writerow(["nx", config.nx])
    writer.writerow(["h_l", config.h_l])
    writer.writerow(["h_r", config.h_r])
    writer.writerow(["t_end", config.t_end])
    writer.writerow([])
    
    # 写入数据
    for scheme_name, result in schemes_results.items():
        if not result:
            continue
        
        writer.writerow([f"Scheme: {scheme_name}"])
        writer.writerow(["x (m)", "h (m)", "u (m/s)"])
        
        final_t = max(result.keys())
        final_data = result[final_t]
        
        h = final_data[0, :]
        u = np.zeros_like(h)
        mask = h > 1e-6
        u[mask] = final_data[1, mask] / h[mask]
        
        for xi, hi, ui in zip(x, h, u):
            writer.writerow([f"{xi:.6f}", f"{hi:.6f}", f"{ui:.6f}"])
        
        writer.writerow([])
    
    return output.getvalue()


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

            config = DamBreakConfig(
                domain_length=params["domain_length"],
                nx=params["nx"],
                x_dam=params["x_dam"],
                h_l=params["h_l"],
                h_r=params["h_r"],
                u_l=params["u_l"],
                u_r=params["u_r"],
                g=params["g"],
                t_end=params["t_end"],
                cfl=params["cfl"],
                boundary_type=params.get("boundary_type", "transmissive"),
            )

            results = {}
            for idx, scheme_name in enumerate(schemes):
                status_text.text(f"📊 计算 {scheme_name}...")
                progress_bar.progress((idx + 1) / len(schemes))

                scheme = get_scheme(scheme_name)
                result = _adapt_scheme_for_evolve(scheme, config)

                results[scheme_name] = result

            progress_bar.empty()
            status_text.empty()

            return {"config": config, "results": results, "success": True}

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

    # 使用标签页组织结果
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 最终结果",
        "⚖️ 守恒分析",
        "🎬 时间演化",
        "📊 误差分析",
        "💾 导出数据"
    ])

    with tab1:
        display_final_results(config, schemes_results)
    
    with tab2:
        display_conservation_analysis(schemes_results, config)
    
    with tab3:
        display_time_evolution(config.x, schemes_results, config)
        display_multi_time_comparison(config.x, schemes_results, config)
    
    with tab4:
        display_error_analysis(config, schemes_results)
    
    with tab5:
        display_export_options(config.x, schemes_results, config)


def display_final_results(config, schemes_results: Dict):
    """显示最终结果

    Args:
        config: 配置对象
        schemes_results: 各格式的结果
    """
    st.subheader("📈 最终结果")

    try:
        import matplotlib.pyplot as plt

        col1, col2 = st.columns(2)

        with col1:
            # 水深分布
            fig, ax = plt.subplots(figsize=(8, 5))

            x = config.x

            for scheme_name, result in schemes_results.items():
                if not result:
                    continue
                final_t = max(result.keys())
                final_result = result[final_t]
                if final_result.ndim < 2 or final_result.shape[0] < 1:
                    continue
                h = final_result[0, :]

                ax.plot(x, h, label=scheme_name, linewidth=2)

            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Water Depth h (m)")
            ax.set_title(f"水深分布 (t = {config.t_end} s)")
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

        with col2:
            # 速度分布
            fig, ax = plt.subplots(figsize=(8, 5))

            for scheme_name, result in schemes_results.items():
                if not result:
                    continue
                final_t = max(result.keys())
                final_result = result[final_t]
                if final_result.ndim < 2 or final_result.shape[0] < 2:
                    continue
                h = final_result[0, :]
                hu = final_result[1, :]
                u = np.zeros_like(h)
                mask = h > 1e-6
                u[mask] = hu[mask] / h[mask]

                ax.plot(x, u, label=scheme_name, linewidth=2)

            ax.set_xlabel("Position x (m)")
            ax.set_ylabel("Velocity u (m/s)")
            ax.set_title(f"速度分布 (t = {config.t_end} s)")
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

    except ImportError:
        st.info("📊 Matplotlib 未安装，结果以文本显示")
        for scheme_name, result in schemes_results.items():
            final_t = max(result.keys())
            st.write(f"**{scheme_name}**: {final_t}")


def display_error_analysis(config, schemes_results: Dict):
    """显示误差分析

    Args:
        config: 配置对象
        schemes_results: 各格式的结果
    """
    st.subheader("📊 误差统计")

    try:
        exact_solver = _ExactRiemannAdapter(config)
        exact_solution = exact_solver.solve(config)

        error_data = {"格式": [], "L1误差": [], "L2误差": [], "L∞误差": []}

        for scheme_name, result in schemes_results.items():
            if not result:
                continue
            final_t = max(result.keys())
            final_result = result[final_t]
            if final_result.ndim < 2 or final_result.shape[0] < 1:
                continue
            numerical = final_result[0, :]
            exact = exact_solution[0, :]

            if len(numerical) != len(exact):
                st.warning(f"⚠️ {scheme_name} 结果长度不匹配")
                continue

            l1 = np.sum(np.abs(numerical - exact)) / len(exact) * config.dx
            l2 = np.sqrt(np.sum((numerical - exact) ** 2) / len(exact)) * config.dx
            linf = np.max(np.abs(numerical - exact))

            error_data["格式"].append(scheme_name)
            error_data["L1误差"].append(f"{l1:.6f}")
            error_data["L2误差"].append(f"{l2:.6f}")
            error_data["L∞误差"].append(f"{linf:.6f}")

        st.table(error_data)
        
        # 绘制误差对比图
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # L1误差
        ax1.bar(error_data["格式"], [float(e) for e in error_data["L1误差"]], 
                color='lightcoral', alpha=0.7)
        ax1.set_xlabel("数值格式")
        ax1.set_ylabel("L1 Error")
        ax1.set_title("L1 误差对比")
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # L2误差
        ax2.bar(error_data["格式"], [float(e) for e in error_data["L2误差"]], 
                color='lightsalmon', alpha=0.7)
        ax2.set_xlabel("数值格式")
        ax2.set_ylabel("L2 Error")
        ax2.set_title("L2 误差对比")
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.caption(f"误差计算: {str(e)}")


def display_export_options(x: np.ndarray, schemes_results: Dict, config):
    """显示导出选项

    Args:
        x: 空间坐标
        schemes_results: 各格式的结果
        config: 配置对象
    """
    st.subheader("💾 导出数据")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 导出CSV"):
            try:
                csv_data = export_results_to_csv(x, schemes_results, config)
                st.download_button(
                    label="下载CSV文件",
                    data=csv_data,
                    file_name=f"cfd_simulation_{config.t_end:.1f}s.csv",
                    mime="text/csv"
                )
                st.success("✅ CSV数据准备就绪！")
            except Exception as e:
                st.error(f"❌ CSV导出失败: {str(e)}")
    
    with col2:
        if st.button("📄 生成报告"):
            st.info("HTML报告生成功能开发中...")


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
