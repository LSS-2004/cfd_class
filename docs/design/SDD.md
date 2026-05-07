# 概要设计说明书 (SDD)

> **文档编号**: CFD-CLASS-SDD-001
> **版本**: v1.0
> **日期**: 2026-05-07
> **状态**: 框架版 (待完善)
> **依据标准**: GB/T 8567 计算机软件文档编制规范

---

## 文档控制信息

| 项目 | 内容 |
|------|------|
| **软件名称** | CFD-Class 一维溃坝CFD教学软件 |
| **文档作者** | @Arch (架构师) |
| **审核人** | @PM (项目经理) |
| **批准人** | @PM (项目经理) |

---

## 1. 引言

### 1.1 编写目的

本文档定义了 CFD-Class 软件的系统架构、模块划分、接口设计和数据结构。

### 1.2 参考资料

1. GB/T 8567-2006 计算机软件文档编制规范
2. SRS.md — 软件需求规格说明书
3. Toro, E.F. "Riemann Solvers and Numerical Methods for Fluid Dynamics"
4. PRODUCT_DELIVERY_STANDARD.md — 产品交付规范

---

## 2. 系统架构

### 2.1 架构模式

采用 **MVC (Model-View-Controller)** 分层架构：

```
┌─────────────────────────────────────────────┐
│              View Layer (视图层)              │
│         Streamlit UI Components              │
│    (pages/ + components/ + assets/)          │
├─────────────────────────────────────────────┤
│           Controller Layer (控制层)            │
│        Business Logic Engines               │
│         (engines/)                          │
├─────────────────────────────────────────────┤
│             Model Layer (模型层)              │
│          Core Computation Engine            │
│     (core/schemes/ + core/solvers/ + ...)   │
└─────────────────────────────────────────────┘
```

### 2.2 技术架构图

```
                    ┌─────────────┐
                    │   Browser   │
                    │  (Chrome/   │
                    │ Firefox/Edge│
                    └──────┬──────┘
                           │ HTTP/WebSocket
                    ┌──────▼──────┐
                    │  Streamlit  │
                    │   Server    │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐     ┌──────▼──────┐   ┌───────▼──────┐
   │ Home Page│     │Simulation   │   │Animation     │
   │ (理论背景)│     │Page(参数运行)│   │Page(可视化)  │
   └──────────┘     └──────┬──────┘   └───────┬──────┘
                           │                  │
                   ┌───────▼──────────────────▼───────┐
                   │      SimulationEngine           │
                   │   (业务逻辑协调器)                 │
                   └───────────────┬─────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
             ┌──────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
             │ BaseScheme  │ │Riemann   │ │ErrorAnalysis│
             │ (6种格式实现)│ │Solver    │ │ (误差度量)   │
             └─────────────┘ └──────────┘ └─────────────┘
```

---

## 3. 模块设计

### 3.1 核心计算引擎 (`src/core/`)

#### 3.1.1 配置模块 (`config.py`)

```python
@dataclass(frozen=True)
class DamBreakConfig:
    """溃坝问题运行参数配置.

    使用 frozen dataclass 确保配置不可变，
    避免运行时意外修改导致结果不一致。
    """

    # 物理参数
    h_L: float = 1.0       # 左侧水深 [m]
    h_R: float = 0.0       # 右侧水深 [m] (0=干底)
    u_L: float = 0.0       # 左侧流速 [m/s]
    u_R: float = 0.0       # 右侧流速 [m/s]
    g: float = 9.81        # 重力加速度 [m/s²]

    # 数值参数
    cfl: float = 0.9       # CFL稳定性数
    nx: int = 200          # 网格单元数
    t_end: float = 0.5     # 终止时间 [s]

    # 域参数
    x_min: float = -5.0    # 左边界 [m]
    x_max: float = 5.0     # 右边界 [m]

    def __post_init__(self) -> None:
        """参数合法性校验."""
        if self.h_L <= 0:
            raise ValueError("h_L must be positive")
        if self.h_R < 0:
            raise ValueError("h_R must be non-negative")
        if self.cfl <= 0 or self.cfl > 1.0:
            raise ValueError("CFL must be in (0, 1]")
        if self.nx < 10:
            raise ValueError("nx must be >= 10")

    @property
    def dx(self) -> float:
        """网格步长."""
        return (self.x_max - self.x_min) / self.nx

    @property
    def x_grid(self) -> NDArray[np.float64]:
        """网格节点坐标（单元中心）."""
        return np.linspace(
            self.x_min + self.dx / 2,
            self.x_max - self.dx / 2,
            self.nx
        )
```

#### 3.1.2 格式基类 (`schemes/base_scheme.py`)

