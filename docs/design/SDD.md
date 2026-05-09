# 概要设计说明书 (SDD)

> **文档编号**: CFD-CLASS-SDD-001
> **版本**: v1.1
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

---

## 1. 引言

### 1.1 编写目的

本文档定义了 CFD-Class 软件的系统架构、模块划分、接口设计和数据结构，为开发团队提供详细的设计依据和实现指导。

**文档范围**:
- 覆盖 CFD-Class 软件的全部设计内容，包括系统架构、模块详细设计、数据结构、算法设计、接口定义及测试策略
- 涵盖核心计算引擎（Model层）、前端界面（View层）及业务逻辑引擎（Controller层）的完整设计
- 包含六种有限体积格式（LF/LW/MC/Godunov/HLL/MUSCL-Hancock）的算法描述
- 包含 Riemann 求解器、误差分析等核心算法的详细设计

**预期读者**:
| 读者类型 | 使用目的 |
|---------|---------|
| 开发团队 (@BE, @FE) | 作为编码实现的直接技术依据 |
| 测试人员 (@QA) | 理解模块接口，设计测试用例 |
| 项目管理人员 (@PM) | 掌握技术方案，进行进度与风险管控 |
| 未来维护者 | 理解系统结构，进行功能扩展或缺陷修复 |
| 技术评审人员 | 评估设计合理性与实现可行性 |

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

### 2.2 模块划分图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CFD-Class 系统模块划分                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    View Layer (视图层)                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  home    │  │simulation│  │animation │  │  report  │   │   │
│  │  │  首页    │  │ 模拟页面 │  │ 动画页面 │  │ 报告页面 │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │   │
│  │  │param_panel│  │scheme_   │  │result_   │  (components/)  │   │
│  │  │参数面板  │  │selector  │  │viewer    │                  │   │
│  │  └──────────┘  └──────────┘  └──────────┘                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│                              │ 调用 render()                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 Controller Layer (控制层)                    │   │
│  │  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │   │
│  │  │SimulationEngine│ │ AnimationEngine│ │ ReportGenerator│  │   │
│  │  │  模拟协调引擎   │ │  动画生成引擎   │ │  报告生成引擎   │  │   │
│  │  └────────────────┘ └────────────────┘ └────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│                              │ 调用 evolve() / compute_error()      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Model Layer (模型层)                       │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │              schemes/ (六种数值格式)                  │   │   │
│  │  │  ┌────┐ ┌────┐ ┌────┐ ┌──────┐ ┌────┐ ┌─────────┐ │   │   │
│  │  │  │ LF │ │ LW │ │ MC │ │Godunov│ │HLL │ │MUSCL-Han│ │   │   │
│  │  │  └────┘ └────┘ └────┘ └──────┘ └────┘ └─────────┘ │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│   │
│  │  │ solvers/        │  │ analysis/       │  │ config.py   ││   │
│  │  │ Riemann求解器   │  │ 误差分析工具     │  │ 配置管理    ││   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────┘│   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    utils/ (通用工具层)                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │   │
│  │  │ 异常定义    │  │ 常量定义    │  │ 数学辅助函数        │ │   │
│  │  │ exceptions  │  │ constants   │  │ math_utils          │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.3 技术架构图

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

**模块职责**: 集中管理溃坝问题的所有运行参数，提供不可变配置对象和参数合法性校验。

**配置参数完整列表**:

| 参数名 | 类型 | 默认值 | 范围限制 | 物理/数值含义 | 校验规则 |
|--------|------|--------|----------|--------------|----------|
| `h_L` | float | 1.0 | [0.1, 10.0] | 左侧初始水深 [m] | 必须 > 0 |
| `h_R` | float | 0.0 | [0.0, 10.0] | 右侧初始水深 [m]，0表示干底 | 必须 ≥ 0 |
| `u_L` | float | 0.0 | [-5.0, 5.0] | 左侧初始流速 [m/s] | 无额外限制 |
| `u_R` | float | 0.0 | [-5.0, 5.0] | 右侧初始流速 [m/s] | 无额外限制 |
| `g` | float | 9.81 | [0.1, 20.0] | 重力加速度 [m/s²] | 必须 > 0 |
| `cfl` | float | 0.9 | [0.1, 0.95] | CFL稳定性数 | 必须 ∈ (0, 1] |
| `nx` | int | 200 | [50, 2000] | 网格单元数 | 必须 ≥ 10 |
| `t_end` | float | 0.5 | [0.1, 10.0] | 终止模拟时间 [s] | 必须 > 0 |
| `x_min` | float | -5.0 | [-20.0, 0.0] | 计算域左边界 [m] | 必须 < x_max |
| `x_max` | float | 5.0 | [0.0, 20.0] | 计算域右边界 [m] | 必须 > x_min |

**校验规则详细说明**:

1. **物理约束校验**: `h_L > 0`, `h_R ≥ 0`, `g > 0`
2. **数值稳定性校验**: `0 < cfl ≤ 1.0`，建议不超过 0.95
3. **网格分辨率校验**: `nx ≥ 10`，保证基本计算精度
4. **域有效性校验**: `x_min < x_max`
5. **干底工况特殊处理**: 当 `h_R = 0` 时，右侧为干底，需触发干底 Riemann 求解分支

**派生属性**:

| 属性名 | 类型 | 计算方式 | 说明 |
|--------|------|----------|------|
| `dx` | float | `(x_max - x_min) / nx` | 均匀网格步长 |
| `x_grid` | NDArray | `linspace(x_min+dx/2, x_max-dx/2, nx)` | 单元中心坐标数组 |

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
        if self.x_min >= self.x_max:
            raise ValueError("x_min must be less than x_max")
        if self.g <= 0:
            raise ValueError("g must be positive")
        if self.t_end <= 0:
            raise ValueError("t_end must be positive")

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

**模块职责**: 定义所有有限体积格式的统一接口，封装公共功能（CFL时间步长计算、边界条件处理、正性保持）。

**类属性说明**:

| 属性名 | 类型 | 说明 |
|--------|------|------|
| `name` | str | 格式名称（如 "Lax-Friedrichs"） |
| `order` | int | 格式精度阶数（1 或 2） |
| `tvd` | bool | 是否具备 TVD 性质 |

**抽象方法详细说明**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `evolve` | `U0`, `config`, `progress_callback` | `Dict[float, NDArray]` | 执行完整的时间演化计算，必须实现 |
| `_compute_flux` | `U_L`, `U_R`, `g` | `NDArray` | 计算数值通量（部分格式需重写） |

**具体方法说明**:

