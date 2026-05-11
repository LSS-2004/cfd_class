"""
报告生成页面

提供 HTML 报告生成功能
"""

import streamlit as st
import numpy as np
from typing import Dict, Any

st.set_page_config(
    page_title="报告生成 | CFD-Class",
    page_icon="📝",
    layout="wide"
)


def main():
    """报告生成页面主函数"""
    st.title("📝 模拟报告生成")
    st.markdown("生成符合学术规范的 HTML 分析报告")
    st.divider()

    # 参数配置
    st.sidebar.header("⚙️ 报告参数")

    with st.sidebar.expander("📐 物理参数", expanded=True):
        domain_length = st.number_input("计算域长度 [m]", 100.0, 5000.0, 1000.0, 100.0)
        nx = st.number_input("网格数量", 10, 5000, 100, 10)
        x_dam = st.slider("大坝位置 [m]", 0.0, domain_length, domain_length / 2, 10.0)
        h_l = st.number_input("左侧水深 h_l [m]", 0.001, 100.0, 10.0, 0.1)
        h_r = st.number_input("右侧水深 h_r [m]", 0.001, 100.0, 1.0, 0.1)

    with st.sidebar.expander("⏱️ 时间参数", expanded=True):
        t_end = st.number_input("结束时间 [s]", 0.01, 200.0, 50.0, 1.0)
        cfl = st.number_input("CFL", 0.01, 1.0, 0.9, 0.05)

    # 方案选择
    st.sidebar.divider()
    available_schemes = [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Godunov",
        "HLL",
        "MUSCL-Hancock"
    ]
    selected_schemes = st.sidebar.multiselect("选择计算方案", available_schemes, default=["Lax-Friedrichs"])

    # 报告配置
    st.sidebar.divider()
    st.sidebar.header("📄 报告配置")
    report_title = st.sidebar.text_input("报告标题", "CFD-Class 模拟分析报告")
    include_exact = st.sidebar.checkbox("包含精确解对比", value=True)
    include_convergence = st.sidebar.checkbox("包含收敛性分析", value=False)

    # 主内容区
    st.header("📊 生成报告")

    params = {
        "domain_length": domain_length,
        "nx": nx,
        "x_dam": x_dam,
        "h_l": h_l,
        "h_r": h_r,
        "t_end": t_end,
        "cfl": cfl,
        "schemes": selected_schemes
    }

    # 参数摘要
    with st.expander("📋 参数摘要", expanded=False):
        st.json(params)

    # 生成按钮
    if st.button("📝 生成 HTML 报告", type="primary"):
        if not selected_schemes:
            st.error("❌ 请至少选择一个数值方案")
        else:
            with st.spinner("🔄 正在生成报告..."):
                try:
                    from src.core.config import DamBreakConfig
                    from src.core.schemes import get_scheme

                    config = DamBreakConfig(**params)

                    # 运行模拟
                    results = {}
                    for scheme_name in selected_schemes:
                        scheme = get_scheme(scheme_name)
                        result = scheme.evolve(config)
                        results[scheme_name] = result

                    # 生成报告
                    report_html = generate_report_html(
                        report_title, params, results, config,
                        include_exact=include_exact,
                        include_convergence=include_convergence
                    )

                    st.success("✅ 报告生成完成！")

                    # 显示报告预览
                    st.subheader("📄 报告预览")
                    st.components.v1.html(report_html, height=600, scrolling=True)

                    # 下载按钮
                    st.download_button(
                        label="⬇️ 下载 HTML 报告",
                        data=report_html,
                        file_name=f"CFD_Class_Report_{np.datetime64('now')}.html",
                        mime="text/html"
                    )

                except ImportError as e:
                    st.error(f"❌ 核心模块未实现: {e}")
                    st.info("💡 请先完成后端开发")

    else:
        st.info("👈 配置参数后点击「生成 HTML 报告」")


def generate_report_html(
    title: str,
    params: Dict[str, Any],
    results: Dict,
    config: Any,
    include_exact: bool = True,
    include_convergence: bool = False
) -> str:
    """生成 HTML 报告

    Args:
        title: 报告标题
        params: 参数字典
        results: 模拟结果
        config: 配置对象
        include_exact: 是否包含精确解
        include_convergence: 是否包含收敛性分析

    Returns:
        str: HTML 报告内容
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .summary {{ background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p><strong>生成时间:</strong> {np.datetime64('now')}</p>
        
        <h2>📋 参数配置</h2>
        <div class="summary">
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>计算域长度</td><td>{params['domain_length']} m</td></tr>
                <tr><td>网格数量</td><td>{params['nx']}</td></tr>
                <tr><td>大坝位置</td><td>{params['x_dam']} m</td></tr>
                <tr><td>左侧水深</td><td>{params['h_l']} m</td></tr>
                <tr><td>右侧水深</td><td>{params['h_r']} m</td></tr>
                <tr><td>结束时间</td><td>{params['t_end']} s</td></tr>
                <tr><td>CFL</td><td>{params['cfl']}</td></tr>
            </table>
        </div>
        
        <h2>📊 模拟结果</h2>
        <table>
            <tr><th>数值方案</th><th>状态</th></tr>
    """

    for scheme_name, result in results.items():
        status = "✅ 成功" if result else "❌ 失败"
        html += f"<tr><td>{scheme_name}</td><td>{status}</td></tr>"

    html += """
        </table>
        
        <h2>📈 结果分析</h2>
        <p>模拟结果分析将在后续版本中完善。</p>
        
        <div class="footer">
            <p>Generated by CFD-Class | 符合GB/T国标的教学软件</p>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    main()