```python
class BaseScheme(ABC):
    """有限体积格式抽象基类.

    所有数值格式必须继承此类并实现 evolve() 方法。
    提供统一的接口供上层调用。
    """

    def __init__(
        self,
        name: str,
        order: int,
        tvd: bool = False
    ) -> None:
        self.name = name
        self.order = order
        self.tvd = tvd

    @abstractmethod
    def evolve(
        self,
        U0: NDArray[np.float64],
        config: DamBreakConfig,
        progress_callback: Optional[Callable[[float, float], None]] = None
    ) -> Dict[float, NDArray[np.float64]]:
        """执行时间演化计算.

        Args:
            U0: 初始守恒变量矩阵, shape=(2, nx), U[0]=h, U[1]=hu
            config: 运行参数配置
            progress_callback: 进度回调函数 callback(current_time, end_time)

        Returns:
            字典 {时刻t: 解状态U}, 包含所有记录时刻的解

        Raises:
            ValueError: 输入参数不合法
            NumericalInstabilityError: 数值不稳定时
        """
        pass

    def _compute_dt(
        self,
        U: NDArray[np.float64],
        config: DamBreakConfig
    ) -> float:
        """基于CFL条件计算稳定时间步长."""
        h = U[0, :]
        u = np.where(h > EPS_H, U[1, :] / h, 0.0)
        c = np.sqrt(config.g * np.maximum(h, EPS_H))
        max_speed = np.max(np.abs(u) + c)
        return config.cfl * config.dx / max_speed

    def _apply_bc(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """应用透射边界条件（零梯度外推）."""
        U[:, 0] = U[:, 1]
        U[:, -1] = U[:, -2]
        return U
```

#### 3.1.3 六种格式接口

所有格式统一实现 `BaseScheme.evolve()` 接口：

| 格式类名 | 文件 | 阶数 | TVD | 关键算法 |
|---------|------|------|-----|---------|
| `LaxFriedrichsScheme` | `lax_friedrichs.py` | 1 | ✅ | 数值粘性通量分裂 |
| `LaxWendroffScheme` | `lax_wendroff.py` | 2 | ❌ | 两步Taylor展开 |
| `MacCormackScheme` | `maccormack.py` | 2 | ❌ | 预测-校正两步法 |
| `GodunovScheme` | `godunov.py` | 1+ | ✅ | 精确Riemann求解器 |
| `HLLOneScheme` | `hll.py` | 1+ | ✅ | HLL近似Riemann通量 |
| `MUSCLHancockScheme` | `muscl_hancock.py` | 2 | ✅ | MUSCL重构+minmod限制器 |

#### 3.1.4 Riemann求解器 (`solvers/riemann_solver.py`)

```python
def exact_riemann_solution(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float
) -> dict:
    """计算精确Riemann解.

    支持湿底和干底两种情况。
    使用Newton-Raphson迭代求解非线性星区方程。

    Args:
        U_L: 左侧守恒变量 [h_L, hu_L]
        U_R: 右侧守恒变量 [h_R, hu_R]
        g: 重力加速度

    Returns:
        dict包含:
        - 'S_L': 左波波速
        - 'S_R': 右波波速
        - 'h_star': 星区水深
        - 'u_star': 星区流速
        - 'type': 波系类型 ('dry_ritter', 'wet_general', etc.)
    """
    pass


def hll_flux(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float
) -> NDArray[np.float64]:
    """计算HLL近似Riemann通量.

    两波近似: F_HLL = (S_R*F_L - S_L*F_R + S_L*S_R*(U_R-U_L)) / (S_R-S_L)
    """
    pass
```

#### 3.1.5 误差分析工具 (`analysis/error_analysis.py`)

```python
def compute_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    p: int = 2
) -> float:
    """计算p范数误差.

    Args:
        numerical: 数值解
        exact: 精确解
        p: 范数阶数 (1=L1, 2=L2, inf=L∞)

    Returns:
        误差值
    """
    pass


def estimate_order(
    nx_list: List[int],
    errors: List[float]
) -> float:
    """估计收敛阶.

    通过 log-log 线性拟合 error ∝ nx^(-order).

    Args:
        nx_list: 网格序列, 如 [50, 100, 200, 400, 800]
        errors: 对应的误差列表

    Returns:
        估计的收敛阶 order
    """
    pass
```

### 3.2 前端模块 (`src/frontend/`)

#### 3.2.1 主入口 (`app.py`)

