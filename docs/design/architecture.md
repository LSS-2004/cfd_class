# 架构设计详细文档

> **文档编号**: CFD-CLASS-ARCH-001
> **版本**: v1.0
> **日期**: 2026-05-09
> **状态**: 正式版
> **依据标准**: GB/T 8567-2006 计算机软件文档编制规范

---

## 文档控制信息

| 项目 | 内容 |
|------|------|
| **软件名称** | CFD-Class 一维溃坝CFD教学软件 |
| **文档作者** | @Arch (架构师) |
| **审核人** | @PM (项目经理) |
| **批准人** | @PM (项目经理) |
| **分发范围** | 全体开发团队成员 |

---

## 1. 引言

### 1.1 编写目的

本文档为 CFD-Class 软件的架构设计详细文档，旨在从系统全局视角阐述软件的整体架构、分层设计、模块划分、数据流、接口定义、部署方式及关键技术决策。本文档面向开发团队（@BE、@FE、@QA）、测试人员及未来维护者，作为编码实现、系统集成与验收的技术依据。

### 1.2 范围

本文档覆盖 CFD-Class 软件的全部技术架构内容，包括：
- 系统整体架构与分层设计
- Core 层、Frontend 层、Utils 层的详细模块结构
- 数据流设计与接口定义
- 本地与 Docker 部署架构
- 关键技术决策与性能优化策略

### 1.3 参考资料

1. GB/T 8567-2006 计算机软件文档编制规范
2. GB/T 9385-2008 计算机软件需求规格说明
3. SRS.md — 软件需求规格说明书
4. SDD.md — 概要设计说明书
5. Toro, E.F. "Riemann Solvers and Numerical Methods for Fluid Dynamics", Springer, 2009
6. LeVeque, R.J. "Finite Volume Methods for Hyperbolic Problems", Cambridge, 2002

---

## 2. 架构概述

### 2.1 设计原则

CFD-Class 在架构设计中遵循以下软件工程原则：

| 原则 | 说明 | 在本项目中的体现 |
|------|------|----------------|
| **SOLID** | 单一职责、开闭原则、里氏替换、接口隔离、依赖倒置 | `BaseScheme` 抽象基类定义统一接口，六种格式各自独立实现；`SimulationEngine` 依赖抽象而非具体格式 |
| **DRY** | 不要重复自己 | 边界条件处理、时间步长计算、正性保持等逻辑封装在基类公共方法中 |
| **KISS** | 保持简单直接 | 一维问题天然简化，不引入不必要的多维抽象；Streamlit 降低前端复杂度 |
| **YAGNI** | 你不会需要它 | 暂不支持二维/三维扩展，聚焦一维溃坝教学场景 |
| **关注点分离** | 不同职责分层处理 | 数值计算（Core）、业务编排（Engines）、界面渲染（Frontend）严格分层 |

### 2.2 架构模式说明

本项目采用 **MVC（Model-View-Controller）分层架构**，并针对教学软件的特点进行适应性调整：

- **Model（模型层）**：对应 `src/core/` 目录，负责全部数值计算与物理建模，包括有限体积格式实现、Riemann 求解器、误差分析工具。该层无 UI 依赖，可独立运行与测试。
- **View（视图层）**：对应 `src/frontend/pages/` 与 `components/`，基于 Streamlit 构建 Web 界面，负责参数输入、结果可视化、动画展示。该层不包含业务计算逻辑。
- **Controller（控制层）**：对应 `src/frontend/engines/`，作为 Model 与 View 之间的协调器，负责接收 View 层的用户输入，调用 Model 层完成计算，并将结果转换为 View 层可直接渲染的数据结构。

MVC 模式的优势在于：
1. **教学场景适配**：教师或学生可独立替换 Core 层的数值格式，无需修改前端代码
2. **测试友好**：Core 层可脱离 Streamlit 环境进行单元测试与收敛性验证
3. **并行开发**：@BE 专注算法实现，@FE 专注界面交互，两者通过 `SimulationResult` 等标准数据结构解耦

### 2.3 技术栈选型理由

| 类别 | 技术 | 选型理由 |
|------|------|---------|
| 开发语言 | Python 3.10+ | 生态丰富，NumPy/SciPy 科学计算栈成熟；语法简洁，适合教学代码阅读；团队技术储备统一 |
| 前端框架 | Streamlit | 纯 Python 编写 UI，无需 JavaScript/CSS 技能；与数据科学工作流无缝集成；适合快速构建参数化交互界面 |
| 数值计算 | NumPy + SciPy | 向量化运算性能优异；`ndarray` 是科学计算事实标准；SciPy 提供优化与插值工具 |
| 可视化 | Matplotlib | 与 NumPy 深度集成；支持静态图、动画帧、高质量学术绑图；可导出 PNG/PDF/GIF |
| 测试框架 | pytest | 简洁的断言语法；支持参数化测试（适合六种格式的统一测试）；覆盖率插件成熟 |
| 代码质量 | Black + isort + flake8 + mypy | 强制统一代码风格；静态类型检查减少运行时错误 |
| 报告生成 | Jinja2 + MathJax | Jinja2 模板引擎生成 HTML；MathJax 离线渲染 LaTeX 公式 |
| 动画处理 | Pillow | 图像序列合成 GIF；轻量无额外依赖 |

