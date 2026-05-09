"""
CFD-Class 主应用入口

一维溃坝CFD教学软件主界面
- 提供多页面导航
- 展示系统概览和快速链接
"""

import streamlit as st
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="CFD-Class | 一维溃坝CFD教学软件",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 路径配置
BASE_DIR = Path(__file__).parent.parent
PAGES_DIR = BASE_DIR / "pages"


def main():
    """主应用入口"""

    # 标题和欢迎信息
    st.title("🌊 CFD-Class: 一维溃坝CFD教学软件")
    st.markdown("### 符合GB/T国标的计算流体动力学教学平台")
    st.divider()

    # 项目信息
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="数值格式",
            value="6种",
            delta="FVM格式对比"
        )

    with col2:
        st.metric(
            label="精度阶数",
            value="1-2阶",
            delta="TVD稳定性"
        )

    with col3:
        st.metric(
            label="适用场景",
            value="教学演示",
            delta="科研分析"
        )

    with col4:
        st.metric(
            label="输出格式",
            value="HTML",
            delta="图表+动画"
        )

    st.divider()

    # 功能模块介绍
    st.header("🎯 功能模块")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📊 模拟运行
        - 参数化输入面板
        - 物理参数配置（h_L, h_R, L, t_end等）
        - 格式选择器（6种FVM格式）
        - 实时计算和误差统计

        ### 🎬 动画演示
        - 时间演化过程可视化
        - 六格式对比动画
        - 参数扫描动画生成
        - GIF导出功能
        """)

    with col2:
        st.markdown("""
        ### 📝 报告生成
        - 一键HTML报告导出
        - 收敛性分析图表
        - 敏感性矩阵计算
        - 学术规范格式

        ### 🏠 理论背景
        - 浅水方程推导
        - 波系结构图解
        - TVD概念讲解
        - 文献引用列表
        """)

    st.divider()

    # 快速开始指南
    st.header("🚀 快速开始")

    with st.expander("📖 使用指南", expanded=True):
        st.markdown("""
        **步骤1**: 在侧边栏选择"模拟运行"页面

        **步骤2**: 配置物理参数
        - 左侧水深 `h_L` (m)
        - 右侧水深 `h_R` (m)
        -  domain长度 `L` (m)
        - 终止时间 `t_end` (s)

        **步骤3**: 选择数值格式
        - Lax-Friedrichs (一阶，基准对比)
        - Lax-Wendroff (二阶，光滑解)
        - MacCormack (二阶，预测校正)
        - Godunov (一阶+，精确Riemann)
        - HLL (一阶+，近似Riemann)
        - MUSCL-Hancock (二阶TVD)

        **步骤4**: 点击"开始模拟"运行计算

        **步骤5**: 查看结果图表或生成报告
        """)

    # 技术栈信息
    st.header("🛠️ 技术栈")

    tech_cols = st.columns(5)

    techs = [
        ("🐍 Python 3.10+", "核心开发语言"),
        ("📊 Streamlit", "Web用户界面"),
        ("🔢 NumPy/SciPy", "数值计算"),
        ("📈 Matplotlib", "可视化绑图"),
        ("🧪 pytest", "单元测试框架")
    ]

    for idx, (tech, desc) in enumerate(techs):
        with tech_cols[idx]:
            st.markdown(f"**{tech}**")
            st.caption(desc)

    st.divider()

    # 关于信息
    st.header("ℹ️ 关于项目")

    with st.expander("项目信息", expanded=False):
        st.markdown("""
        **CFD-Class** 是一款面向具有流体力学基础知识的学生的一维溃坝问题研究演示教学软件。

        **核心价值**:
        - 🎓 教学导向: 从物理背景到数值实现的全链路学习体验
        - 🔬 格式对比: 6种经典FVM格式的性能与精度对比分析
        - 🎮 交互探索: 参数化输入 + 实时可视化 + 动画演示
        - 📊 自动报告: 一键生成符合学术规范的HTML分析报告

        **符合标准**:
        - GB/T 8567-2006 计算机软件文档编制规范
        - GB/T 9385-2008 计算机软件需求规格说明
        - GB/T 9386-2008 计算机软件测试文档编制规范

        **版本**: v0.1.0-alpha (初始化阶段)

        **团队**: CFD-Team (6人团队)
        - 项目经理: @PM
        - 架构师: @Arch
        - 后端开发: @BE
        - 前端开发: @FE
        - 测试工程师: @QA
        - 文档工程师: @TW
        """)

    # 页脚
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Made with ❤️ by CFD-Team | 符合GB/T国标的教学软件 | "
        "<a href='https://github.com/kaklos-cyber/cfd_class' target='_blank'>GitHub</a>"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