| 方法名 | 访问级别 | 功能描述 | 算法说明 |
|--------|----------|----------|----------|
| `_compute_dt` | protected | CFL自适应时间步长 | `dt = cfl * dx / max(|u|+c)` |
| `_apply_bc` | protected | 透射边界条件 | 零梯度外推：`U[:,0]=U[:,1]`, `U[:,-1]=U[:,-2]` |
| `_positive_fix` | protected | 正性保持修正 | `h = max(h, EPS_H)` |
| `_conserved_to_primitive` | protected | 守恒变量转原始变量 | `u = hu/h` (当 `h>EPS_H`) |

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
        """基于CFL条件计算稳定时间步长.

        算法:
        1. 从守恒变量提取水深 h = U[0, :]
        2. 计算流速 u = hu/h (当 h > EPS_H 时，否则 u = 0)
        3. 计算波速 c = sqrt(g*h)
        4. 最大特征速度 = max(|u| + c)
        5. dt = cfl * dx / max_speed
        """
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

    def _positive_fix(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """正性保持修正，防止负水深."""
        U[0, :] = np.maximum(U[0, :], EPS_H)
        return U
```

#### 3.1.3 六种格式接口

所有格式统一实现 `BaseScheme.evolve()` 接口。

**格式总览**:

| 格式类名 | 文件 | 阶数 | TVD | 关键算法 |
|---------|------|------|-----|---------|
| `LaxFriedrichsScheme` | `lax_friedrichs.py` | 1 | ✅ | 数值粘性通量分裂 |
| `LaxWendroffScheme` | `lax_wendroff.py` | 2 | ❌ | 两步Taylor展开 |
| `MacCormackScheme` | `maccormack.py` | 2 | ❌ | 预测-校正两步法 |
| `GodunovScheme` | `godunov.py` | 1+ | ✅ | 精确Riemann求解器 |
| `HLLOneScheme` | `hll.py` | 1+ | ✅ | HLL近似Riemann通量 |
| `MUSCLHancockScheme` | `muscl_hancock.py` | 2 | ✅ | MUSCL重构+minmod限制器 |

---

**① Lax-Friedrichs 格式**

*算法描述*: 最基础的中心格式，通过添加数值粘性项保证稳定性。数值通量取左右通量平均加上粘性耗散项。

*数值通量公式*:
```
F_{i+1/2} = 0.5 * (F(U_i) + F(U_{i+1})) - 0.5 * (dx/dt) * (U_{i+1} - U_i)
```

*伪代码*:
```
function evolve_LF(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)
        U_new = zeros_like(U)

        for i = 1 to nx-2:
            F_L = flux(U[:, i])
            F_R = flux(U[:, i+1])
            F_half = 0.5*(F_L + F_R) - 0.5*(dx/dt)*(U[:, i+1] - U[:, i])

            F_L_prev = flux(U[:, i-1])
            F_R_prev = flux(U[:, i])
            F_half_prev = 0.5*(F_L_prev + F_R_prev) - 0.5*(dx/dt)*(U[:, i] - U[:, i-1])

            U_new[:, i] = U[:, i] - (dt/dx)*(F_half - F_half_prev)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

---

**② Lax-Wendroff 格式**

*算法描述*: 基于Taylor展开的二阶精度格式，先进行预测步（半步长），再进行校正步（整步长）。

*伪代码*:
```
function evolve_LW(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)

        # 预测步: 半步长
        U_half = zeros_like(U)
        for i = 0 to nx-2:
            F_i = flux(U[:, i])
            F_ip1 = flux(U[:, i+1])
            U_half[:, i] = 0.5*(U[:, i] + U[:, i+1]) - 0.5*(dt/dx)*(F_ip1 - F_i)

        # 校正步: 整步长
        U_new = U.copy()
        for i = 1 to nx-2:
            F_half_i = flux(U_half[:, i-1])
            F_half_ip1 = flux(U_half[:, i])
            U_new[:, i] = U[:, i] - (dt/dx)*(F_half_ip1 - F_half_i)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

---

**③ MacCormack 格式**

*算法描述*: 预测-校正型两步格式，预测步用向前差分，校正步用向后差分，具有二阶精度。

*伪代码*:
```
function evolve_MC(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)

        # 预测步 (向前差分)
        U_pred = U.copy()
        for i = 0 to nx-2:
            F_i = flux(U[:, i])
            F_ip1 = flux(U[:, i+1])
            U_pred[:, i] = U[:, i] - (dt/dx)*(F_ip1 - F_i)

        U_pred = _apply_bc(U_pred)

        # 校正步 (向后差分)
        U_new = U.copy()
        for i = 1 to nx-1:
            F_pred_i = flux(U_pred[:, i])
            F_pred_im1 = flux(U_pred[:, i-1])
            U_new[:, i] = 0.5*(U[:, i] + U_pred[:, i]) - 0.5*(dt/dx)*(F_pred_i - F_pred_im1)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

---

**④ Godunov 格式**

*算法描述*: 一阶迎风格式，通过精确求解每个单元界面上的 Riemann 问题来计算数值通量，天然具备激波捕捉能力。

*伪代码*:
```
function evolve_Godunov(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)
        U_new = U.copy()

        for i = 1 to nx-2:
            # 求解界面 (i-1/2) 的 Riemann 问题
            U_L = U[:, i-1]
            U_R = U[:, i]
            riemann = exact_riemann_solution(U_L, U_R, config.g)

            # 构造界面通量
            h_star = riemann['h_star']
            u_star = riemann['u_star']
            F_boundary = [h_star * u_star, h_star * u_star^2 + 0.5*g*h_star^2]

            # 根据波速方向确定通量
            if riemann['S_L'] >= 0:
                F_left = flux(U_L)
            elif riemann['S_R'] <= 0:
                F_left = flux(U_R)
            else:
                F_left = F_boundary

            # 同理求解界面 (i+1/2)
            U_L2 = U[:, i]
            U_R2 = U[:, i+1]
            riemann2 = exact_riemann_solution(U_L2, U_R2, config.g)
            # ... 确定 F_right

            U_new[:, i] = U[:, i] - (dt/dx)*(F_right - F_left)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

---

**⑤ HLL 格式**

*算法描述*: Harten-Lax-van Leer 近似 Riemann 求解器，用左右两个波速近似 Riemann 问题的波系结构，计算效率高。

*HLL 通量公式*:
```
F_HLL = (S_R * F_L - S_L * F_R + S_L * S_R * (U_R - U_L)) / (S_R - S_L)
```

其中波速估计:
```
S_L = min(u_L - c_L, u_R - c_R, u_hat - c_hat)
S_R = max(u_L + c_L, u_R + c_R, u_hat + c_hat)
```

*伪代码*:
```
function evolve_HLL(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)
        U_new = U.copy()

        for i = 1 to nx-2:
            U_L = U[:, i-1]
            U_R = U[:, i]
            F_L = flux(U_L)
            F_R = flux(U_R)

            # 估计波速
            h_L = U_L[0]; u_L = U_L[1]/h_L; c_L = sqrt(g*h_L)
            h_R = U_R[0]; u_R = U_R[1]/h_R; c_R = sqrt(g*h_R)

            h_hat = 0.5*(h_L + h_R)
            u_hat = (sqrt(h_L)*u_L + sqrt(h_R)*u_R) / (sqrt(h_L) + sqrt(h_R))
            c_hat = sqrt(g*h_hat)

            S_L = min(u_L - c_L, u_R - c_R, u_hat - c_hat)
            S_R = max(u_L + c_L, u_R + c_R, u_hat + c_hat)

            # 计算 HLL 通量
            if S_L >= 0:
                F_half = F_L
            elif S_R <= 0:
                F_half = F_R
            else:
                F_half = (S_R*F_L - S_L*F_R + S_L*S_R*(U_R - U_L)) / (S_R - S_L)

            # 同理计算右侧界面通量 F_half_right
            U_new[:, i] = U[:, i] - (dt/dx)*(F_half_right - F_half)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

---

**⑥ MUSCL-Hancock 格式**

*算法描述*: 二阶高分辨率格式，通过 MUSCL 线性重构和 minmod 限制器实现高阶精度，同时保持 TVD 性质。包含三步：变量重构、边界外推（预测步）、通量计算（校正步）。

*伪代码*:
```
function evolve_MUSCL(U0, config):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}

    while t < config.t_end:
        dt = min(_compute_dt(U, config), config.t_end - t)

        # Step 1: 计算单元边界值 (MUSCL重构)
        U_L_face = zeros_like(U)
        U_R_face = zeros_like(U)

        for i = 1 to nx-2:
            # 计算相邻单元的梯度 (minmod限制器)
            delta_L = U[:, i] - U[:, i-1]
            delta_R = U[:, i+1] - U[:, i]

            for var = 0 to 1:
                if delta_L[var] > 0 and delta_R[var] > 0:
                    slope = min(delta_L[var], delta_R[var])
                elif delta_L[var] < 0 and delta_R[var] < 0:
                    slope = max(delta_L[var], delta_R[var])
                else:
                    slope = 0

                # 线性重构: U_face = U_i ± 0.5*slope
                U_L_face[var, i] = U[var, i] - 0.5*slope
                U_R_face[var, i] = U[var, i] + 0.5*slope

        # Step 2: 时间预测 (半步长)
        U_pred = zeros_like(U)
        for i = 1 to nx-2:
            F_i = flux(U[:, i])
            F_im1 = flux(U[:, i-1])
            F_ip1 = flux(U[:, i+1])

            # 从左右边界值计算通量
            U_pred[:, i] = U[:, i] - 0.5*(dt/dx)*(flux(U_R_face[:, i]) - flux(U_L_face[:, i]))

        U_pred = _apply_bc(U_pred)
        U_pred = _positive_fix(U_pred)

        # Step 3: 用预测值计算 Riemann 通量 (Godunov或HLL)
        U_new = U.copy()
        for i = 1 to nx-2:
            # 左侧界面: U_R_face[:, i-1] (右值) 与 U_L_face[:, i] (左值)
            UL = U_R_face[:, i-1]
            UR = U_L_face[:, i]

            # 使用 HLL 通量 (或 Godunov)
            F_left = hll_flux(UL, UR, config.g)

            # 右侧界面
            UL2 = U_R_face[:, i]
            UR2 = U_L_face[:, i+1]
            F_right = hll_flux(UL2, UR2, config.g)

            U_new[:, i] = U[:, i] - (dt/dx)*(F_right - F_left)

        U = _apply_bc(U_new)
        U = _positive_fix(U)
        t += dt
        snapshots[t] = U.copy()

    return snapshots
```

#### 3.1.4 Riemann求解器 (`solvers/riemann_solver.py`)

**模块职责**: 提供一维浅水方程 Riemann 问题的精确解和近似解，用于 Godunov 格式通量计算和精确解对比。

**波系类型判断**:

| 类型 | 条件 | 处理方式 |
|------|------|----------|
| `dry_ritter` | `h_R = 0` (干底) | 使用 Ritter 干底解析解 |
| `wet_general` | `h_L > 0` 且 `h_R > 0` | Newton-Raphson 迭代求解 |
| `dry_left` | `h_L = 0` | 右侧稀疏波向干底扩展 |

**Newton-Raphson 迭代算法伪代码**:

```
function exact_riemann_solution(U_L, U_R, g):
    h_L = U_L[0];  u_L = U_L[1]/h_L
    h_R = U_R[0];  u_R = U_R[1]/h_R

    # 干底情况
    if h_R < EPS_H:
        return solve_dry_ritter(h_L, u_L, g)

    # 湿底情况: Newton-Raphson 求解星区水深 h_star
    # 定义压力函数 f(h) = f_L(h) + f_R(h) + u_R - u_L = 0
    # 其中:
    #   f_L(h) = 2*(sqrt(g*h_L) - sqrt(g*h))           if h <= h_L (稀疏波)
    #   f_L(h) = (h - h_L) * sqrt(0.5*g*(h+h_L)/(h*h_L)) if h > h_L (激波)
    #   f_R(h) 同理

    # 初始猜测
    h_guess = 0.5 * (h_L + h_R)

    for iteration = 1 to MAX_ITER:
        # 计算左压力函数 f_L 及其导数 df_L
        if h_guess <= h_L:
            # 稀疏波分支
            f_L = 2 * (sqrt(g*h_L) - sqrt(g*h_guess))
            df_L = -sqrt(g/h_guess)
        else:
            # 激波分支
            A = sqrt(0.5*g*(h_guess + h_L)/(h_guess*h_L))
            f_L = (h_guess - h_L) * A
            df_L = A - 0.25*g*(h_guess - h_L)/(A*h_guess^2)

        # 计算右压力函数 f_R 及其导数 df_R
        if h_guess <= h_R:
            f_R = 2 * (sqrt(g*h_R) - sqrt(g*h_guess))
            df_R = -sqrt(g/h_guess)
        else:
            A = sqrt(0.5*g*(h_guess + h_R)/(h_guess*h_R))
            f_R = (h_guess - h_R) * A
            df_R = A - 0.25*g*(h_guess - h_R)/(A*h_guess^2)

        # 残差和更新
        residual = f_L + f_R + u_R - u_L
        derivative = df_L + df_R

        if abs(residual) < TOLERANCE:
            break

        h_new = h_guess - residual / derivative

        # 保证正性
        if h_new <= 0:
            h_new = 0.5 * h_guess

        h_guess = h_new

    h_star = h_guess
    u_star = 0.5 * (u_L + u_R) + 0.5 * (f_R - f_L)

    # 计算波速
    if h_star <= h_L:
        S_L = u_L - sqrt(g*h_L)          # 左稀疏波头速度
    else:
        S_L = u_L - sqrt(0.5*g*(h_star+h_L)*h_star/h_L)  # 左激波速度

    if h_star <= h_R:
        S_R = u_R + sqrt(g*h_R)          # 右稀疏波头速度
    else:
        S_R = u_R + sqrt(0.5*g*(h_star+h_R)*h_star/h_R)  # 右激波速度

    return {
        'h_star': h_star,
        'u_star': u_star,
        'S_L': S_L,
        'S_R': S_R,
        'type': 'wet_general'
    }
```

**HLL 近似通量算法**:

```python
def hll_flux(U_L, U_R, g):
    """计算HLL近似Riemann通量.

    两波近似: F_HLL = (S_R*F_L - S_L*F_R + S_L*S_R*(U_R-U_L)) / (S_R-S_L)
    """
    F_L = flux(U_L)
    F_R = flux(U_R)

    h_L = U_L[0]; u_L = U_L[1]/max(h_L, EPS_H); c_L = sqrt(g*h_L)
    h_R = U_R[0]; u_R = U_R[1]/max(h_R, EPS_H); c_R = sqrt(g*h_R)

    # Roe 平均波速估计
    h_hat = 0.5*(h_L + h_R)
    u_hat = (sqrt(h_L)*u_L + sqrt(h_R)*u_R) / (sqrt(h_L) + sqrt(h_R))
    c_hat = sqrt(g*h_hat)

    S_L = min(u_L - c_L, u_R - c_R, u_hat - c_hat)
    S_R = max(u_L + c_L, u_R + c_R, u_hat + c_hat)

    if S_L >= 0:
        return F_L
    elif S_R <= 0:
        return F_R
    else:
        return (S_R*F_L - S_L*F_R + S_L*S_R*(U_R - U_L)) / (S_R - S_L)
```

#### 3.1.5 误差分析工具 (`analysis/error_analysis.py`)

**模块职责**: 提供数值解与精确解的误差度量、收敛阶估计及质量守恒检查。

**误差度量算法**:

| 范数类型 | 公式 | 适用场景 |
|----------|------|----------|
| L1 | `Σ|num - exact| * dx` | 整体误差评估 |
| L2 | `sqrt(Σ|num - exact|² * dx)` | 均方根误差 |
| L∞ | `max|num - exact|` | 最大单点误差 |

*伪代码*:
```
function compute_error(numerical, exact, p, dx):
    diff = abs(numerical - exact)

    if p == 1:
        return sum(diff) * dx
    elif p == 2:
        return sqrt(sum(diff^2) * dx)
    elif p == inf:
        return max(diff)
    else:
        return (sum(diff^p) * dx)^(1/p)
```

**收敛阶估计算法**:

*理论背景*: 对于收敛的数值格式，误差与网格尺寸满足 `error ∝ dx^order ∝ nx^(-order)`。取对数后得到线性关系：`log(error) = C - order * log(nx)`。

*算法步骤*:
1. 对网格序列 `nx_list` 和对应误差 `errors` 取对数
2. 使用最小二乘法拟合直线 `y = a + b*x`
3. 收敛阶 `order = -b`
4. 计算拟合优度 R² 评估可靠性

*伪代码*:
```
function estimate_order(nx_list, errors):
    # 输入验证
    if length(nx_list) < 2 or length(errors) < 2:
        raise ValueError("至少需要2组数据")

    # 取对数
    log_nx = log(nx_list)      # x = log(nx)
    log_err = log(errors)      # y = log(error)

    # 最小二乘线性拟合: y = a + b*x
    n = length(nx_list)
    x_mean = mean(log_nx)
    y_mean = mean(log_err)

    numerator = sum((log_nx - x_mean) * (log_err - y_mean))
    denominator = sum((log_nx - x_mean)^2)

    slope = numerator / denominator       # b = d(log_err)/d(log_nx)
    intercept = y_mean - slope * x_mean   # a

    order = -slope

    # 计算 R²
    ss_res = sum((log_err - (intercept + slope*log_nx))^2)
    ss_tot = sum((log_err - y_mean)^2)
    r_squared = 1 - ss_res / ss_tot

    return {
        'order': order,
        'r_squared': r_squared,
        'intercept': intercept
    }
```

**质量守恒检查算法**:

```
function check_mass_conservation(U_history, config):
    initial_mass = sum(U_history[0.0][0, :]) * config.dx
    final_mass = sum(U_history[config.t_end][0, :]) * config.dx

    relative_error = abs(final_mass - initial_mass) / initial_mass

    return {
        'initial_mass': initial_mass,
        'final_mass': final_mass,
        'relative_error': relative_error,
        'passed': relative_error < 1e-6
    }
```

### 3.2 前端模块 (`src/frontend/`)

#### 3.2.1 主入口 (`app.py`)

**模块职责**: 应用主入口，负责全局页面配置、侧边栏导航、页面路由和 Streamlit 会话状态管理。

**页面路由表**:

| 页面标识 | 显示名称 | 对应模块 | 功能描述 |
|----------|----------|----------|----------|
| `home` | 🏠 首页 | `pages/home.py` | 理论背景、公式推导、学习路径 |
| `simulation` | 📊 模拟 | `pages/simulation.py` | 参数设置、格式选择、运行模拟 |
| `animation` | 🎬 动画 | `pages/animation.py` | GIF生成、多格式对比动画 |
| `report` | 📝 报告 | `pages/report.py` | 收敛性分析、HTML报告生成 |

**状态管理说明**:

Streamlit 使用 `st.session_state` 管理跨页面状态：

| 状态键 | 类型 | 作用域 | 说明 |
|--------|------|--------|------|
| `simulation_results` | Dict[str, SimulationResult] | 全局 | 存储最近一次模拟结果，供动画和报告页面复用 |
| `selected_config` | DamBreakConfig | 全局 | 当前选中的参数配置 |
| `selected_schemes` | List[str] | 全局 | 当前选中的格式列表 |
| `current_page` | str | 全局 | 当前活动页面标识 |

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

    # 初始化会话状态
    if "simulation_results" not in st.session_state:
        st.session_state.simulation_results = {}
    if "selected_config" not in st.session_state:
        st.session_state.selected_config = DamBreakConfig()
    if "selected_schemes" not in st.session_state:
        st.session_state.selected_schemes = ["LF", "LW", "MC", "Godunov", "HLL", "MUSCL"]

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

每个页面是一个独立的 Python 模块，导出 `render()` 函数。页面通过 `st.session_state` 共享状态数据。

**页面组件详细说明**:

| 页面 | 文件 | 核心组件 | 状态读写 |
|------|------|----------|----------|
| 首页 | `home.py` | 理论卡片、公式展示、学习路径 | 只读 |
| 模拟 | `simulation.py` | 参数面板、格式选择器、结果展示 | 读写 `simulation_results`, `selected_config` |
| 动画 | `animation.py` | 动画配置、GIF预览、下载按钮 | 读 `simulation_results` |
| 报告 | `report.py` | 报告配置、生成进度、HTML下载 | 读 `simulation_results` |

---

**① 首页 (`home.py`)**

*职责*: 展示一维溃坝问题的理论背景、数学推导、六种格式对比表和推荐学习路径。

*组件结构*:
```
render()
├── st.header("🌊 一维溃坝问题理论背景")
├── st.markdown("物理描述与工程意义")
├── st.latex("浅水方程推导")
├── st.expander("N-S方程到浅水方程")
├── st.expander("特征线分析")
├── st.dataframe("六种格式对比表")
└── st.columns("学习路径卡片")
```

---

**② 模拟页面 (`simulation.py`)**

*职责*: 提供参数输入、格式选择、模拟运行和结果可视化。

*组件结构*:
```
render()
├── st.header("📊 数值模拟")
├── col_left, col_right = st.columns([1, 2])
│   ├── col_left:
│   │   ├── param_panel.render()      → 返回 DamBreakConfig
│   │   ├── scheme_selector.render()  → 返回 List[str]
│   │   ├── preset_loader.render()    → 加载预设案例
│   │   └── st.button("▶ 开始模拟")
│   └── col_right:
│       ├── progress_bar (运行进度)
│       ├── result_tabs:
│       │   ├── "水深剖面 h(x)" → matplotlib 图表
│       │   ├── "流速剖面 u(x)" → matplotlib 图表
│       │   ├── "误差统计" → st.table(L1/L2/L∞)
│       │   └── "质量守恒" → st.metric(Δm/m₀)
│       └── download_buttons (PNG/CSV)
└── run_simulation(config, schemes) → 调用 SimulationEngine
```

---

**③ 动画页面 (`animation.py`)**

*职责*: 基于模拟结果生成时间演化动画，支持单格式和多格式对比。

*组件结构*:
```
render()
├── st.header("🎬 动画生成")
├── 检查 st.session_state.simulation_results
│   └── 若为空: st.warning("请先在模拟页面运行计算")
├── col_left, col_right = st.columns([1, 2])
│   ├── col_left:
│   │   ├── animation_type_selector  (单格式/多格式/参数扫描)
│   │   ├── fps_slider               (1-30 fps)
│   │   ├── frame_count_slider       (10-100 帧)
│   │   └── st.button("生成动画")
│   └── col_right:
│       ├── animation_preview        (st.image 预览)
│       └── st.download_button       (GIF下载)
└── generate_animation() → 调用 AnimationEngine
```

---

**④ 报告页面 (`report.py`)**

*职责*: 生成包含完整分析的专业 HTML 报告，支持离线下载。

*组件结构*:
```
render()
├── st.header("📝 分析报告")
├── 检查 st.session_state.simulation_results
├── col_left, col_right = st.columns([1, 2])
│   ├── col_left:
│   │   ├── report_template_selector  (简明/详细/学术)
│   │   ├── convergence_settings      (nx序列选择)
│   │   ├── chart_selection           (勾选需要的图表)
│   │   └── st.button("生成报告")
│   └── col_right:
│       ├── report_preview            (HTML iframe预览)
│       └── st.download_button        (HTML下载)
└── generate_report() → 调用 ReportGenerator
```

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

    # 存储结果到会话状态，供其他页面使用
    st.session_state.simulation_results = results
    st.session_state.selected_config = config
    st.session_state.selected_schemes = schemes

    from src.frontend.components import result_viewer
    result_viewer.display(results)
```

#### 3.2.3 业务逻辑引擎 (`engines/`)

**引擎总览**:

| 引擎 | 文件 | 功能 | 依赖模块 |
|------|------|------|----------|
| `SimulationEngine` | `simulation_engine.py` | 协调core模块执行模拟，返回标准化结果 | `core/schemes/`, `core/solvers/`, `core/analysis/` |
| `AnimationEngine` | `animation_engine.py` | 生成GIF/视频动画帧序列 | `matplotlib`, `Pillow` |
| `ReportGenerator` | `report_generator.py` | 生成HTML格式分析报告 | `jinja2`, `matplotlib` |

---

**① SimulationEngine**

*职责*: 接收前端传来的配置和格式列表，协调核心计算模块执行模拟，统一封装结果。

*输入输出*:

| 方向 | 数据 | 类型 | 说明 |
|------|------|------|------|
| 输入 | `config` | DamBreakConfig | 模拟参数配置 |
| 输入 | `scheme_names` | List[str] | 选中的格式名称列表 |
| 输出 | `results` | Dict[str, SimulationResult] | 各格式的模拟结果 |

*处理流程*:
```
run(config, scheme_names):
    results = {}
    scheme_map = {
        "LF": LaxFriedrichsScheme(),
        "LW": LaxWendroffScheme(),
        "MC": MacCormackScheme(),
        "Godunov": GodunovScheme(),
        "HLL": HLLOneScheme(),
        "MUSCL": MUSCLHancockScheme()
    }

    # 构造初始条件
    U0 = initialize_dambreak(config)

    for name in scheme_names:
        scheme = scheme_map[name]

        # 执行时间演化
        start_time = time.time()
        time_history = scheme.evolve(U0, config, progress_callback)
        exec_time = time.time() - start_time

        # 计算精确解 (用于误差对比)
        exact = compute_exact_solution(config.x_grid, config.t_end, config)

        # 计算误差
        final_U = time_history[config.t_end]
        errors = {
            'L1': compute_error(final_U[0], exact[0], p=1, config.dx),
            'L2': compute_error(final_U[0], exact[0], p=2, config.dx),
            'Linf': compute_error(final_U[0], exact[0], p=inf)
        }

        # 质量守恒检查
        mass_error = check_mass_conservation(time_history, config)

        results[name] = SimulationResult(
            config=config,
            scheme_name=name,
            time_history=time_history,
            exact_solution=exact,
            errors=errors,
            execution_time=exec_time,
            mass_conservation_error=mass_error['relative_error']
        )

    return results
```

---

**② AnimationEngine**

*职责*: 将模拟结果的时间序列转换为可视化的 GIF 动画。

*输入输出*:

| 方向 | 数据 | 类型 | 说明 |
|------|------|------|------|
| 输入 | `results` | Dict[str, SimulationResult] | 模拟结果字典 |
| 输入 | `animation_type` | str | 动画类型 (single/multi/scan) |
| 输入 | `fps` | int | 帧率 (1-30) |
| 输入 | `frame_count` | int | 总帧数 |
| 输出 | `gif_bytes` | bytes | GIF 二进制数据 |

*处理流程*:
```
generate_animation(results, animation_type, fps, frame_count):
    if animation_type == "single":
        # 单格式动画
        result = list(results.values())[0]
        frames = extract_frames(result.time_history, frame_count)
        return create_gif(frames, fps)

    elif animation_type == "multi":
        # 多格式对比动画 (2x3 布局)
        frames = []
        for t in selected_time_points:
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            for (name, result), ax in zip(results.items(), axes.flat):
                plot_snapshot(result.time_history[t], ax, title=name)
            frames.append(fig_to_image(fig))
        return create_gif(frames, fps)

    elif animation_type == "scan":
        # 参数扫描动画
        # ... 连续变化某一参数，生成多组模拟结果
        pass
```

---

**③ ReportGenerator**

*职责*: 生成包含完整分析的专业 HTML 报告，支持多种模板。

*输入输出*:

| 方向 | 数据 | 类型 | 说明 |
|------|------|------|------|
| 输入 | `results` | Dict[str, SimulationResult] | 模拟结果字典 |
| 输入 | `template` | str | 报告模板 (brief/detailed/academic) |
| 输入 | `nx_list` | List[int] | 收敛性分析网格序列 |
| 输出 | `html_content` | str | 完整 HTML 字符串 |

*处理流程*:
```
generate_report(results, template, nx_list):
    # 1. 执行收敛性分析 (若提供 nx_list)
    convergence_data = {}
    if nx_list:
        for name in results.keys():
            errors_vs_nx = []
            for nx in nx_list:
                config_nx = replace(config, nx=nx)
                result_nx = run_single_scheme(scheme, config_nx)
                errors_vs_nx.append(result_nx.errors['L1'])
            convergence_data[name] = estimate_order(nx_list, errors_vs_nx)

    # 2. 生成图表 (Base64编码嵌入HTML)
    charts = {
        'h_profile': plot_h_profile(results),
        'u_profile': plot_u_profile(results),
        'error_comparison': plot_error_comparison(results),
        'convergence_plot': plot_convergence(convergence_data, nx_list)
    }

    # 3. 渲染模板
    template_engine = jinja2.Environment(loader=...)
    html = template_engine.get_template(f"{template}.html").render(
        results=results,
        convergence=convergence_data,
        charts=charts,
        generation_time=datetime.now()
    )

    return html
```

---

## 4. 数据结构

### 4.1 守恒变量系统

**守恒变量向量** `U = [h, hu]^T`:

| 变量 | 符号 | 维度 | 物理意义 | 约束条件 |
|------|------|------|----------|----------|
| 水深 | h | [m] | 水面到河床的距离 | h ≥ 0 |
| 动量密度 | hu | [m²/s] | h × u (单位宽度动量) | 无显式约束 |

**原始变量** (由守恒变量导出):

| 变量 | 公式 | 说明 |
|------|------|------|
| 流速 | `u = hu / h` | 当 h > EPS_H 时，否则 u = 0 |
| 波速 | `c = √(g × h)` | 浅水波传播速度 |
| 弗劳德数 | `Fr = u / c` | 判断流态 (亚临界/超临界) |

**通量向量** `F(U) = [hu, hu² + gh²/2]^T`:

| 分量 | 公式 | 物理意义 |
|------|------|----------|
| 质量通量 | `F₁ = hu` | 单位时间通过单位宽度的水体体积 |
| 动量通量 | `F₂ = hu² + gh²/2` | 单位时间通过单位宽度的动量 |

### 4.2 配置数据结构

```python
@dataclass(frozen=True)
class DamBreakConfig:
    """溃坝问题运行参数配置.

    Attributes:
        h_L: 左侧初始水深 [m], 范围 [0.1, 10.0]
        h_R: 右侧初始水深 [m], 范围 [0.0, 10.0], 0表示干底
        u_L: 左侧初始流速 [m/s], 范围 [-5.0, 5.0]
        u_R: 右侧初始流速 [m/s], 范围 [-5.0, 5.0]
        g: 重力加速度 [m/s²], 范围 [0.1, 20.0]
        cfl: CFL稳定性数, 范围 (0, 1.0]
        nx: 网格单元数, 范围 [50, 2000]
        t_end: 终止时间 [s], 范围 [0.1, 10.0]
        x_min: 计算域左边界 [m]
        x_max: 计算域右边界 [m]
    """
    h_L: float = 1.0
    h_R: float = 0.0
    u_L: float = 0.0
    u_R: float = 0.0
    g: float = 9.81
    cfl: float = 0.9
    nx: int = 200
    t_end: float = 0.5
    x_min: float = -5.0
    x_max: float = 5.0
```

### 4.3 结果数据结构

```python
@dataclass
class SimulationResult:
    """单次模拟的标准化结果.

    Attributes:
        config: 本次模拟使用的参数配置
        scheme_name: 使用的数值格式名称
        time_history: 时间演化历史 {时刻t: 解状态U(2×nx)}
        exact_solution: 精确解 (用于误差对比), shape=(2, nx)
        errors: 误差统计 {'L1': float, 'L2': float, 'Linf': float}
        execution_time: 计算耗时 [秒]
        mass_conservation_error: 质量守恒相对误差
    """
    config: DamBreakConfig
    scheme_name: str
    time_history: Dict[float, NDArray[np.float64]]
    exact_solution: Optional[NDArray[np.float64]] = None
    errors: Optional[Dict[str, float]] = None
    execution_time: float = 0.0
    mass_conservation_error: float = 0.0
```

### 4.4 Riemann解数据结构

```python
@dataclass
class RiemannSolution:
    """Riemann问题精确解.

    Attributes:
        h_star: 星区水深
        u_star: 星区流速
        S_L: 左波波速 (稀疏波头或激波速度)
        S_R: 右波波速 (稀疏波头或激波速度)
        wave_type: 波系类型 ('dry_ritter', 'wet_general', 'dry_left')
        S_head_L: 左稀疏波头速度 (仅稀疏波)
        S_tail_L: 左稀疏波尾速度 (仅稀疏波)
        S_head_R: 右稀疏波头速度 (仅稀疏波)
        S_tail_R: 右稀疏波尾速度 (仅稀疏波)
    """
    h_star: float
    u_star: float
    S_L: float
    S_R: float
    wave_type: str
    S_head_L: Optional[float] = None
    S_tail_L: Optional[float] = None
    S_head_R: Optional[float] = None
    S_tail_R: Optional[float] = None
```

### 4.5 收敛性分析数据结构

```python
@dataclass
class ConvergenceResult:
    """收敛性分析结果.

    Attributes:
        scheme_name: 数值格式名称
        nx_list: 网格序列
        errors: 对应误差列表
        estimated_order: 估计收敛阶
        r_squared: 拟合优度 R²
        theoretical_order: 理论收敛阶
    """
    scheme_name: str
    nx_list: List[int]
    errors: List[float]
    estimated_order: float
    r_squared: float
    theoretical_order: int
```

### 4.6 动画配置数据结构

```python
@dataclass
class AnimationConfig:
    """动画生成配置.

    Attributes:
        animation_type: 动画类型 ('single', 'multi', 'scan')
        fps: 帧率 (1-30)
        frame_count: 总帧数 (10-100)
        dpi: 图像分辨率 (100-300)
        show_exact: 是否叠加精确解曲线
        color_scheme: 配色方案
    """
    animation_type: str = "single"
    fps: int = 15
    frame_count: int = 30
    dpi: int = 150
    show_exact: bool = True
    color_scheme: str = "default"
```

---

## 5. 算法设计

### 5.1 初始条件构造算法

```
function initialize_dambreak(config):
    U0 = zeros(2, config.nx)

    for i = 0 to config.nx-1:
        x = config.x_grid[i]

        if x < 0:
            U0[0, i] = config.h_L   # 左侧水深
            U0[1, i] = config.h_L * config.u_L  # 左侧动量
        else:
            U0[0, i] = config.h_R   # 右侧水深
            U0[1, i] = config.h_R * config.u_R  # 右侧动量

    return U0
```

### 5.2 时间演化主循环算法

```
function time_evolution(scheme, U0, config, progress_callback):
    U = U0.copy()
    t = 0.0
    snapshots = {0.0: U.copy()}
    step = 0

    while t < config.t_end:
        # 计算稳定时间步长
        dt = scheme._compute_dt(U, config)
        dt = min(dt, config.t_end - t)  # 确保恰好到达 t_end

        # 执行单步演化 (由各格式子类实现)
        U = scheme._step(U, dt, config)

        # 应用边界条件
        U = scheme._apply_bc(U)

        # 正性保持
        U = scheme._positive_fix(U)

        t += dt
        step += 1

        # 记录快照 (每固定间隔或固定步数)
        if should_record(t, step):
            snapshots[t] = U.copy()

        # 进度回调
        if progress_callback:
            progress_callback(t, config.t_end)

    # 确保最终时刻被记录
    if config.t_end not in snapshots:
        snapshots[config.t_end] = U.copy()

    return snapshots
```

### 5.3 精确解计算算法

```
function compute_exact_solution(x_grid, t, config):
    exact = zeros(2, len(x_grid))

    # 求解初始 Riemann 问题
    U_L = [config.h_L, config.h_L * config.u_L]
    U_R = [config.h_R, config.h_R * config.u_R]
    riemann = exact_riemann_solution(U_L, U_R, config.g)

    for i, x in enumerate(x_grid):
        # 在 (x,t) 处采样 Riemann 解
        xi = x / t  # 自相似变量

        if xi < riemann.S_L:
            # 左状态区
            exact[0, i] = config.h_L
            exact[1, i] = config.h_L * config.u_L
        elif xi > riemann.S_R:
            # 右状态区
            exact[0, i] = config.h_R
            exact[1, i] = config.h_R * config.u_R
        else:
            # 星区或稀疏波内部
            state = sample_riemann_state(xi, riemann, config)
            exact[0, i] = state.h
            exact[1, i] = state.h * state.u

    return exact
```

### 5.4 数值通量计算算法 (通用框架)

```
function compute_numerical_flux(U, config, flux_function):
    F = zeros(2, config.nx - 1)  # 界面通量 (nx-1 个界面)

    for i = 0 to config.nx-2:
        U_L = U[:, i]
        U_R = U[:, i+1]
        F[:, i] = flux_function(U_L, U_R, config.g)

    return F
```

---

## 6. 接口定义

### 6.1 内部API (Core → Frontend)

**Core Engine API 清单**:

| 接口 | 函数签名 | 返回值 | 调用方 |
|------|----------|--------|--------|
| 时间演化 | `BaseScheme.evolve(U0, config, callback)` | `Dict[float, NDArray]` | SimulationEngine |
| 精确Riemann解 | `exact_riemann_solution(U_L, U_R, g)` | `RiemannSolution` | GodunovScheme, exact solver |
| HLL通量 | `hll_flux(U_L, U_R, g)` | `NDArray[shape=(2,)]` | HLLScheme, MUSCLScheme |
| 误差计算 | `compute_error(num, exact, p, dx)` | `float` | SimulationEngine |
| 收敛阶估计 | `estimate_order(nx_list, errors)` | `ConvergenceResult` | ReportGenerator |
| 质量守恒检查 | `check_mass_conservation(history, config)` | `Dict` | SimulationEngine |
| 精确解采样 | `compute_exact_solution(x_grid, t, config)` | `NDArray[shape=(2, nx)]` | SimulationEngine |

**接口详细参数说明**:

**① `BaseScheme.evolve`**

| 参数名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `U0` | NDArray[float64] | shape=(2, nx), U0[0,:] ≥ 0 | 初始守恒变量矩阵 |
| `config` | DamBreakConfig | 已通过校验 | 运行参数配置 |
| `progress_callback` | Callable[[float, float], None] | 可选 | 进度回调函数 `(current_time, end_time)` |
| **返回值** | Dict[float, NDArray] | 键 ≥ 0, 值 shape=(2, nx) | 时间快照字典 |

**② `exact_riemann_solution`**

| 参数名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `U_L` | NDArray[float64] | shape=(2,), U_L[0] ≥ 0 | 左侧守恒变量 [h_L, hu_L] |
| `U_R` | NDArray[float64] | shape=(2,), U_R[0] ≥ 0 | 右侧守恒变量 [h_R, hu_R] |
| `g` | float | g > 0 | 重力加速度 |
| **返回值** | RiemannSolution | - | 包含波速和星区状态的解结构 |

**③ `compute_error`**

| 参数名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `numerical` | NDArray[float64] | shape=(nx,) | 数值解向量 |
| `exact` | NDArray[float64] | shape=(nx,) | 精确解向量 |
| `p` | int | p ∈ {1, 2, inf} | 范数阶数 |
| `dx` | float | dx > 0 | 网格步长 (L1/L2需要) |
| **返回值** | float | ≥ 0 | 误差值 |

### 6.2 外部API (用户通过UI调用)

用户通过Streamlit界面间接调用所有功能，无直接编程API。前端通过以下交互触发后端计算：

| 用户操作 | 触发函数 | 涉及模块 |
|----------|----------|----------|
| 点击"开始模拟" | `SimulationEngine.run()` | core/schemes/, core/solvers/, core/analysis/ |
| 点击"生成动画" | `AnimationEngine.generate()` | matplotlib, Pillow |
| 点击"生成报告" | `ReportGenerator.generate()` | jinja2, matplotlib |
| 调整参数滑块 | `DamBreakConfig` 构造 | config.py |

---

## 7. 测试策略

### 7.1 测试层次

| 测试层次 | 范围 | 工具 | 目标覆盖率 |
|----------|------|------|------------|
| 单元测试 | 单个函数/方法 | pytest | ≥ 80% |
| 集成测试 | 模块间交互 | pytest | 核心流程全覆盖 |
| 系统测试 | 端到端功能 | Streamlit Test Framework | P0需求全覆盖 |
| 回归测试 | 数值结果正确性 | pytest + 基准数据 | 所有格式 |

### 7.2 核心模块测试用例

**① 配置模块测试 (`test_config.py`)**

| 用例ID | 测试内容 | 输入 | 预期结果 |
|--------|----------|------|----------|
| TC-CFG-01 | 合法参数构造 | `h_L=1.0, h_R=0.5, nx=200` | 成功创建对象 |
| TC-CFG-02 | 负水深校验 | `h_L=-1.0` | 抛出 `ConfigValidationError` |
| TC-CFG-03 | CFL越界校验 | `cfl=1.5` | 抛出 `ConfigValidationError` |
| TC-CFG-04 | 网格数不足校验 | `nx=5` | 抛出 `ConfigValidationError` |
| TC-CFG-05 | 域边界校验 | `x_min=5.0, x_max=-5.0` | 抛出 `ConfigValidationError` |
| TC-CFG-06 | 派生属性计算 | `nx=200, x_min=-5, x_max=5` | `dx=0.05`, `x_grid` 长度=200 |
| TC-CFG-07 | 不可变性测试 | 尝试修改 `config.h_L=2.0` | 抛出 `FrozenInstanceError` |

**② 格式模块测试 (`test_schemes.py`)**

| 用例ID | 测试内容 | 输入 | 预期结果 |
|--------|----------|------|----------|
| TC-SCH-01 | LF格式干底溃坝 | `h_L=1.0, h_R=0.0, nx=200` | 无崩溃，h ≥ 0 |
| TC-SCH-02 | Godunov格式湿底溃坝 | `h_L=1.0, h_R=0.5, nx=200` | L∞误差 < 5% |
| TC-SCH-03 | MUSCL格式TVD性质 | 含激波工况 | 总变差不增 |
| TC-SCH-04 | 所有格式质量守恒 | 任意合法参数 | Δm/m₀ < 1e-6 |
| TC-SCH-05 | CFL条件稳定性 | `cfl=0.9, t_end=0.5` | 所有格式不崩溃 |
| TC-SCH-06 | 进度回调触发 | 带回调函数运行 | 回调被多次调用 |
| TC-SCH-07 | 边界条件正确性 | 非对称初始条件 | 边界外推正确 |

**③ Riemann求解器测试 (`test_riemann.py`)**

| 用例ID | 测试内容 | 输入 | 预期结果 |
|--------|----------|------|----------|
| TC-RIE-01 | 湿底Riemann解 | `h_L=1.0, h_R=0.5, u_L=u_R=0` | h_star ∈ (0.5, 1.0) |
| TC-RIE-02 | 干底Riemann解 | `h_L=1.0, h_R=0.0` | 返回 `dry_ritter` 类型 |
| TC-RIE-03 | 对称溃坝 | `h_L=h_R=1.0, u_L=1.0, u_R=-1.0` | u_star ≈ 0 |
| TC-RIE-04 | Newton-Raphson收敛 | 随机湿底工况 | 迭代次数 < 20 |
| TC-RIE-05 | HLL通量对称性 | 交换U_L和U_R | 通量符号相反 |
| TC-RIE-06 | 波速单调性 | 任意工况 | S_L ≤ S_R |

**④ 误差分析测试 (`test_analysis.py`)**

| 用例ID | 测试内容 | 输入 | 预期结果 |
|--------|----------|------|----------|
| TC-ERR-01 | L1误差计算 | 已知精确解和数值解 | 误差值正确 |
| TC-ERR-02 | 收敛阶估计 | nx=[50,100,200,400], error∝nx⁻² | 估计阶 ≈ 2.0 |
| TC-ERR-03 | 一阶格式收敛阶 | LF格式, nx序列 | 估计阶 ≈ 1.0 |
| TC-ERR-04 | 质量守恒检查 | 守恒格式结果 | passed=True |
| TC-ERR-05 | 不足数据异常 | nx_list长度为1 | 抛出 `ValueError` |

**⑤ 前端引擎测试 (`test_engines.py`)**

| 用例ID | 测试内容 | 输入 | 预期结果 |
|--------|----------|------|----------|
| TC-ENG-01 | SimulationEngine单格式 | `config, ["LF"]` | 返回1个结果 |
| TC-ENG-02 | SimulationEngine多格式 | `config, 6种格式` | 返回6个结果 |
| TC-ENG-03 | AnimationEngine单格式 | 单格式结果 | 返回非空bytes |
| TC-ENG-04 | ReportGenerator生成 | 多格式结果 | 返回非空HTML字符串 |

### 7.3 数值回归测试基准

**干底溃坝基准 (Ritter解)**:
- 参数: `h_L=1.0, h_R=0.0, u_L=u_R=0.0, g=9.81, t_end=0.5, nx=200`
- 接受标准: 所有格式 L∞误差(h) < 5%

**湿底溃坝基准**:
- 参数: `h_L=1.0, h_R=0.5, u_L=u_R=0.0, g=9.81, t_end=0.5, nx=200`
- 接受标准: Godunov格式 L∞误差(h) < 3%

### 7.4 测试环境

| 环境 | Python版本 | 用途 |
|------|------------|------|
| CI环境 | 3.10, 3.11 | 自动化测试 (GitHub Actions) |
| 开发环境 | 3.10 | 本地开发调试 |
| 预发布环境 | 3.11 | 发布前验证 |

---

## 8. 错误处理

### 8.1 自定义异常类

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

### 8.2 错误处理策略

| 异常类型 | 触发场景 | 处理方式 |
|---------|---------|---------|
| `ConfigValidationError` | 参数超出范围 | 前端显示友好提示，阻止运行 |
| `NumericalInstabilityError` | CFL过大或激波过强 | 降低CFL自动重试，最多3次 |
| `ConvergenceError` | Riemann迭代不收敛 | 回退到HLL近似求解器 |
| `PositiveDepthViolation` | 干底工况下出现负值 | 应用正性修正(h=max(h, EPS_H)) |

---

*文档结束*
*版本历史*:
- v1.0 (2026-05-07) 初始框架版
- v1.1 (2026-05-09) 完善详细设计：补充模块设计、数据结构、算法设计、接口定义、测试策略
