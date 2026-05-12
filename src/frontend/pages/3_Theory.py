"""
理论背景页面

浅水方程、激波管理论、TVD概念讲解
"""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="理论背景 | CFD-Class", page_icon="🏠", layout="wide")


def display_swe_derivation():
    """显示浅水方程推导"""
    st.header("🌊 浅水方程推导")

    with st.expander("📐 控制方程", expanded=True):
        st.markdown("""
        ### 一维浅水方程（Saint-Venant方程）

        质量守恒方程（连续方程）:
        $$\\frac{\\partial h}{\\partial t} + \\frac{\\partial (hu)}{\\partial x} = 0$$

        动量守恒方程:
        $$\\frac{\\partial (hu)}{\\partial t} + \\frac{\\partial (hu^2 + \\frac{1}{2}gh^2)}{\\partial x} = 0$$

        其中:
        - $h$: 水深 (m)
        - $u$: 流速 (m/s)
        - $g$: 重力加速度 (m/s²)
        - $x$: 空间坐标 (m)
        - $t$: 时间 (s)
        """)

    with st.expander("📝 守恒形式 vs 非守恒形式", expanded=False):
        st.markdown("""
        ### 守恒形式

        使用守恒变量 $\\mathbf{U} = [h, hu]^T$:

        $$\\frac{\\partial \\mathbf{U}}{\\partial t} + \\frac{\\partial \\mathbf{F}(\\mathbf{U})}{\\partial x} = 0$$

        其中通量 $\\mathbf{F}(\\mathbf{U}) = [hu, hu^2 + \\frac{1}{2}gh^2]^T$

        ### 优势

        - 正确捕捉激波和间断
        - 质量、动量守恒
        - 适用于有限体积法
        """)


def display_wave_structure():
    """显示波系结构"""
    st.header("🌊 波系结构")

    st.markdown("""
    ### 一维溃坝问题的波系结构

    溃坝会产生三种基本波：
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 1️⃣ 左行稀疏波 (Left Rarefaction)

        **特征**:
        - 向左传播
        - 水位逐渐降低
        - 速度逐渐减小

        **物理意义**:
        左侧水体向左流动，形成平坦的水面
        """)

    with col2:
        st.markdown("""
        #### 2️⃣ 接触间断 (Contact Discontinuity)

        **特征**:
        - 不传播（相对于流体）
        - 速度相同
        - 水深可能有突变

        **物理意义**:
        不同水深流体的分界面
        """)

    with col3:
        st.markdown("""
        #### 3️⃣ 右行激波 (Right Shock)

        **特征**:
        - 向右传播
        - 水位突然跃升
        - 熵增（非可逆）

        **物理意义**:
        水流的突变界面
        """)

    with st.expander("📊 波系示意图", expanded=False):
        st.info("💡 波系示意图开发中...")
        st.markdown("""
        ```
        左行稀疏波 ← |←←←←←←←←←←←←|
        接触间断    |________________|
        右行激波    |→→→→→→→→→→→→→|
        ```

        **x-t 图**:

        ```
        t
        ↑
        |     /        ________
        |    /    ____/
        |   /____/
        |  /
        | /
        +——————————————→ x
        ```
        """)


def display_riemann_solver():
    """显示Riemann求解器"""
    st.header("🧮 Riemann问题求解")

    st.markdown("""
    ### 激波管问题 (Riemann Problem)

    初始条件:
    $$h(x, 0) = \\begin{cases} h_L & x < x_{dam} \\\\ h_R & x > x_{dam} \\end{cases}$$
    $$u(x, 0) = \\begin{cases} u_L & x < x_{dam} \\\\ u_R & x > x_{dam} \\end{cases}$$
    """)

    with st.expander("📐 Exact Riemann Solver", expanded=False):
        st.markdown("""
        ### 精确Riemann解法

        **Rankine-Hugoniot条件**:

        $$s = \\frac{[F]}{[U]} = \\frac{F_R - F_L}{U_R - U_L}$$

        **波速关系**:

        - 稀疏波左边界速度: $a_L - 2c_L$
        - 稀疏波右边界速度: $a_R + 2c_R$
        - 激波速度: $s = \\frac{u_R c_R - u_L c_L}{c_R - c_L}$

        其中声速 $c = \\sqrt{gh}$
        """)

    with st.expander("📐 HLL Approximate Solver", expanded=False):
        st.markdown("""
        ### HLL近似求解器

        **Harten-Lax-van Leer (HLL) 近似**:

        $$\\mathbf{U}(x,t) = \\begin{cases} \\mathbf{U}_L & \\frac{x}{t} < s_L \\\\ \\mathbf{U}_* & s_L < \\frac{x}{t} < s_R \\\\ \\mathbf{U}_R & \\frac{x}{t} > s_R \\end{cases}$$

        **波速估计**:

        $$s_L = \\min(u_L - c_L, u_R - c_R)$$
        $$s_R = \\max(u_L + c_L, u_R + c_R)$$

        **优点**: 计算简单，稳定
        **缺点**: 忽略中间状态细节
        """)