---

## 3. 系统架构图

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              用户 (Browser)                              │
│                    Chrome / Firefox / Edge / Safari                      │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │ HTTP (WebSocket)
┌─────────────────────────────▼───────────────────────────────────────────┐
│                         Streamlit Server                                 │
│                    (streamlit run src/frontend/app.py)                   │
│                         端口: 8501 (默认)                                 │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼─────┐        ┌──────▼──────┐       ┌──────▼──────┐
   │   View   │        │ Controller  │       │    View     │
   │  Layer   │◄──────►│   Layer     │◄─────►│   Layer     │
   │(pages/ + │        │ (engines/)  │       │(components/ │
   │components│        │             │       │ + assets/)  │
   └────┬─────┘        └──────┬──────┘       └──────┬──────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                          Model Layer (Core)                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │   schemes/  │  │   solvers/   │  │  analysis/  │  │   config.py  │  │
│  │ 6种FVM格式   │  │Riemann求解器 │  │ 误差分析工具 │  │ 配置数据类   │  │
│  │             │  │             │  │             │  │              │  │
│  │•LF Scheme   │  │•Exact Solver│  │•L1/L2/L∞   │  │•参数校验     │  │
│  │•LW Scheme   │  │•HLL Flux   │  │•收敛阶估计  │  │•不可变性保证 │  │
│  │•MC Scheme   │  │             │  │             │  │              │  │
│  │•Godunov     │  │             │  │             │  │              │  │
│  │•HLL         │  │             │  │             │  │              │  │
│  │•MUSCL-Hancock│ │             │  │             │  │              │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                         Utils Layer (公共层)                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐                     │
│  │  constants  │  │  exceptions  │  │   helpers   │                     │
│  │  (物理常量)  │  │ (自定义异常)  │  │  (通用函数)  │                     │
│  └─────────────┘  └──────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 模块依赖关系

```
                        ┌─────────────┐
                        │   Browser   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │  Streamlit  │
                        │    Server   │
                        └──────┬──────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
        │   pages/  │   │components/│   │  engines/ │
        │  (视图层)  │◄──┤  (视图层)  │◄──┤ (控制层)  │
        └───────────┘   └───────────┘   └─────┬─────┘
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        │                     │                     │
                  ┌─────▼─────┐         ┌─────▼─────┐         ┌─────▼─────┐
                  │  schemes/ │         │  solvers/ │         │ analysis/ │
                  │ (模型层)  │         │ (模型层)  │         │ (模型层)  │
                  └─────┬─────┘         └───────────┘         └───────────┘
                        │
                        ▼
                  ┌───────────┐
                  │  config   │
                  │ (配置类)   │
                  └───────────┘
                        ▲
                        │
                  ┌───────────┐
                  │   utils/  │
                  │ (公共层)   │
                  └───────────┘
```

---

## 4. 模块详细架构

### 4.1 Core 层（模型层）

Core 层是 CFD-Class 的计算核心，负责全部数值求解与物理分析。该层设计目标为：**零外部 UI 依赖、高内聚、可独立测试**。

#### 4.1.1 目录结构

```
src/core/
├── __init__.py
├── config.py                 # DamBreakConfig frozen dataclass
├── exceptions.py             # CFDError 异常体系
├── schemes/
│   ├── __init__.py
│   ├── base_scheme.py        # BaseScheme 抽象基类
│   ├── lax_friedrichs.py     # Lax-Friedrichs 格式
│   ├── lax_wendroff.py       # Lax-Wendroff 格式
│   ├── maccormack.py         # MacCormack 格式
│   ├── godunov.py            # Godunov 格式
│   ├── hll.py                # HLL 格式
│   └── muscl_hancock.py      # MUSCL-Hancock 格式
├── solvers/
│   ├── __init__.py
│   └── riemann_solver.py     # 精确/HLL Riemann 求解器
└── analysis/
    ├── __init__.py
    └── error_analysis.py     # 误差度量与收敛阶估计
```

#### 4.1.2 类图与交互关系

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Core Layer                                  │
│                                                                         │
│  ┌─────────────────────┐                                                │
│  │  <<abstract>>       │                                                │
│  │   BaseScheme        │◄────────────────────────────────────────┐      │
│  │─────────────────────│                                         │      │
│  │ + name: str         │                                         │      │
│  │ + order: int        │                                         │      │
│  │ + tvd: bool         │                                         │      │
│  │─────────────────────│                                         │      │
│  │ + evolve(U0, config)│                                         │      │
│  │   → Dict[t, U]      │                                         │      │
│  │ # _compute_dt()     │                                         │      │
│  │ # _apply_bc()       │                                         │      │
│  └─────────────────────┘                                         │      │
│           ▲                                                      │      │
│           │ implements                                           │      │
│    ┌──────┼──────┬────────┬──────────┬──────────┐              │      │
│    │      │      │        │          │          │              │      │
│ ┌──┴──┐┌──┴──┐┌─┴────┐┌──┴────┐┌───┴────┐┌───┴──────┐       │      │
│ │  LF ││  LW ││  MC  ││Godunov││  HLL   ││MUSCL-Hanc│       │      │
│ │Scheme││Scheme││Scheme││ Scheme││ Scheme ││  ock     │       │      │
│ └─────┘└─────┘└──────┘└───────┘└────────┘└──────────┘       │      │
│                                                               │      │
│  ┌─────────────────────┐      ┌─────────────────────────┐    │      │
│  │  DamBreakConfig     │      │   SimulationResult      │    │      │
│  │  (frozen dataclass) │      │   (dataclass)           │    │      │
│  │─────────────────────│      │─────────────────────────│    │      │
│  │ h_L, h_R, u_L, u_R  │      │ config: DamBreakConfig  │────┘      │
│  │ g, cfl, nx, t_end   │      │ scheme_name: str        │           │
│  │ x_min, x_max        │      │ time_history: Dict      │           │
│  │─────────────────────│      │ exact_solution: NDArray │           │
│  │ + dx (property)     │      │ errors: Dict[str,float] │           │
│  │ + x_grid (property) │      │ execution_time: float   │           │
│  │ + __post_init__()   │      │ mass_conservation_error │           │
│  └─────────────────────┘      └─────────────────────────┘           │
│                                                                         │
│  ┌─────────────────────┐      ┌─────────────────────────┐              │
│  │  riemann_solver.py  │      │   error_analysis.py     │              │
│  │─────────────────────│      │─────────────────────────│              │
│  │ exact_riemann_sol() │      │ compute_error()         │              │
│  │ hll_flux()          │      │ estimate_order()        │              │
│  └─────────────────────┘      └─────────────────────────┘              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 4.1.3 BaseScheme 设计说明

`BaseScheme` 是所有有限体积格式的抽象基类，采用 **模板方法模式** 设计：

- **公共算法骨架**：`_compute_dt()`（CFL 时间步长）、`_apply_bc()`（透射边界条件）在基类中实现，所有子类复用
- **可变算法步骤**：`evolve()` 为抽象方法，各子类根据自身数值格式实现时间推进逻辑
- **正性保持**：基类提供 `EPS_H = 1e-12` 阈值，子类在更新水深后调用 `np.maximum(h, EPS_H)` 防止负值

#### 4.1.4 六种格式特性对比

| 格式类 | 继承关系 | 核心算法 | 时间推进方式 |
|--------|---------|---------|-------------|
| `LaxFriedrichsScheme` | `BaseScheme` | 中心差分 + 数值粘性通量 | 单步显式 |
| `LaxWendroffScheme` | `BaseScheme` | Taylor 展开两步法 | 预测-校正 |
| `MacCormackScheme` | `BaseScheme` | 预测-校正两步法 | 预测步 + 校正步 |
| `GodunovScheme` | `BaseScheme` | 精确 Riemann 求解器 | 单步 Godunov 通量 |
| `HLLOneScheme` | `BaseScheme` | HLL 两波近似通量 | 单步 HLL 通量 |
| `MUSCLHancockScheme` | `BaseScheme` | MUSCL 重构 + minmod 限制器 + Hancock 预测 | 重构 → 预测 → 校正 |

#### 4.1.5 Riemann 求解器设计

Riemann 求解器模块采用 **策略模式** 设计：

- `exact_riemann_solution(U_L, U_R, g)`：精确求解器，支持湿底与干底两种工况，内部使用 Newton-Raphson 迭代求解非线性星区方程
- `hll_flux(U_L, U_R, g)`：近似求解器，两波近似公式计算数值通量，作为精确求解器的快速替代

Godunov 格式依赖精确求解器；HLL 格式依赖近似求解器；其余格式不直接依赖 Riemann 求解器。

### 4.2 Frontend 层（视图层 + 控制层）

Frontend 层负责用户交互与结果展示，分为 Pages、Components、Engines 三个子层。

#### 4.2.1 目录结构

```
src/frontend/
├── __init__.py
├── app.py                    # 应用主入口，页面路由
├── pages/
│   ├── __init__.py
│   ├── home.py               # 首页：理论背景
│   ├── simulation.py         # 模拟页：参数运行
│   ├── animation.py          # 动画页：动态可视化
│   └── report.py             # 报告页：对比分析
├── components/
│   ├── __init__.py
│   ├── param_panel.py        # 参数输入面板
│   ├── scheme_selector.py    # 格式多选组件
│   ├── result_viewer.py      # 结果展示组件
│   └── progress_bar.py       # 进度条组件
└── engines/
    ├── __init__.py
    ├── simulation_engine.py  # 模拟业务引擎
    ├── animation_engine.py   # 动画生成引擎
    └── report_generator.py   # 报告生成引擎
```

#### 4.2.2 Pages 层

每个页面模块导出统一的 `render()` 函数接口，由 `app.py` 根据侧边栏导航动态导入：

```python
# 统一页面接口
def render() -> None:
    """渲染页面内容."""
    pass
```

| 页面 | 职责 | 依赖的 Components | 依赖的 Engines |
|------|------|------------------|---------------|
| `home.py` | 理论背景展示、学习路径引导 | 无 | 无 |
| `simulation.py` | 参数配置、格式选择、运行控制、结果展示 | `param_panel`, `scheme_selector`, `result_viewer`, `progress_bar` | `simulation_engine` |
| `animation.py` | 动画参数设置、GIF 生成与预览 | `param_panel`, `progress_bar` | `animation_engine` |
| `report.py` | 报告配置、HTML 生成与下载 | `param_panel`, `scheme_selector` | `report_generator` |

#### 4.2.3 Components 层

Components 层封装可复用的 UI 交互单元，每个组件接受标准数据类型作为输入/输出，避免与 Streamlit session state 过度耦合：

| 组件 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `param_panel.render()` | 无 | `DamBreakConfig` | 返回 frozen 配置对象，确保不可变性 |
| `scheme_selector.render()` | 无 | `List[str]` | 返回选中的格式名称列表 |
| `result_viewer.display(results)` | `List[SimulationResult]` | 无 | 渲染对比图、误差表格 |
| `progress_bar.track(callback)` | `Callable` | 无 | 将 Core 层的进度回调绑定到 Streamlit 进度条 |

#### 4.2.4 Engines 层

Engines 层是 Frontend 与 Core 之间的 **适配器层**，承担以下职责：

1. **数据转换**：将用户界面输入转换为 `DamBreakConfig` 等 Core 层数据结构
2. **计算编排**：根据用户选择的格式列表，循环调用对应的 `BaseScheme` 子类
3. **结果封装**：将 Core 层返回的原始数组封装为 `SimulationResult` 标准结果对象
4. **异常转换**：将 Core 层的数值异常转换为友好的前端提示信息

| 引擎 | 核心方法 | 调用链 |
|------|---------|--------|
| `SimulationEngine` | `run(config, schemes) → List[SimulationResult]` | 遍历 schemes → 实例化 Scheme → 调用 `evolve()` → 封装结果 |
| `AnimationEngine` | `generate_gif(results, fps) → bytes` | 提取 `time_history` → Matplotlib 绑帧 → Pillow 合成 GIF |
| `ReportGenerator` | `generate_html(results, template) → str` | Jinja2 模板渲染 → 嵌入图表 Base64 → 输出完整 HTML |

### 4.3 Utils 层（公共层）

Utils 层提供跨层共享的公共工具，遵循 **底层不依赖上层** 原则：

```
src/utils/
├── __init__.py
├── constants.py              # 物理常量与数值阈值
├── exceptions.py             # 异常类层次结构
└── helpers.py                # 通用辅助函数
```

| 模块 | 内容 | 使用方 |
|------|------|--------|
| `constants.py` | `EPS_H = 1e-12`, `G_DEFAULT = 9.81` | Core 层（正性保持）、Frontend 层（默认值） |
| `exceptions.py` | `CFDError`, `ConfigValidationError`, `NumericalInstabilityError`, `ConvergenceError`, `PositiveDepthViolation` | Core 层（抛出）、Engines 层（捕获转换） |
| `helpers.py` | 数组校验、文件路径处理、时间格式化 | 全层 |

---

## 5. 数据流设计

### 5.1 从用户输入到结果展示的完整数据流

```
┌─────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────┐
│  用户    │────►│  Streamlit UI   │────►│   Components    │────►│   Engines   │
│ 操作输入 │     │ (pages/*.py)    │     │ (components/)   │     │  (engines/)  │
└─────────┘     └─────────────────┘     └─────────────────┘     └──────┬──────┘
                                                                       │
                              ┌────────────────────────────────────────┘
                              │  1. 创建 DamBreakConfig
                              │  2. 根据 scheme 名称映射到类
                              │  3. 实例化 Scheme 对象
                              ▼
                        ┌─────────────┐
                        │  Core Layer │
                        │  (core/)    │
                        └──────┬──────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        ┌─────▼─────┐    ┌─────▼─────┐   ┌─────▼─────┐
        │  schemes/ │    │  solvers/ │   │  analysis/│
        │  evolve() │    │  exact/   │   │  compute  │
        │           │    │  hll_flux │   │  _error() │
        └─────┬─────┘    └───────────┘   └───────────┘
              │
              │ 返回 Dict[float, NDArray]
              │
              ▼
        ┌─────────────┐
        │   Engines   │
        │  封装为      │
        │ Simulation  │
        │  Result     │
        └──────┬──────┘
               │
               │ 返回 List[SimulationResult]
               │
               ▼
        ┌─────────────┐
        │ Components  │
        │ result_     │
        │ viewer.     │
        │ display()   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  Streamlit  │
        │   渲染输出   │
        │ (图表/表格)  │
        └─────────────┘
```

### 5.2 数据流阶段说明

| 阶段 | 数据载体 | 处理说明 |
|------|---------|---------|
| **输入采集** | `Dict[str, Union[float, int]]` | Streamlit widget 返回原始值，Components 层进行类型转换与范围校验 |
| **配置构建** | `DamBreakConfig` | `param_panel` 将原始输入封装为 frozen dataclass，触发 `__post_init__` 合法性校验 |
| **格式分发** | `List[Type[BaseScheme]]` | `simulation_engine` 维护 `SCHEME_REGISTRY` 字典，根据名称字符串映射到类 |
| **计算执行** | `NDArray[np.float64]` | Core 层以 `ndarray` 进行向量化运算，时间推进过程中通过回调函数报告进度 |
| **结果封装** | `SimulationResult` | Engines 层将原始数组、配置、误差、执行时间等封装为标准结果对象 |
| **可视化渲染** | `matplotlib.figure.Figure` | Components 层调用 Matplotlib 绑图，Streamlit 通过 `st.pyplot()` 渲染 |

### 5.3 关键数据结构流转

```
用户输入 (UI Widgets)
    │
    ▼
┌─────────────────────────────────────────┐
│ DamBreakConfig (frozen dataclass)       │
│ ├── 物理参数: h_L, h_R, u_L, u_R, g     │
│ ├── 数值参数: cfl, nx, t_end            │
│ └── 域参数:  x_min, x_max               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ U0: NDArray[float64], shape=(2, nx)     │
│ ├── U0[0, :] = h (水深)                  │
│ └── U0[1, :] = hu (动量密度)              │
└─────────────────────────────────────────┘
    │
    ▼ (evolve 循环)
┌─────────────────────────────────────────┐
│ time_history: Dict[float, NDArray]      │
│ ├── key: 记录时刻 t                      │
│ └── value: U(2×nx) 该时刻的守恒变量       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ SimulationResult (dataclass)            │
│ ├── config: DamBreakConfig              │
│ ├── scheme_name: str                    │
│ ├── time_history: Dict[float, NDArray]  │
│ ├── exact_solution: NDArray (可选)       │
│ ├── errors: Dict[str, float] (可选)      │
│ ├── execution_time: float               │
│ └── mass_conservation_error: float      │
└─────────────────────────────────────────┘
```

---

## 6. 接口架构

### 6.1 Core → Frontend 内部 API

Core 层对外暴露以下稳定接口，Frontend 层（Engines）通过导入调用：

#### 6.1.1 配置接口

```python
# src/core/config.py
from dataclasses import dataclass
from numpy.typing import NDArray
import numpy as np

@dataclass(frozen=True)
class DamBreakConfig:
    """溃坝问题运行参数配置."""

    # 物理参数
    h_L: float = 1.0
    h_R: float = 0.0
    u_L: float = 0.0
    u_R: float = 0.0
    g: float = 9.81

    # 数值参数
    cfl: float = 0.9
    nx: int = 200
    t_end: float = 0.5

    # 域参数
    x_min: float = -5.0
    x_max: float = 5.0

    def __post_init__(self) -> None: ...

    @property
    def dx(self) -> float: ...

    @property
    def x_grid(self) -> NDArray[np.float64]: ...
```

#### 6.1.2 格式接口

```python
# src/core/schemes/base_scheme.py
from abc import ABC, abstractmethod
from typing import Dict, Callable, Optional
from numpy.typing import NDArray

class BaseScheme(ABC):
    """有限体积格式抽象基类."""

    def __init__(self, name: str, order: int, tvd: bool = False) -> None: ...

    @abstractmethod
    def evolve(
        self,
        U0: NDArray[np.float64],
        config: DamBreakConfig,
        progress_callback: Optional[Callable[[float, float], None]] = None
    ) -> Dict[float, NDArray[np.float64]]: ...

    def _compute_dt(self, U: NDArray[np.float64], config: DamBreakConfig) -> float: ...

    def _apply_bc(self, U: NDArray[np.float64]) -> NDArray[np.float64]: ...
```

#### 6.1.3 Riemann 求解器接口

```python
# src/core/solvers/riemann_solver.py
from numpy.typing import NDArray

def exact_riemann_solution(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float
) -> dict: ...

def hll_flux(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float
) -> NDArray[np.float64]: ...
```

#### 6.1.4 误差分析接口

```python
# src/core/analysis/error_analysis.py
from numpy.typing import NDArray
from typing import List

def compute_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    p: int = 2
) -> float: ...

def estimate_order(
    nx_list: List[int],
    errors: List[float]
) -> float: ...
```

### 6.2 模块间依赖关系

```
依赖方向: A ──► B 表示 A 依赖 B（A imports B）

frontend/pages/ ──────┐
                      ▼
frontend/components/ ─┬──► frontend/engines/ ──► core/schemes/
                      │                         │
                      │                         ├──► core/solvers/
                      │                         │
                      │                         ├──► core/analysis/
                      │                         │
                      │                         └──► core/config/
                      │                               ▲
                      │                               │
                      └───────────────────────────────┘
                                                    ▲
                                                    │
                                              core/utils/
                                                    ▲
                                                    │
                                              frontend/utils/
```

#### 6.2.1 依赖规则

| 规则编号 | 规则描述 | 约束强度 |
|---------|---------|---------|
| DEP-01 | Core 层不得依赖 Frontend 层 | 强制 |
| DEP-02 | Core 层不得依赖 Streamlit | 强制 |
| DEP-03 | Utils 层不得依赖 Core 层或 Frontend 层 | 强制 |
| DEP-04 | Engines 可依赖 Core 层与 Components 层 | 允许 |
| DEP-05 | Pages 可依赖 Components 层与 Engines 层 | 允许 |
| DEP-06 | Components 之间可相互依赖，但避免循环依赖 | 建议 |

---

## 7. 部署架构

### 7.1 本地运行架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户主机                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Python 3.10+ 虚拟环境                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   NumPy     │  │   SciPy     │  │  Matplotlib │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Streamlit  │  │   Pillow    │  │   Jinja2    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                      ┌─────────────────────┐        │   │
│  │                      │   CFD-Class 源码     │        │   │
│  │                      │   (src/ + docs/)     │        │   │
│  │                      └─────────────────────┘        │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼ streamlit run src/frontend/app.py
│                     ┌─────────────┐                         │
│                     │  localhost  │                         │
│                     │   :8501     │                         │
│                     └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

#### 7.1.1 本地运行步骤

```bash
# 1. 克隆仓库
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
streamlit run src/frontend/app.py
```

#### 7.1.2 本地运行特点

- **单进程模式**：Streamlit 默认以单进程运行，适合个人教学使用
- **无外部依赖**：除 Python 包外，无需数据库、缓存服务器等外部服务
- **数据不离开本地**：所有计算在本地完成，满足数据隐私需求（NFR-05.03）

### 7.2 Docker 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker 宿主机                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              cfd-class 容器                          │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  基于 python:3.11-slim 镜像                  │   │   │
│  │  │  ┌─────────────┐  ┌─────────────────────┐   │   │   │
│  │  │  │  Python     │  │   CFD-Class 应用     │   │   │   │
│  │  │  │  3.11       │  │   (src/ + docs/)     │   │   │   │
│  │  │  └─────────────┘  └─────────────────────┘   │   │   │
│  │  │  ┌─────────────┐  ┌─────────────────────┐   │   │   │
│  │  │  │  系统依赖    │  │   字体/时区配置      │   │   │   │
│  │  │  │  (gcc/etc)  │  │   (CJK/Asia)        │   │   │   │
│  │  │  └─────────────┘  └─────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                      │                              │   │
│  │                      ▼ 暴露端口 8501               │   │
│  └──────────────────────┬─────────────────────────────┘   │
│                         │                                  │
│                    ┌────┴────┐                             │
│                    │ :8501   │                             │
│                    └────┬────┘                             │
│                         │                                  │
│  ┌──────────────────────┴─────────────────────────────┐   │
│  │              浏览器访问 http://localhost:8501        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 7.2.1 Dockerfile 设计要点

```dockerfile
# 基于官方 Python 3.11 slim 镜像
FROM python:3.11-slim

# 安装系统编译依赖（NumPy/SciPy 需要）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用源码
COPY src/ ./src/
COPY docs/ ./docs/
COPY assets/ ./assets/

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 启动命令
ENTRYPOINT ["streamlit", "run", "src/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 7.2.2 Docker 运行命令

```bash
# 构建镜像
docker build -t cfd-class .

# 运行容器
docker run -p 8501:8501 cfd-class

# 后台运行（生产部署）
docker run -d -p 8501:8501 --name cfd-class-app cfd-class
```

#### 7.2.3 Docker 部署优势

- **环境一致性**：消除 "在我机器上能运行" 问题
- **快速部署**：单容器启动，无需复杂编排
- **隔离性**：计算过程与宿主机隔离，避免依赖冲突
- **可移植性**：支持任何支持 Docker 的平台（Windows/macOS/Linux）

---

## 8. 技术决策记录

### 8.1 决策 001：为什么选择 Streamlit 作为前端框架

| 项目 | 内容 |
|------|------|
| **决策日期** | 2026-05-07 |
| **决策状态** | 已采纳 |
| **决策背景** | 团队无专职前端开发人员，需要快速构建参数化交互界面；目标用户为流体力学专业学生，界面以数据可视化为主 |

**候选方案对比**：

| 方案 | 优点 | 缺点 | 评估结论 |
|------|------|------|---------|
| Streamlit | 纯 Python 开发；与 NumPy/Matplotlib 无缝集成；学习成本低；适合数据应用 | 定制化 UI 能力有限；不适合复杂多页面应用；性能不如 React/Vue | ✅ 采纳 |
| Dash (Plotly) | 交互能力更强；绑图质量高 | 需要理解回调机制；学习曲线较陡 | 备选 |
| Gradio | 极简 API；适合 ML 演示 | 布局灵活性差；社区生态较小 | 否决 |
| React + Flask | UI 完全可控；前后端分离 | 需要 JavaScript 技能；开发工作量大 | 否决 |

**决策理由**：
1. 团队技术栈统一为 Python，Streamlit 无需引入 JavaScript 技术债
2. 教学软件以参数滑块、绑图展示、表格对比为核心交互，Streamlit 原生组件完全覆盖
3. 开发效率高，预计 Phase 2 UI 开发周期可控制在 2 周内
4. 与 Matplotlib 深度集成，可直接渲染学术论文级绑图

### 8.2 决策 002：为什么选择 Python 而非 C++/Fortran

| 项目 | 内容 |
|------|------|
| **决策日期** | 2026-05-07 |
| **决策状态** | 已采纳 |
| **决策背景** | CFD 领域传统上使用 C++/Fortran 追求极致性能；但本项目定位为教学软件，代码可读性与开发效率优先 |

**候选方案对比**：

| 方案 | 优点 | 缺点 | 评估结论 |
|------|------|------|---------|
| Python (NumPy) | 语法简洁可读；生态丰富；开发效率高；适合教学 | 纯 Python 循环慢；需依赖 NumPy 向量化 | ✅ 采纳 |
| C++ | 极致性能；精细内存控制 | 开发周期长；编译复杂；教学代码可读性差 | 否决 |
| Fortran | 数值计算性能优异；科学计算传统语言 | 现代工具链支持弱；人才储备少；UI 开发困难 | 否决 |
| Python + Cython | 兼顾开发效率与性能 | 增加构建复杂度；需要编写 C 扩展 | 备选（未来优化） |

**决策理由**：
1. **教学导向**：学生需要阅读和理解源代码，Python 的语法清晰度显著优于 C++/Fortran
2. **性能足够**：一维问题计算量小，NumPy 向量化后 nx=2000 网格可在 30 秒内完成（满足 NFR-01.01）
3. **生态优势**：Streamlit、Matplotlib、Jinja2 等教学展示工具均为 Python 原生
4. **维护成本**：团队无 C++/Fortran 专家，采用 Python 可降低长期维护风险

**性能兜底策略**：若未来性能成为瓶颈，可将核心循环用 Cython 重写，保持 Python 接口不变。

### 8.3 决策 003：为什么采用 frozen dataclass 作为配置管理

| 项目 | 内容 |
|------|------|
| **决策日期** | 2026-05-07 |
| **决策状态** | 已采纳 |
| **决策背景** | 配置对象在多个模块间传递，需要保证数据一致性；数值计算过程中意外修改配置可能导致结果不可复现 |

**候选方案对比**：

| 方案 | 优点 | 缺点 | 评估结论 |
|------|------|------|---------|
| `@dataclass(frozen=True)` | 运行时不可变；类型提示支持；自动生成 `__init__`/`__repr__`/`__eq__` | 创建后修改需重建对象 | ✅ 采纳 |
| 普通 dict | 灵活；无学习成本 | 无类型安全；键名易出错；运行时可能被修改 | 否决 |
| Pydantic BaseModel | 强大的校验能力；JSON 序列化 | 引入额外依赖；frozen 模式较新 | 备选 |
| NamedTuple | 不可变；轻量 | 无默认值支持（Python < 3.6）；字段访问语法不如 dataclass 直观 | 否决 |

**决策理由**：
1. **不可变性保证**：`frozen=True` 确保配置对象一旦创建便不可修改，避免在长时间计算过程中被意外篡改
2. **类型安全**：配合 mypy 静态检查，可在编码阶段发现类型错误
3. **内置校验**：`__post_init__` 方法提供声明式参数合法性校验
4. **零额外依赖**：Python 标准库内置，无需引入 Pydantic 等第三方库
5. **哈希支持**：frozen dataclass 自动支持 `__hash__`，可作为字典键或缓存键使用

---

## 9. 性能考虑

### 9.1 计算密集型任务的优化策略

CFD-Class 的计算密集型任务主要集中在 Core 层的 `evolve()` 时间推进循环。优化策略如下：

#### 9.1.1 向量化运算

| 优化项 | 策略 | 预期收益 |
|--------|------|---------|
| 数组操作 | 全部使用 NumPy `ndarray` 向量化操作，避免 Python 级 `for` 循环 | 10~100 倍加速 |
| 通量计算 | 整网格同时计算数值通量，而非逐单元循环 | 5~10 倍加速 |
| 边界条件 | 使用切片赋值 `U[:, 0] = U[:, 1]` 而非逐点赋值 | 消除 Python 循环开销 |

#### 9.1.2 算法级优化

| 优化项 | 策略 | 适用场景 |
|--------|------|---------|
| 时间步长自适应 | 每步基于 CFL 条件重新计算 `dt`，避免全局最小时间步长 | 所有格式 |
| 快照稀疏记录 | 不记录每个时间步，仅按固定间隔（如每 0.01s）记录 | 动画生成 |
| 精确解缓存 | 同一配置下精确 Riemann 解只计算一次，多格式复用 | 多格式对比 |

#### 9.1.3 未来优化方向

| 方向 | 方案 | 触发条件 |
|------|------|---------|
| Numba JIT | 对 `evolve()` 循环添加 `@numba.jit` 装饰器 | nx=2000 时单格式运行时间 > 10 秒 |
| Cython 重写 | 将核心循环编译为 C 扩展 | 需要支持更大网格（nx > 5000） |
| 多进程并行 | 使用 `multiprocessing` 并行运行多种格式 | 用户同时选择 6 种格式时总耗时 > 30 秒 |

### 9.2 内存管理策略

#### 9.2.1 内存使用估算

以 nx=2000 网格为例：

| 数据对象 | 形状 | 数据类型 | 内存占用 |
|---------|------|---------|---------|
| 守恒变量 U | (2, 2000) | float64 | ~32 KB |
| 时间历史（100 个快照） | 100 × (2, 2000) | float64 | ~3.2 MB |
| 6 种格式结果 | 6 × 100 × (2, 2000) | float64 | ~19.2 MB |
| Matplotlib 图表 | 1920×1080 | RGBA | ~8 MB/张 |
| **峰值估算** | — | — | **< 100 MB** |

实际峰值远低于 NFR-01.05 的 512MB 限制，内存不是当前瓶颈。

#### 9.2.2 内存优化措施

| 措施 | 实现方式 | 目的 |
|------|---------|------|
| 数组复用 | 在 `evolve()` 内预分配 `U_new` 数组，避免每步创建新数组 | 减少 GC 压力 |
| 快照稀疏化 | 仅按用户指定间隔记录快照，默认每 20 步记录一次 | 控制 `time_history` 大小 |
| 结果及时释放 | Engines 层在生成 GIF/HTML 后，使用 `del` 释放临时大数组 | 降低峰值内存 |
| 生成器模式 | 动画引擎使用生成器逐帧绑图，而非一次性加载所有帧 | 流式处理 |

### 9.3 缓存策略

#### 9.3.1 应用级缓存

Streamlit 提供 `@st.cache_data` 装饰器，可用于缓存纯函数计算结果：

```python
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def run_simulation_cached(config: DamBreakConfig, scheme_name: str) -> SimulationResult:
    """缓存单次模拟结果，相同参数直接返回缓存."""
    scheme = SCHEME_REGISTRY[scheme_name]()
    return simulation_engine.run_single(config, scheme)
```

| 缓存内容 | 缓存键 | TTL | 说明 |
|---------|--------|-----|------|
| 单次模拟结果 | `(config, scheme_name)` 的哈希值 | 1 小时 | 用户重复运行相同参数时秒级响应 |
| 精确 Riemann 解 | `(h_L, h_R, u_L, u_R, g, t_end)` | 无限 | 精确解仅依赖初始条件 |
| 收敛性分析 | `(config_template, nx_list)` | 1 小时 | 网格序列分析计算量大，适合缓存 |

#### 9.3.2 缓存失效策略

| 场景 | 失效行为 |
|------|---------|
| 用户修改任意参数 | 所有相关缓存自动失效（Streamlit 基于输入参数哈希自动处理） |
| 应用重启 | 内存缓存清空，首次运行需重新计算 |
| 长时间未访问 | TTL 到期后自动清理，释放内存 |

#### 9.3.3 缓存注意事项

1. **frozen dataclass 的必要性**：`DamBreakConfig` 的不可变性确保其哈希值稳定，是缓存键可靠性的基础
2. **ndarray 不可哈希**：缓存函数接收/返回的 `ndarray` 需通过 `SimulationResult` dataclass 包装，或转换为 `bytes`
3. **内存上限**：Streamlit 缓存默认无上限，大量不同参数的模拟可能导致内存增长，需监控并在必要时设置 `max_entries`

---

## 10. 附录

### 10.1 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 浅水方程 | Shallow Water Equations (SWE) | 描述浅水流动的双曲型守恒律方程组 |
| 有限体积法 | Finite Volume Method (FVM) | 基于守恒律积分形式的数值离散方法 |
| Riemann 问题 | Riemann Problem | 初始为左右常数状态的守恒律初值问题 |
| TVD | Total Variation Diminishing | 总变差衰减，保证数值解无虚假振荡的性质 |
| CFL 条件 | Courant-Friedrichs-Lewy Condition | 双曲型方程显式格式的时间步长稳定性限制 |
| 冻结数据类 | Frozen Dataclass | Python 中创建后不可修改的 dataclass 实例 |

### 10.2 版本历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-05-09 | 初始正式版 | @Arch |

---

*文档结束*