```python
import streamlit as st

def main() -> None:
    """应用主入口，配置侧栏导航和页面路由."""

    st.set_page_config(
        page_title="CFD-Class 一维溃坝教学",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.image("assets/logo.png", width=100)
        st.title("CFD-Class")
        st.caption("一维溃坝CFD教学软件 v0.1.0-alpha")

        page = st.radio(
            "导航",
            ["🏠 首页", "📊 模拟", "🎬 动画", "📝 报告"],
            label_visibility="collapsed"
        )

    if page == "🏠 首页":
        from src.frontend.pages import home
        home.render()
    elif page == "📊 模拟":
        from src.frontend.pages import simulation
        simulation.render()
    elif page == "🎬 动画":
        from src.frontend.pages import animation
        animation.render()
    elif page == "📝 报告":
        from src.frontend.pages import report
        report.render()


if __name__ == "__main__":
    main()
```

#### 3.2.2 页面模块 (`pages/`)

每个页面是一个独立的 Python 模块，导出 `render()` 函数：

```python
# pages/simulation.py 示例结构
def render() -> None:
    """渲染模拟页面."""
    st.header("📊 数值模拟")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        # 参数面板组件
        from src.frontend.components import param_panel
        config = param_panel.render()

        # 格式选择组件
        from src.frontend.components import scheme_selector
        selected_schemes = scheme_selector.render()

    with col_right:
        # 运行控制
        if st.button("▶ 开始模拟", type="primary"):
            run_simulation(config, selected_schemes)


def run_simulation(
    config: DamBreakConfig,
    schemes: List[str]
) -> None:
    """执行模拟并显示结果."""
    from src.frontend.engines import simulation_engine
    results = simulation_engine.run(config, schemes)

    from src.frontend.components import result_viewer
    result_viewer.display(results)
```

#### 3.2.3 业务逻辑引擎 (`engines/`)

| 引擎 | 文件 | 功能 |
|------|------|------|
| `SimulationEngine` | `simulation_engine.py` | 协调core模块执行模拟，返回标准化结果 |
| `AnimationEngine` | `animation_engine.py` | 生成GIF/视频动画帧序列 |
| `ReportGenerator` | `report_generator.py` | 生成HTML格式分析报告 |

---

## 4. 接口定义

### 4.1 内部API (Core → Frontend)

```
Core Engine API:
├── BaseScheme.evolve(U0, config) → Dict[t, U]
├── exact_riemann_solution(U_L, U_R, g) → dict
├── hll_flux(U_L, U_R, g) → ndarray
├── compute_error(num, exact, p) → float
├── estimate_order(nx_list, errors) → float
└── DamBreakConfig (frozen dataclass)
```

### 4.2 外部API (用户通过UI调用)

用户通过Streamlit界面间接调用所有功能，无直接编程API。

---

## 5. 数据结构

### 5.1 守恒变量

```python
# 守恒变量向量 U = [h, hu]^T
# h: 水深 [m], 必须满足 h >= 0
# hu: 动量密度 [m²/s] = h * u

# 原始变量
u = hu / h  # 流速 [m/s] (当 h > EPS_H 时)
c = sqrt(g * h)  # 波速 [m/s]

# 通量向量 F = [hu, hu² + gh²/2]^T
```

### 5.2 结果数据结构

```python
@dataclass
class SimulationResult:
    """单次模拟的标准化结果."""

    config: DamBreakConfig
    scheme_name: str
    time_history: Dict[float, NDArray]  # {t: U(2×nx)}
    exact_solution: Optional[NDArray] = None
    errors: Optional[Dict[str, float]] = None  # {'L1': ..., 'L2': ..., 'Linf': ...}
    execution_time: float = 0.0  # 秒
    mass_conservation_error: float = 0.0
```

---

## 6. 错误处理

### 6.1 自定义异常类

```python
class CFDError(Exception):
    """CFD-Class 基础异常."""


class ConfigValidationError(CFDError):
    """配置参数验证错误."""


class NumericalInstabilityError(CFDError):
    """数值不稳定错误."""


class ConvergenceError(CFDError):
    """求解器未收敛错误."""


class PositiveDepthViolation(CFDError):
    """负水深违反正性保持条件."""
```

### 6.2 错误处理策略

| 异常类型 | 触发场景 | 处理方式 |
|---------|---------|---------|
| `ConfigValidationError` | 参数超出范围 | 前端显示友好提示，阻止运行 |
| `NumericalInstabilityError` | CFL过大或激波过强 | 降低CFL自动重试，最多3次 |
| `ConvergenceError` | Riemann迭代不收敛 | 回退到HLL近似求解器 |
| `PositiveDepthViolation` | 干底工况下出现负值 | 应用正性修正(h=max(h, EPS_H)) |

---

*文档结束*
*版本历史*: v1.0 (2026-05-07) 初始框架版