def display_fvm_schemes():
    """显示FVM格式"""
    st.header("📐 有限体积格式")

    schemes = {
        "Lax-Friedrichs": {
            "formula": "U_i^{n+1} = \\frac{1}{2}(U_L + U_R) - \\frac{\\Delta t}{2\\Delta x}(F_R - F_L)",
            "features": ["一阶精度", "强稳定性", "强数值扩散"],
            "application": "基准格式、教学演示",
        },
        "Lax-Wendroff": {
            "formula": "U_i^{n+1} = U_i^n - \\frac{\\Delta t}{\\Delta x}(F_i - F_{i-1}) + \\frac{1}{2}\\frac{\\Delta t^2}{\\Delta x^2}\\frac{\\partial F}{\\partial U}(F_i - F_{i-1})",
            "features": ["二阶精度", "高精度光滑解", "激波震荡"],
            "application": "光滑解测试",
        },
        "Godunov": {
            "formula": "逐单元Riemann问题求解",
            "features": ["一阶+精度", "精确激波捕捉", "计算量大"],
            "application": "高精度基准",
        },
        "MUSCL-Hancock": {
            "formula": "预测-校正 + TVD限制器",
            "features": ["二阶TVD", "高精度高稳定性", "激波平滑"],
            "application": "推荐工程应用",
        },
    }

    for name, info in schemes.items():
        with st.expander(f"📐 {name}", expanded=False):
            st.markdown(f"**公式**: ${info['formula']}$")
            st.markdown(f"**特点**: {', '.join(info['features'])}")
            st.markdown(f"**应用**: {info['application']}")


def display_tvd_concept():
    """显示TVD概念"""
    st.header("🛡️ TVD (Total Variation Diminishing) 概念")

    with st.expander("📐 定义", expanded=True):
        st.markdown("""
        ### TVD 条件

        对于任意时间步 $n$ 和 $n+1$:

        $$TV(U^{n+1}) \\leq TV(U^n)$$

        其中总变差 (Total Variation):

        $$TV(U) = \\sum_{i=1}^{N-1} |U_{i+1} - U_i|$$
        """)

    with st.expander("📐 物理意义", expanded=False):
        st.markdown("""
        ### 为什么需要TVD？

        **非TVD格式的问题**:

        - Lax-Wendroff: 高精度但激波处有震荡
        - MacCormack: 预测校正但可能不稳定

        **TVD格式的优势**:

        - 抑制激波处的非物理震荡
        - 保持解的单调性
        - 稳定性和高精度兼顾

        **常用限制器**:

        | 限制器 | 公式 | 特点 |
        |--------|------|------|
        | MinMod | $\\phi(\\theta) = \\max(0, \\min(1, \\theta))$ | 最强限制 |
        | Van Leer | $\\phi(\\theta) = \\frac{|\theta| + \\theta}{1 + \\theta}$ | 平滑限制 |
        | Superbee | $\\phi(\\theta) = \\max(0, \\min(2\\theta, 1), \\min(\\theta, 2))$ | 最强保真 |
        """)


def display_references():
    """显示参考文献"""
    st.header("📚 参考文献")

    references = [
        {
            "title": "TVD Schemes for Hyperbolic Conservation Laws",
            "author": "Harten, A.",
            "year": "1983",
            "journal": "Journal of Computational Physics",
            "volume": "49",
            "pages": "357-393",
        },
        {
            "title": "Towards the Ultimate Conservative Difference Scheme",
            "author": "Van Leer, B.",
            "year": "1974",
            "journal": "Journal of Computational Physics",
            "volume": "14",
            "pages": "361-370",
        },
        {
            "title": "On the Different Formulations of the Consolidation Equations of Shallow Water Theory",
            "author": "Stoker, J.J.",
            "year": "1957",
            "journal": "Commun. Pure Appl. Math.",
            "volume": "10",
            "pages": "567-581",
        },
    ]

    for idx, ref in enumerate(references, 1):
        st.markdown(f"""
        **{idx}. {ref['title']}**

        {ref['author']}

        *{ref['journal']}*, {ref['year']}, *{ref['volume']}*, {ref['pages']}
        """)


def main():
    """理论背景页面主函数"""

    st.title("🏠 理论背景")
    st.markdown("学习一维溃坝问题的物理基础和数值方法")

    menu = st.sidebar.radio(
        "📚 选择内容",
        [
            "浅水方程",
            "波系结构",
            "Riemann求解器",
            "有限体积格式",
            "TVD概念",
            "参考文献",
        ],
        index=0,
    )

    if menu == "浅水方程":
        display_swe_derivation()

    elif menu == "波系结构":
        display_wave_structure()

    elif menu == "Riemann求解器":
        display_riemann_solver()

    elif menu == "有限体积格式":
        display_fvm_schemes()

    elif menu == "TVD概念":
        display_tvd_concept()

    elif menu == "参考文献":
        display_references()

    st.divider()

    with st.expander("ℹ️ 学习建议", expanded=False):
        st.markdown("""
        **推荐学习路径**:

        1. **理解物理**: 先学习浅水方程和波系结构
        2. **掌握理论**: 学习Riemann问题和求解器
        3. **理解数值**: 掌握有限体积法和TVD概念
        4. **实践应用**: 使用本软件对比不同格式的表现

        **进一步学习**:

        - 阅读文献中的参考文献
        - 尝试不同的参数配置
        - 对比不同格式在各种场景下的表现
        """)


if __name__ == "__main__":
    main()
