# CFD-Class Sprint 1 - 完整20个任务Issues批量创建脚本
# =====================================================
# 此脚本将一次性创建Sprint 1的所有20个任务Issues
# 包含: 完整的标题、描述、验收标准、参考文档、标签、指派
#
# 使用方法:
#   1. 先运行 setup_repository.ps1 (如果尚未运行)
#   2. 运行本脚本: .\scripts\create_all_issues.ps1
# =====================================================

$ErrorActionPreference = "Continue"
$repo = "kaklos-cyber/cfd_class"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       CFD-Class Sprint 1 - 批量Issue创建工具 (20个任务)         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ====== 验证环境 ======
$ghCheck = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghCheck) {
    Write-Host "❌ 错误: 未找到 gh CLI" -ForegroundColor Red
    exit 1
}

# ====== 定义20个Issues ======
$allIssues = @(
    # ========== 批次A: 基础设施 (@PM) ==========
    @{
        title = "chore: 配置main/develop分支保护规则 (#A1)"
        body = @"
## 任务描述
配置GitHub仓库的分支保护规则，确保代码质量和团队协作规范。

## 具体步骤

### main分支保护 (生产分支):
- [ ] **Require a pull request before merging**: ✅ 开启
- [ ] **Require approvals**: **2人审核通过** (PM + Arch)
- [ ] **Dismiss stale PR approvals**: ✅ 开启 (新commit需重新审核)
- [ ] **Require status checks to pass**: ✅ 开启
  - 必须通过的检查项: `ci/test`, `ci/lint`
- [ ] **Do not allow bypassing**: ✅ 开启
- [ ] **Include administrators**: ✅ 开启 (管理员也需遵守)
- [ ] **Allow force pushes**: ❌ 关闭
- [ ] **Allow deletions**: ❌ 关闭

### develop分支保护 (开发集成分支):
- [ ] **Require PR**: ✅ 开启
- [ ] **Require approvals**: **1人审核通过**
- [ ] **Require status checks**: `ci/test`
- [ ] **Allow force pushes**: ❌ 关闭
- [ ] **Allow deletions**: ❌ 关闭

## 验收标准
- [ ] main分支无法直接push（必须走PR流程）
- [ ] develop分支PR需至少1人审核
- [ ] CI检查未通过时无法合并

## 参考文档
GITHUB_COLLABORATION_GUIDE.md §1.3 分支保护规则配置
PRODUCT_DELIVERY_STANDARD.md §三 仓库架构
"@
        labels = "chore,priority/critical,module/infrastructure"
        assignees = @("PM")
    },
    @{
        title = "chore: 创建完整Labels标签体系(12个) (#A2)"
        body = @"
## 任务描述
在仓库 Settings → Labels 中创建以下完整的标签体系。

### 类型标签 (kind/*) - 5个
| 标签名 | 颜色 | 描述 | 使用场景 |
|--------|------|------|---------|
| `kind/bug` | 🔴 #e11d21 | 软件缺陷 | 发现Bug时 |
| `kind/enhancement` | 🟣 #a855f7 | 新功能建议 | 提出新功能时 |
| `kind/docs` | 🔵 #0075ff | 文档相关 | 文档工作时 |
| `kind/refactor` | 🟡 #fbca04 | 代码重构 | 重构代码时 |
| `kind/testing` | 🟢 #2ea44f | 测试相关 | 测试相关 |

### 优先级标签 (priority/*) - 4个
| 标签名 | 颜色 | 含义 | 响应时间 |
|--------|------|------|---------|
| `priority/critical` | ❤️ #d73a49 | P0-紧急 | 立即处理(15min)|
| `priority/high` | 🟠 #ff7b00 | P1-高 | 48小时内 |
| `priority/medium` | 🔵 #1d9ce0 | P2-中 | 本Sprint内 |
| `priority/low` | ⚪ #909399 | P3-低 | 有空再做 |

### 模块标签 (module/*) - 5个
| 标签名 | 对应目录 |
|--------|---------|
| `module/core` | src/core/ (核心引擎) |
| `module/ui` | src/frontend/ (用户界面) |
| `module/tests` | tests/ (测试代码) |
| `module/docs` | docs/ (产品文档) |
| `module/infrastructure` | .github/, scripts/ (CI/CD) |

### 状态标签 (status/*) - 3个
| 标签名 | 含义 |
|--------|------|
| `status/in-progress` | 正在实施中 |
| `status/review` | 待Code Review |
| `status/blocked` | 被阻塞(需注明原因) |

## 验收标准
- [ ] 总共12个标签全部创建成功
- [ ] 每个标签颜色和描述正确
- [ ] 新建Issue时可正常选择这些标签

## 参考文档
GITHUB_COLLABORATION_GUIDE.md §4.2 Issue标签体系
"@
        labels = "chore,priority/high,module/infrastructure"
        assignees = @("PM")
    },
    @{
        title = "chore: 邀请5位团队成员并分配权限 (#A3)"
        body = @"
## 任务描述
邀请6人团队中的其他5位成员加入GitHub仓库，并分配相应权限。

### 成员列表与权限矩阵

| 角色 | GitHub账号 | 权限级别 | 可执行操作 |
|------|-----------|---------|-----------|
| 架构师 @Arch | *(待填写)* | **Admin** | 所有操作+合并到main |
| 后端开发 @BE | *(待填写)* | **Write** | Push/PR/Issue |
| 前端开发 @FE | *(待填写)* | **Write** | Push/PR/Issue |
| 测试工程师 @QA | *(待填写)* | **Write** | Push/PR/Issue |
| 文档工程师 @TW | *(待填写)* | **Write** | Push/PR/Issue |

> **注意**: PM(@你) 已经是Owner/Admin，无需重复添加。

### 操作步骤
1. 访问 https://github.com/kaklos-cyber/cfd_class/settings/access
2. 点击 **"Add people"** 按钮
3. 输入成员的GitHub用户名（一次可输入多个）
4. 选择权限角色:
   - @Arch → 选择 **Admin**
   - 其他人 → 选择 **Write**
5. 点击 **Invite**
6. 等待所有成员接受邀请（通常需要几分钟到几小时）

### 验证方法
- [ ] 在 Collaborators 列表中看到所有6位成员
- [ ] 每位成员的状态显示为 "Accepted" (非 Pending)
- [ ] 各成员权限级别正确显示

## 注意事项
- ⚠️ 如果成员还没有GitHub账号，请先让他们注册
- ⚠️ 推荐使用组织(Organization)方式管理团队（后续升级）
- ⚠️ 邀请后请在微信群通知大家接受邀请
"@
        labels = "chore,priority/critical,module/infrastructure"
        assignees = @("PM")
    },
    @{
        title = "docs: 建立GitHub Projects Sprint 1看板 (#A4)"
        body = @"
## 任务描述
创建 GitHub Project 看板用于可视化管理和跟踪 Sprint 1 的所有任务。

### 看板设计

#### 项目信息
```
名称: CFD-Class Sprint 1
类型: Team managed (推荐)
可见性: Private (仅成员可见)
```

#### 看板列定义 (5列)

| 列名 | 图标 | 用途 | WIP限制 | 过滤条件 |
|------|------|------|---------|----------|
| **Backlog** | 📋 | 待办任务池 | 无限 | 无 |
| **In Progress** | ⚙️ | 进行中的任务 | **≤3** | `status:in-progress` |
| **Review** | 👀 | 待Code Review | **≤5** | `status:review` |
| **Testing** | 🧪 | QA测试中 | 无限 | 无 |
| **Done** | ✅ | 已完成 | 无限 | 无 |

#### 自动化规则 (可选)
```
当 Issue 被添加到 "In Progress" 时:
  → 自动添加标签: status/in-progress
  
当 Issue 被添加到 "Review" 时:
  → 自动添加标签: status/review
  
当 Issue 被添加到 "Done" 时:
  → 自动移除 status/in-progress 和 status/review
```

### 创建步骤
1. 访问 https://github.com/kaklos-cyber/cfd_class/projects/new
2. 选择 **"Team managed"** 类型
3. 填写:
   - Name: `CFD-Class Sprint 1`
   - Description: `一维溃坝CFD教学软件 Sprint 1 任务看板`
   - Visibility: `Private`
4. 在 Views 中选择 **"Board"** 视图
5. 手动添加上述5个列 (Columns)
6. (可选) 设置自动化规则 (Automation)

### 将Issues添加到看板
创建完看板后，有两种方式添加Issues:

**方式1: 单个Issue添加**
- 打开任意Issue页面
- 在右侧边栏找到 **"Projects"** 下拉框
- 选择 `CFD-Class Sprint 1`
- Issue自动出现在 Backlog 列

**方式2: 批量添加**
- 进入Project页面
- 点击 **"+"** 或 **"Add items"**
- 选择 **"Issues"**
- 批量勾选要添加的Issues
- 确认添加

### 验收标准
- [ ] Project看板创建成功且可见
- [ ] 5个列已正确配置
- [ ] 可以拖拽Issue在不同列之间移动
- [ ] 至少将 A1-A3 Issues 添加到 Done 列

## 参考文档
GITHUB_COLLABORATION_GUIDE.md §4.3 Projects看板管理
"@
        labels = "docs,priority/high,module/infrastructure"
        assignees = @("PM")
    },

    # ========== 批次B: 核心引擎 (@BE) ==========
    @{
        title = "feat(core): 实现 DamBreakConfig frozen dataclass (#B1)"
        body = @"
## 功能概述
实现 `DamBreakConfig` 数据类，统一管理一维溃坝问题的所有运行参数。

这是整个项目的**基础组件**，所有格式、UI、测试都依赖它。

## 技术要求

### 文件位置
`src/core/config.py`

### 类设计 (使用 dataclass)
```python
from dataclasses import dataclass, field
from typing import Final
import numpy as np
from numpy.typing import NDArray

@dataclass(frozen=True)  # 冻结: 创建后不可修改
class DamBreakConfig:
    """一维溃坝问题运行参数配置.
    
    使用 frozen dataclass 确保:
    - 配置不可变 (防止运行时意外修改)
    - 可作为字典键使用 (hashable)
    - 支持类型提示和IDE自动补全
    
    Attributes:
        h_L: 左侧初始水深 [m], 范围 [0.1, 10.0]
        h_R: 右侧初始水深 [m], 范围 [0.0, 10.0] (0=干底)
        u_L: 左侧初始流速 [m/s], 范围 [-5.0, 5.0]
        u_R: 右侧初始流速 [m/s], 范围 [-5.0, 5.0]
        g: 重力加速度 [m/s²], 范围 [0.1, 20.0], 默认9.81
        cfl: CFL稳定性系数, 范围 (0.1, 0.95], 默认0.9
        nx: 网格单元数, 范围 [50, 2000], 默认200
        t_end: 终止时间 [s], 范围 [0.1, 10.0], 默认0.5
        x_min: 左边界坐标 [m], 默认-5.0
        x_max: 右边界坐标 [m], 默认5.0
    """
    
    # ===== 物理参数 ======
    h_L: float = 1.0
    h_R: float = 0.0
    u_L: float = 0.0
    u_R: float = 0.0
    g: float = 9.81
    
    # ===== 数值参数 ======
    cfl: float = 0.9
    nx: int = 200
    t_end: float = 0.5
    
    # ===== 域参数 ======
    x_min: float = -5.0
    x_max: float = 5.0
    
    def __post_init__(self) -> None:
        """参数合法性校验."""
        if self.h_L <= 0:
            raise ValueError(f"h_L must be positive, got {self.h_L}")
        if self.h_R < 0:
            raise ValueError(f"h_R must be non-negative, got {self.h_R}")
        if self.cfl <= 0 or self.cfl > 1.0:
            raise ValueError(f"CFL must be in (0, 1], got {self.cfl}")
        if self.nx < 10:
            raise ValueError(f"nx must be >= 10, got {self.nx}")
        if self.t_end <= 0:
            raise ValueError(f"t_end must be positive, got {self.t_end}")
        if self.x_min >= self.x_max:
            raise ValueError(f"x_min ({self.x_min}) must be < x_max ({self.x_max})")
    
    @property
    def dx(self) -> float:
        """网格步长 [m]."""
        return (self.x_max - self.x_min) / self.nx
    
    @property
    def x_grid(self) -> NDArray[np.float64]:
        """网格节点坐标数组 (单元中心), shape=(nx,)."""
        return np.linspace(
            self.x_min + self.dx / 2,
            self.x_max - self.dx / 2,
            self.nx
        )
```

## 验收标准 (Acceptance Criteria)

### 功能性 (Must Have)
- [ ] 可以使用默认值实例化: `config = DamBreakConfig()`
- [ ] 可以自定义参数实例化: `config = DamBreakConfig(h_L=2.0, nx=500)`
- [ ] **Frozen属性**: 尝试修改任何属性抛出 `FrozenInstanceError`
- [ ] `dx` 属性返回正确的浮点数: `(x_max-x_min)/nx`
- [ ] `x_grid` 屔回长度为 `nx` 的等间距 numpy 数组
- [ ] `x_grid[0]` ≈ `x_min + dx/2`, `x_grid[-1]` ≈ `x_max - dx/2`

### 参数校验 (Must Have)
- [ ] `h_L ≤ 0` → 抛出 `ValueError` ("h_L must be positive...")
- [ ] `h_R < 0` → 抛出 `ValueError` ("h_R must be non-negative...")
- [ ] `CFL > 1.0` → 抛出 `ValueError` ("CFL must be in (0, 1]...")
- [ ] `CFL ≤ 0` → 抛出 `ValueError`
- [ ] `nx < 10` → 抛出 `ValueError` ("nx must be >= 10...")
- [ ] `t_end ≤ 0` → 抛出 `ValueError`
- [ ] 错误消息清晰易懂，包含实际值和建议范围

### 类型安全 (Should Have)
- [ ] 通过 mypy 类型检查 (`mypy src/core/config.py`)
- [ ] 所有属性有正确的类型注解
- [ ] 返回值类型注解完整 (dx→float, x_grid→NDArray)

### 性能 (Nice to Have)
- [ ] 实例化耗时 < 1ms (10000次循环测试)
- [ ] 内存占用 < 1KB per instance

## 测试用例清单 (供@QA参考)

```python
def test_default_values():
    config = DamBreakConfig()
    assert config.h_L == 1.0
    assert config.h_R == 0.0
    assert config.cfl == 0.9
    assert config.nx == 200

def test_custom_values():
    config = DamBreakConfig(h_L=2.0, h_R=0.5, nx=100)
    assert config.h_L == 2.0
    assert config.h_R == 0.5
    assert config.nx == 100
    assert abs(config.dx - 0.1) < 1e-10

def test_frozen():
    config = DamBreakConfig()
    try:
        config.h_L = 999  # 应该失败
        assert False, "应该抛出 FrozenInstanceError"
    except AttributeError:
        pass  # 预期行为

def test_validation_h_L_negative():
    try:
        DamBreakConfig(h_L=-1.0)
        assert False, "应该抛出 ValueError"
    except ValueError as e:
        assert "positive" in str(e).lower()

def test_dx_property():
    config = DamBreakConfig(x_min=0, x_max=10, nx=100)
    assert abs(config.dx - 0.1) < 1e-10

def test_x_grid():
    config = DamBreakConfig(x_min=0, x_max=10, nx=5)
    grid = config.x_grid
    assert len(grid) == 5
    assert abs(grid[0] - 1.0) < 1e-10  # 0 + 0.1
    assert abs(grid[-1] - 9.0) < 1e-10  # 10 - 0.1

def test_extreme_params():
    config = DamBreakConfig(h_L=10.0, h_R=0.001, g=20.0, cfl=0.95, nx=2000, t_end=10.0)
    assert config is not None  # 不应报错
```

## 参考文档
- SDD.md §3.1.1 配置模块设计
- SRS.md §FR-05.10 核心引擎需求
- CONTRIBUTING.md §7 编码规范
"@
        labels = "feat,priority/high,module/core,status/in-progress"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现精确Riemann求解器 (湿底+干底) (#B2)"
        body = @"
## 功能概述
实现一维浅水方程(Saint-Venant方程组)的**精确Riemann求解器**。

支持两种情况:
1. **湿底情况** (h_L > 0 且 h_R > 0): 使用 Newton-Raphson 迭代求解星区非线性方程
2. **干底情况** (h_R ≈ 0): 使用 Ritter (1892) 解析解

这是项目中最关键的算法之一，所有 Godunov 格式都依赖它。

## 数学背景

### 控制方程 (一维浅水方程)
$$
\frac{\partial \mathbf{U}}{\partial t} + \frac{\partial \mathbf{F}(\mathbf{U})}{\partial x} = 0
$$

其中守恒变量 $\mathbf{U} = [h, hu]^T$，通量 $\mathbf{F} = [hu, hu^2 + \frac{1}{2}gh^2]^T$

### Riemann问题定义
初始条件 ($t=0$):
$$
\mathbf{U}(x,0) = \begin{cases}
\mathbf{U}_L = [h_L, hu_L]^T & x < 0 \\
\mathbf{U}_R = [h_R, hu_R]^T & x > 0
\end{cases}$$

### 波系结构 (四区)
```
          S_L      S_*     S_R
    ┌─────┬──────┬──────┬─────┐
    │  L  │ Fan  │ *   │ R  │
    │     │      │     │    │
    └─────┴──────┴──────┴─────┘
         ←-----←-------→ x=0
```
- L区: 未扰动的左状态 $(h_L, u_L)$
- Fan区: 稀疏波扇区 (连续变化)
- *区: 星区 (恒定状态 $(h_*, u_*)$
- R区: 未扰动的右状态 $(h_R, u_R)$
- $S_L$: 左波速 (稀疏波头或激波速度)
- $S_*$: 星区接触间断速度
- $S_R$: 右波速 (稀疏波尾或激波速度)

## API接口设计

### 文件位置
`src/core/solvers/exact_solution.py`

### 主函数签名
```python
def exact_riemann_solution(
    U_L: NDArray[np.float64],   # shape=(2,) 左侧守恒变量 [h_L, hu_L]
    U_R: NDArray[np.float64],   # shape=(2,) 右侧守恒变量 [h_R, hu_R]
    g: float,                     # 重力加速度 [m/s²]
    tol: float = 1e-10,           # Newton迭代容差
    max_iter: int = 50             # 最大迭代次数
) -> dict:
    """返回精确Riemann解的完整信息.

    Returns:
        dict {
            'S_L': float,           # 左波速度 [m/s]
            'S_R': float,           # 右波速度 [m/s]
            'S_star': float,        # 星区接触间断速度 [m/s]
            'h_star': float,        # 星区水深 [m]
            'u_star': float,        # 星区流速 [m/s]
            'type': str,            # 波系类型标识:
                                    # 'dry_ritter' - 干底Ritter解
                                    # 'wet_left_shock' - 左激波
                                    # 'wet_right_shock' - 右激波
                                    # 'wet_left_rarefaction' - 左稀疏波
                                    # 'wet_right_rarefaction' - 右稀疏波
                                    # 'wet_two_rarefactions' - 双稀疏波
            'star_region_left': dict,   # 左星区状态 {'h': , 'u': }
            'star_region_right': dict,  # 右星区状态{'h': , 'u': }
        }
    """
```

### 辅助函数 (内部使用)
```python
def _compute_star_state_h(
    h_L: float, u_L: float,
    h_R: float, u_R: float,
    g: float
) -> tuple[float, float]:
    """给定左右状态，计算星区水深h*和u* (仅依赖h*的非线性方程).
    
    使用Newton-Raphson迭代求解:
        f(h*) = φ_L(h*) - φ_R(h*) = 0
    其中 φ(h) = 
        { 2(√(gh) - √(gh_L))  if h > h_L (左稀疏波)
        { 2√(gh)               if h_L ≤ h ≤ h_R (无穿越)
        { 2(√(gh_L) - √(gh))  if h < h_L (右稀疏波)
    """

def _classify_wave_structure(
    h_star: float, u_star: float,
    h_L: float, u_L: float,
    h_R: float, u_R: float,
    g: float
) -> str:
    """根据星区状态判断波系类型."""

def _ritter_dry_bed_solution(
    h_L: float, u_L: float,
    g: float, x: float, t: float
) -> tuple[float, float]:
    """Ritter (1892) 干底解析解.
    
    对于 h_R = 0, u_R = 0 的特殊情况:
    - 稀疏波扇区: h(x/t) = (1/g)*(u_L - x/(2t))²
    - 波速: S_L = u_L - √(gh_L), S_* = u_L/3 + 2√(gh_L)/3
    """
```

## 实现要点

### 1. 干底情况 (h_R ≈ 0)
```python
if h_R < EPS_DRY:  # EPS_DRY = 1e-6
    # 使用Ritter解析解
    if u_L >= 0:  # 向右扩展
        S_L = u_L - np.sqrt(g * h_L)
        S_R = u_L / 3.0 + 2.0 * np.sqrt(g * h_L) / 3.0
        type_str = "dry_ritter_right"
    else:  # 向左扩展 (u_L < 0)
        # ... 对称情况
```

### 2. 湿底情况 (h_L > 0 且 h_R > 0)
```python
else:
    # Step 1: 计算初始猜测 h*_0
    h_star_0 = (h_L + h_R) / 2.0  # 简单平均作为初值
    
    # Step 2: Newton-Raphson迭代
    for i in range(max_iter):
        f_val = phi_L(h_star) - phi_R(h_star)
        f_deriv = dphi_L(h_star) - dphi_R(h_star)
        
        if abs(f_val) < tol or abs(f_deriv) < 1e-14:
            break
        
        delta = f_val / f_deriv
        h_star = h_star - delta
        
        # 安全检查: h*不能为负
        if h_star < 0:
            h_star = EPS_H  # 重置为小正数
    
    # Step 3: 计算u*
    u_star = 0.5 * (u_L + u_R) + np.sqrt(g * h_L) - np.sqrt(g * h_star)
    
    # Step 4: 计算波速
    c_star = np.sqrt(g * h_star)
    S_L = min(u_L - np.sqrt(g * h_L), u_star - c_star)
    S_R = max(u_R + np.sqrt(g * h_R), u_star + c_star)
    
    # Step 5: 分类波系结构
    wave_type = _classify_wave_structure(...)
```

## 验收标准

### 正确性验证 (Must Have)
- [ ] **湿底案例1** (h_L=1.0, h_R=0.5, u_L=u_R=0):
  - 与 Toro (2009) Table 6.1 结果一致 (误差<1e-6)
  - h* ≈ 0.718 (理论值)
  - u* ≈ 0.202 (理论值)
  
- [ ] **湿底案例2** (h_L=1.0, h_R=0.1, u_L=u_R=0):
  - 出现右激波 (h_R < h*)
  - S_R > 0 (向右传播)
  
- [ ] **干底案例** (h_L=1.0, h_R=0.0, u_L=u_R=0):
  - 与Ritter解析解完全一致 (误差<1e-10)
  - h(x,t) = (1/g)*(u_L - x/(2t))² (扇区内)
  
- [ ] **极限情况** (h_L = h_R):
  - 返回均匀流解 (S_L=S_R=u*, h*=h_L=h_R)
  
- [ ] **超临界流** (Froude数 > 1):
  - 不崩溃，结果合理

### 收敛性验证 (Must Have)
- [ ] Newton迭代通常在 **<10次** 内收敛
- [ ] 对各种参数组合不发散
- [ ] 初值鲁棒性好 (即使初值偏差较大也能收敛)

### 性能验证 (Should Have)
- [ ] 单次调用耗时 **< 1ms** (典型参数)
- [ ] 支持 numpy array 向量化输入 (批量计算)
- [ ] 内存占用合理 (< 1KB per call)

### 测试覆盖率 (Must Have)
- [ ] 单元测试 ≥ 15 个测试用例
- [ ] 覆盖: 干底/湿底、均匀流、极端参数、边界情况
- [ ] 语句覆盖率 ≥ 90%

## 参考资料
1. Toro, E.F. "Riemann Solvers and Numerical Methods for Fluid Dynamics", Chapter 4, Springer, 2009
2. George, D.L. "Finite Volume Methods for Hyperbolic Problems", Chapter 13-14, Cambridge, 2008
3. LeVeque, R.J. "Numerical Methods for Conservation Laws", Chapter 13, Birkhäuser, 2002
4. SDD.md §3.1.4 Riemann求解器设计
5. SRS.md §FR-05.02 精确Riemann求解器需求
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现HLL近似Riemann通量 (#B3)"
        body = @"
## 功能概述
实现 HLL (Harten-Lax-van Leer) 两波近似 Riemann 通量计算。

HLL是一种**近似Riemann求解器**，通过估计左右波速来近似通量，避免精确求解的高昂计算成本。

## HLL公式

### 通量公式
$$
\mathbf{F}_{HLL} = \frac{S_R^+ \mathbf{F}_L - S_L^- \mathbf{F}_R + S_R^+ S_L^- (\mathbf{U}_R - \mathbf{U}_L)}{S_R^+ - S_L^-}$$

其中:
- $S_L^+ = \max(S_L, 0)$, $S_L^- = \min(S_L, 0)$
- $S_R^+ = \max(S_R, 0)$, $S_R^- = \min(S_R, 0)$
- $\mathbf{F}_L$, $\mathbf{F}_R$: 左右界面的物理通量
- $\mathbf{U}_L$, $\mathbf{U}_R$: 左右守恒变量

### 波速估计 (Davis Einfeld估计)
$$
\begin{aligned}
S_L &= \min(u_L - c_L,\; u_R - c_R) \\
S_R &= \max(u_L + c_L,\; u_R + c_R)
\end{aligned}$$

其中局部波速 $c = \sqrt{gh}$

## API接口

### 文件位置
`src/core/solvers/riemann_solver.py` (与精确求解器同文件)

### 函数签名
```python
def hll_flux(
    U_L: NDArray[np.float64],   # shape=(2,) 左侧守恒变量 [h_L, hu_L]
    U_R: NDArray[np.float64],   # shape=(2,) 右侧守恒变量 [h_R, hu_R]
    g: float                      # 重力加速度 [m/s²]
) -> NDArray[np.float64]:       # shape=(2,) HLL近似通量向量 [F_mass, F_momentum]
    """计算HLL两波近似Riemann通量.
    
    Args:
        U_L: 左侧守恒变量 (水深, 动量密度)
        U_R: 右侧守恒变量
        g: 重力加速度
        
    Returns:
        HLL通量向量 [F₁, F₂] 对应 [hu, hu²+gh²/2]
    """
```

## 实现代码框架
```python
def hll_flux(U_L, U_R, g):
    # 解包守恒变量
    h_L, hu_L = U_L[0], U_L[1]
    h_R, hu_R = U_R[0], U_R[1]
    
    # 计算原始变量
    u_L = hu_L / h_L if h_L > EPS else 0.0
    u_R = hu_R / h_R if h_R > EPS else 0.0
    
    # 局部波速
    c_L = sqrt(g * h_L) if h_L > EPS else 0.0
    c_R = sqrt(g * h_R) if h_R > EPS else 0.0
    
    # Davis波速估计
    S_L = min(u_L - c_L, u_R - c_R)
    S_R = max(u_L + c_L, u_R + c_R)
    
    # 计算物理通量
    F_L = compute_physical_flux(U_L, g)  # [hu_L, hu_L² + gh_L²/2]
    F_R = compute_physical_flux(U_R, g)  # [hu_R, hu_R² + gh_R²/2]
    
    # HLL通量公式
    SL_p = max(S_L, 0.0)
    SL_n = min(S_L, 0.0)
    SR_p = max(S_R, 0.0)
    SR_n = min(S_R, 0.0)
    
    denom = SR_p - SL_n
    if abs(denom) < 1e-14:
        # 退化情况: 返回平均通量
        return 0.5 * (F_L + F_R)
    
    F_hll = (
        SR_p * F_L - SL_n * F_R + SR_p * SL_n * (U_R - U_L)
    ) / denom
    
    return F_hll
```

## HLL vs 精确Riemann对比

| 特性 | 精确Riemann | HLL近似 |
|------|-------------|---------|
| 精度 | ★★★★★ (精确) | ★★★☆☆ (近似) |
| 速度 | 慢 (需迭代) | **快** (显式公式) |
| 复杂度 | 高 (需分类讨论) | **低** (统一公式) |
| 稳定性 | 强稳定 | **强稳定** |
| 适用场景 | Godunov格式基准 | **HLL格式、工程实用首选** |
| CPU成本 | ~10x | **1x (基线)** |

## 验收标准

### 正确性 (Must Have)
- [ ] 光滑区域: HLL通量与精确通量的差异 < 5%
- [ ] 间断处: 能捕捉激波位置（可能有一定耗散）
- [ ] 均匀流: 当 U_L = U_R 时，返回精确通量
- [ ] 保恒性: HLL通量满足熵条件 (entropy-satisfying)

### 鲁棒性 (Must Have)
- [ ] 干底工况 (h_R=0): 不崩溃，返回合理通量
- [ ] 湿底工况 (h_L>>h_R): 不崩溃
- [ ] 超声速流 (u >> c): 不崩溃
- [ ] 极端参数: CFL接近1时不崩溃

### 性能 (Should Have)
- [ ] 单次调用 < 0.01ms (比精确求解器快100倍以上)
- [ ] 支持批量输入 (shape=(N, 2))
- [ ] 无内存泄漏

### 测试 (Must Have)
- [ ] ≥ 10 个单元测试用例
- [ ] 覆盖: 光滑/间断/均匀流/干底/湿底/极端参数
- [ ] 与精确求解器的对比测试 (误差在合理范围内)

## 参考资料
- Harten, Lax, van Leer (1983) "On Upstream Differencing and Godunov-Type Schemes for Hyperbolic Conservation Laws"
- Toro (2009) Chapter 10
- SDD.md §3.1.4
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现BaseScheme抽象基类 (#B4)"
        body = @"
## 功能概述
定义所有有限体积格式的**抽象基类 BaseScheme**，统一接口和公共逻辑。

这是**面向对象设计**的核心：6种具体格式(LF/LW/MC/Godunov/HLL/MUSCL)都将继承此类。

## 设计模式

采用 **Template Method (模板方法)** 设计模式：
- BaseScheme 定义算法骨架 (_compute_dt, _apply_bc, enforce_positivity)
- 子类只需实现具体的数值通量计算 (_compute_numerical_flux)
- 公共逻辑复用，避免代码重复

## 类层次结构
```
BaseScheme (ABC)           ← 抽象基类
├── LaxFriedrichsScheme     ← 一阶粘性格式
├── LaxWendroffScheme       ← 二阶中心格式
├── MacCormackScheme         ← 二阶预测校正
├── GodunovScheme           ← 精确Riemann格式
├── HLLOneScheme           ← HLL近似格式
└── MUSCLHancockScheme      ← 二阶TVD格式
```

## API接口 (完整定义)

### 文件位置
`src/core/schemes/base_scheme.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable
import numpy as np
from numpy.typing import NDArray

# 导入配置类 (将在B1中实现)
# from src.core.config import DamBreakConfig  
# 这里先用类型注解代替，避免循环依赖

class BaseScheme(ABC):
    """有限体积格式抽象基类.
    
    所有数值格式必须继承此类并实现 evolve() 方法。
    提供统一的接口供上层 SimulationEngine 调用。
    
    Attributes:
        name (str): 格式名称，如 "Lax-Friedrichs"
        order (int): 空间精度阶数 (1或2)
        tvd (bool): 是否具有总变差衰减(TVD)性质
    """
    
    def __init__(
        self,
        name: str,
        order: int,
        tvd: bool = False
    ) -> None:
        """初始化格式实例.
        
        Args:
            name: 格式名称 (如 "Lax-Friedrichs", "MUSCL-Hancock")
            order: 空间精度阶数 (1=一阶, 2=二阶)
            tvd: 是否为TVD格式 (默认False)
            
        Raises:
            ValueError: order 不是 1 或 2
            TypeError: name 不是字符串
        """
        if order not in (1, 2):
            raise ValueError(f"order must be 1 or 2, got {order}")
        if not isinstance(name, str):
            raise TypeError(f"name must be string, got {type(name)}")
            
        self.name = name
        self.order = order
        self.tvd = tvd

    @abstractmethod
    def evolve(
        self,
        U0: NDArray[np.float64],
        config: object,  # DamBreakConfig (延迟导入避免循环依赖)
        progress_callback: Optional[Callable[[float, float], None]] = None
    ) -> Dict[float, NDArray[np.float64]]:
        """执行时间演化计算 (核心接口).
        
        这是唯一的抽象方法，子类必须实现。
        
        Args:
            U0: 初始守恒变量矩阵, shape=(2, nx)
                U[0, :] = h (水深)
                U[1, :] = hu (动量密度)
            config: DamBreakConfig 运行参数配置
            progress_callback: 进度回调函数 callback(current_time, end_time)
                用于前端进度条显示
                
        Returns:
            Dict[float, NDArray]: 字典 {时刻t: 解状态U(2×nx)}
            包含 t=0 (初始条件) 和 t=t_end (最终状态) 以及中间快照
            
        Raises:
            ValueError: 输入参数不合法
            NotImplementedError: 子类未实现
        """
        pass

    def _compute_dt(
        self,
        U: NDArray[np.float64],
        config: object
    ) -> float:
        """基于CFL条件计算稳定时间步长.
        
        使用最大特征速度 λ_max = |u| + c 来确定dt:
        dt = CFL × dx / λ_max
        
        Returns:
            float: 时间步长 [秒]
        """
        h = U[0, :]
        u = np.where(h > 1e-12, U[1, :] / h, 0.0)
        c = np.sqrt(getattr(config, 'g', 9.81) * np.maximum(h, 1e-12))
        lambda_max = np.max(np.abs(u) + c)
        dx = getattr(config, 'dx', 0.1)  # 将从config获取
        cfl = getattr(config, 'cfl', 0.9)
        return cfl * dx / lambda_max

    def _apply_bc(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """应用透射边界条件 (零梯度外推).
        
        左边界: U[:, 0] = U[:, 1]
        右边界: U[:, -1] = U[:, -2]
        
        Returns:
            U: 应用BC后的守恒变量矩阵
        """
        U[:, 0] = U[:, 1]
        U[:, -1] = U[:, -2]
        return U

    def _enforce_positivity(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """正性保持机制: 防止负水深.
        
        干底工况下可能出现数值负水深，
        此方法将其修正为小正数 (EPS_H = 1e-12)。
        
        Returns:
            U: 修正后的守恒变量矩阵 (h ≥ EPS_H)
        """
        U[0, :] = np.maximum(U[0, :], 1e-12)
        return U

    def _record_snapshot(
        self,
        snapshots: Dict[float, NDArray],
        t: float,
        U: NDArray[np.float64],
        config: object
    ) -> None:
        """记录当前时刻的解状态快照 (可选优化).
        
        默认记录: t=0, t_end, 以及 t_end/2, t_end/4 等
        可根据 config.t_end 和 config.nx 自适应调整记录频率。
        """
        snapshots[t] = U.copy()
```

## 公共方法说明

| 方法 | 用途 | 子类是否可覆盖 |
|------|------|----------------|
| `evolve()` | **抽象方法** - 必须实现 | ✅ 必须 |
| `_compute_dt()` | CFL自适应时间步 | ❌ 通常不需要 |
| `_apply_bc()` | 透射边界条件 | ❌ 通常不需要 |
| `_enforce_positivity()` | 正性保持 | ⚠️ 仅特殊格式 |
| `_record_snapshot()` | 快照记录 | ✅ 可以覆盖 |

## 设计原则

1. **单一职责**: BaseScheme只负责算法骨架，不通晓具体通量公式
2. **开闭原则**: 对扩展开放(B5-B10继承)，对修改关闭(公共逻辑固定)
3. **依赖倒置**: 依赖 DamBreakConfig 和 exact_riemann_solution (通过参数注入)
4. **好莱坞原则**: 子类只重写必须改变的部分 (_compute_numerical_flux)

## 验收标准

### 接口契约 (Must Have)
- [ ] 无法直接实例化 BaseScheme (尝试实例化应抛出 TypeError)
- [ ] 子类可以正确继承并调用父类的 _compute_dt(), _apply_bc()
- [ ] _compute_dt() 对各种输入返回合理的正值 (>0)
- [ ] _apply_bc() 正确复制边界值 (U[:,0]=U[:,1], U[:,-1]=U[:,-2])
- [ ] _enforce_positivity() 将负值修正为 1e-12

### 类型安全 (Should Have)
- [ ] 所有公开方法都有完整的类型注解
- [ ] Docstring 使用 Google style (Args/Returns/Raises/Example)
- [ ] 通过 mypy 类型检查 (忽略 import 错误)

### 测试辅助 (Must Have)
- [ ] 提供 factory 方法或示例用法
- [ ] 至少2个子类(LF和LW)可用于集成测试

## 参考资料
- SDD.md §3.1.2 格式基类设计
- Gamma et al. (1991) "A comparative study of some TVD schemes"
- GITHUB_COLLABORATION_GUIDE.md §6 Code Review标准
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    })

    # ====== B5-B10: 六种具体格式 (简化版描述以节省空间) ======
    @{
        title = "feat(core): 实现Lax-Friedrichs格式 (#B5)"
        body = @"
## 功能概述
实现 **Lax-Friedrichs (LxF)** 一阶有限体积格式。

## 数值格式
LxF 是最简单的FVM格式，具有强数值粘性（耗散大），但无条件TVD稳定。

### 核心公式
$$
\mathbf{F}^*_{i+\frac{1}{2}} = \frac{\mathbf{F}_i + \mathbf{F}_{i+1}}{2} - \alpha(\mathbf{U}_{i+1} - \mathbf{U}_i)$$

其中数值粘性系数 $\alpha = \Delta x / \Delta t$

### 特点
- ✅ **一阶空间精度** (误差 O(Δx))
- ✅ **无条件TVD稳定** (对任意CFL < 1.0不产生振荡)
- ❌ **高数值耗散** (光滑区被过度抹平)
- 📊 **适合用途**: 教学入门、基准对比、稳定性测试

## 实现要求
1. 继承 BaseScheme(name="Lax-Friedrichs", order=1, tvd=True)
2. 实现 evolve() 方法:
   - 调用 _compute_dt() 获取时间步长
   - 计算 α = dx/dt (数值粘性系数)
   - 时间推进循环:
     ```
     for n_step in range(num_steps):
         F_phys = compute_flux(U)           # 物理通量
         F_num = 0.5*(F[:,1:] + F[:,:-1])  # 平均通量
         F_lxf = F_num - alpha * (U[:,1:] - U[:,:-1])  # LxF通量
         U[:] = U - (dt/dx) * (F_lxf[:,1:] - F_lxf[:,:-1])
         U = _apply_bc(U)
         U = _enforce_positivity(U)
         record_snapshot(t, U)
     ```
3. 返回 {时刻: 解状态} 字典

## 验收标准
- [ ] 可以实例化: `scheme = LaxFriedrichsScheme()`
- [ ] evolve() 返回正确类型的字典
- [ ] **均匀初值测试**: 常数解不随时间变化 (机器精度内)
- [ ] **干底Ritter解**: L∞误差 < 10% (nx=200, CFL=0.9)
- [ ] **质量守恒**: Δm/m₀ < 1e-6
- [ ] **正性保持**: 不出现负水深 (h ≥ 0)
- [ ] **CFL稳定性**: CFL=0.9 时不崩溃
- [ ] **性能**: nx=500, t_end=0.5 时 < 5秒

## 参考
- Toro (2009) Chapter 6
- LeVeque (2002) Chapter 12
- SDD.md §3.1.2
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现Lax-Wendroff格式 (#B6)"
        body = @"
## 功能概述
实现 **Lax-Wendroff (LW)** 二阶中心有限体积格式。

## 特点
- ✅ **二阶空间精度** (光滑区收敛快)
- ❌ **非TVD稳定** (间断处产生非物理振荡)
- 📊 **适合用途**: 光滑解精度测试、与LF对比展示耗散影响

## 核心公式 (两步Taylor展开)
**Predictor (预测步)**:
$$\mathbf{U}_i^{n+\frac{1}{2}} = \mathbf{U}_i^n - \frac{\Delta t}{2\Delta x}(\mathbf{F}_{i+\frac{1}{2}} - \mathbf{F}_{i-\frac{1}{2}})^n$$

**Corrector (校正步)**:
$$\mathbf{U}_i^{n+1} = \mathbf{U}_i^{n+\frac{1}{2}} - \frac{\Delta t}{2\Delta x}(\tilde{\mathbf{F}}_{i+\frac{1}{2}} - \tilde{\mathbf{F}}_{i-\frac{1}{2}})^{n+\frac{1}{2}}$$

## 实现要点
1. 继承 BaseScheme(name="Lax-Wendroff", order=2, tvd=False)
2. 两步法: Predictor → Corrector
3. 需要额外存储 U_predict 中间变量
4. MacCormack格式与此类似但方向相反 (先算F再算U)

## 验收标准
- [ ] 二阶精度: 光滑区收敛阶 ≈ 2.0 (网格加密测试)
- [ ] 激波振荡: 间断处有明显非物理振荡 (已知缺陷)
- [ ] 比 LF 更精确但不如 LF 稳定
- [ ] 性能: 与 LF 相近 (同为显式格式)

## 参考
- LeVeque (2002) Chapter 17
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现MacCormack格式 (#B7)"
        body = @"
## 功能概述
实现 **MacCormack (MC)** 二阶预测-校正有限体积格式。

## 特点
- ✅ **二阶精度** (时空均为二阶)
- ❌ **非TVD稳定**
- 🔧 **与LW区别**: LW是"先算U再算F"，MC是"先算F再算U"

## 核心公式
**Step 1 - Predictor (预测通量)**:
$$\tilde{\mathbf{F}}_i = \mathbf{F}(\mathbf{U}_i^n)$$

**Step 2 - Predicted U**:
$$\tilde{\mathbf{U}}_i = \mathbf{U}_i^n - \frac{\Delta t}{\Delta x}(\tilde{\mathbf{F}}_{i+\frac{1}{2}} - \tilde{\mathbf{F}}_{i-\frac{1}{2}})$$

**Step 3 - Corrector (校正通量)**:
$$\hat{\mathbf{F}}_i = \mathbf{F}(\tilde{\mathbf{U}}_i)$$

**Step 4 - Corrected U**:
$$\mathbf{U}_i^{n+1} = \tilde{\mathbf{U}}_i - \frac{\Delta t}{2\Delta x}(\hat{\mathbf{F}}_{i+\frac{1}{2}} - \hat{\mathbf{F}}_{i-\frac{1}{2}})$$

## 验证标准
- [ ] 二阶时空精度
- [ ] 与LW精度相当但实现不同
- [ ] 适用于光滑问题

## 参考
- MacCormack (1969) The Effect of Viscosity in Hypersonic Impact Calculations
"@
        labels = "feat,priority/medium,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现Godunov精确格式 (#B8)"
        body = @"
## 功能概述
实现 **Godunov** 精确Riemann求解器格式 (一阶+空间精度)。

## 特点
- ✅ 使用**精确Riemann求解器** (B2实现) 计算界面通量
- ✅ **TVD稳定** (不产生非物理振荡)
- ✅ **激波捕捉质量优秀** (间断锐利)
- 📊 **适用场景**: 激波捕捉基准、工程实用首选之一

## 核心思想
在每个界面 $i+\frac{1}{2}$ 处:
1. 构建 Riemann 问题: $(U_L, U_R) = (U_i, U_{i+1})$
2. 调用 exact_riemann_solution() 求解
3. 使用精确解的星区通量: $\mathbf{F}^* = \mathbf{F}(U^*)$

## 实现要点
1. 继承 BaseScheme(name="Godunov", order=1, tvd=True)
2. 在 evolve() 循环中:
   ```
   for each interface i+1/2:
       U_L = U[:, i]
       U_R = U[:, i+1]
       riemann = exact_riemann_solution(U_L, U_R, g)
       F_star = physical_flux(riemann['h_star'], riemann['u_star'])
       U_update = - (dt/dx) * (F_star - F_{i-1/2})
   ```

## 验收标准
- [ ] 精确Riemann求解器已就绪 (依赖 B2)
- [ ] 激波位置准确 (无明显偏移)
- [ ] 无非物理振荡
- [ ] 比 HLL 更精确 (但更慢)

## 参考
- Godunov (1959) A Difference Scheme for Numerical Computation of Discontinuous Solutions of Hydrodynamic Equations
- Toro (2009) Chapter 6
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现HLL格式 (#B9)"
        body = @"
## 功能概述
实现 **HLL** 近似Riemann求解器格式 (一阶+空间精度)。

## 特点
- ✅ 使用 **HLL近似通量** (B3实现)
- ✅ **TVD稳定**
- ✅ **速度快** (比Godunov快10倍以上)
- 📊 **工程实用首选**

## 核心公式
直接调用 hll_flux(U_L, U_R, g) 获取界面通量 (无需迭代求解)。

## 验证标准
- [ ] HLL通量函数已就绪 (依赖 B3)
- [ ] 与 Godunov定性一致但更快
- [ ] 适合大规模网格计算

## 参考
- Harten, Lax, van Leer (1983)
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现MUSCL-Hancock TVD格式 (#B10)"
        body = @"
## 功能概述
实现 **MUSCL-Hancock** 二阶TVD有限体积格式 (本项目的**最高精度格式**)。

## 特点
- ✅ **二阶TVD** (光滑区二阶 + 间断处无振荡)
- ✅ **MUSCL重构** + **minmod限制器**
- ✅ **两步Hancock时间推进** (保持二阶时间精度)
- 🏆 **本项目旗舰格式**: 最复杂但效果最好

## 核心技术 (3个关键步骤)

### Step 1: MUSCL重构 (空间二阶)
对原始变量进行线性重构:
$$
\tilde{\mathbf{U}}_{i+\frac{1}{2}} = \mathbf{U}_i + \frac{\phi_i}{2}(\mathbf{U}_{i+1} - \mathbf{U}_{i-1})$$

其中斜率 $\phi$ 由 **minmod限制器** 限制:
$$\text{minmod}(a,b) = \begin{cases}
a & \text{if } ab > 0 \text{ and } |a| \leq |b| \\
b & \text{if } ab \leq 0 \text{ and } |b| \leq |a| \\
0 & \text{otherwise}
\end{cases}$$

### Step 2: Hancock预测步
$$\bar{\mathbf{U}}_i^{n+\frac{1}{2}} = \mathbf{U}_i^n - \frac{\Delta t}{\Delta x}(\tilde{\mathbf{F}}_{i+\frac{1}{2}} - \tilde{\mathbf{F}}_{i-\frac{1}{2}})$$

### Step 3: Hancock校正步
$$\mathbf{U}_i^{n+1} = \bar{\mathbf{U}}_i^{n+\frac{1}{2}} - \frac{\Delta t}{\Delta x}(\hat{\mathbf{F}}_{i+\frac{1}{2}} - \hat{\mathbf{F}}_{i-\frac{1}{2}})$$

## 实现要点
1. 继承 BaseScheme(name="MUSCL-Hancock", order=2, tvd=True)
2. 实现 _muscl_reconstruct() 方法 (含minmod limiter)
3. 实现 _hancock_predict() 和 _hancock_correct() 方法
4. 组合到 evolve() 主循环

## 验收标准
- [ ] **TVD性质**: 间断处无振荡 (与LF/Godunov对比)
- [ ] **二阶精度**: 光滑区收敛阶 ≈ 2.0
- [ ] **minmod限制器**: 正确工作 (不抑制过多)
- [ ] **性能**: 比 LF 更精确，比 Godunov 更快
- [ ] **综合最优**: 本项目中精度+稳定性最好的格式

## 参考
- van Leer (1977) Towards the Ultimate Conservative Difference Scheme V
- MUSCL: Barth (1989), Colella (1985)
- Hancock (1995)
- Toro (2009) Chapter 14
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },

    # ========== 批次C: 前端UI (@FE) ==========
    @{
        title = "feat(ui): 创建app.py主入口和侧栏导航 (#C1)"
        body = @"
## 功能概述
创建 Streamlit 应用的**主入口文件** `src/frontend/app.py`，包含：
- 全局页面配置 (st.set_page_config)
- 侧栏导航栏 (4个页面切换)
- 页面路由逻辑

## 技术要求

### 文件位置
`src/frontend/app.py`

### UI布局设计
```
┌─────────────────────────────────────────────────┐
│  🌊 CFD-Class v0.1.0-alpha                  │
│  一维溃坝CFD教学软件                           │
├─────────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────────────┐   │
│  │  🏠 首页                               │   │
│  │  📊 模拟                               │   │
│  │  🎬 动画                               │   │
│  │  📝 报告                               │   │
│  └─────────────────────────────────────────────┘   │
│                                             │
│  [主内容区根据导航显示对应页面]                │
└─────────────────────────────────────────────────┘
```

### 代码框架
```python
import streamlit as st

def main() -> None:
    """应用主入口."""
    st.set_page_config(
        page_title="CFD-Class 一维溃坝教学",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    with st.sidebar:
        # Logo/标题区
        st.image("assets/logo.png", width=100)
        st.title("CFD-Class")
        st.caption("一维溃坝CFD教学软件 v0.1.0-alpha")
        st.divider()
        
        # 导航菜单
        page = st.radio(
            "导航",
            ["🏠 首页", "📊 模拟", "🎬 动画", "📝 报告"],
            label_visibility="collapsed",
            key="nav_menu"
        )
    
    # 页面路由
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

## 验收标准
- [ ] `streamlit run src/frontend/app.py` 可正常启动
- [ ] 浏览器访问 localhost:8501 显示正确页面
- [ ] 侧栏导航可在4个页面间切换
- [ ] 默认选中"首页"
- [ ] 页面布局响应式 (宽屏友好)
- [ ] 标题和图标正确显示

## 参考
- Streamlit官方文档: https://docs.streamlit.io/
- SDD.md §3.2.1 主入口设计
- user_manual.md §5 功能详解
"@
        labels = "feat,priority/high,module/ui,status/in-progress"
        assignees = @("FE")
    },
    @{
        title = "feat(ui): 实现param_panel参数输入面板组件 (#C2)"
        body = @"
## 功能概述
创建可复用的**参数输入面板组件** `src/frontend/components/param_panel.py`。

该组件封装了所有物理参数和数值参数的输入控件，供模拟页面使用。

## 组件功能

### 显示内容
1. **物理参数区** (Physical Parameters)
   - h_L: 左侧水深 [滑块 + 数字输入]
   - h_R: 右侧水深 [滑块 + 数字输入]
   - u_L: 左侧流速 [滑块 + 数字输入]
   - u_R: 右侧流速 [滑块 + 数字输入]
   - g: 重力加速度 [滑块 + 数字输入]

2. **数值参数区** (Numerical Parameters)
   - CFL: CFL数 [滑块 0.1-0.95]
   - nx: 网格数 [滑块 50-2000 或数字输入]
   - t_end: 终止时间 [滑块 0.1-10]

3. **帮助系统**
   - 每个参数旁显示 ℹ️ 图标
   - 点击展开: 物理含义、推荐值、注意事项、参考文献

4. **预设案例下拉框** (可选)
   - 干底Ritter解 (h_L=1, h_R=0)
   - 湿底一般解 (h_L=1, h_R=0.5)
   - 高Froude数 (h_L=1, h_R=0.1, u_L=2)
   - 对称扩展 (h_L=h_R=1, u_L=-1, u_R=1)

### API接口
```python
def render() -> DamBreakConfig:
    """渲染参数面板并返回配置对象.
    
    Returns:
        DamBreakConfig: 用户配置的参数对象 (可直接传给SimulationEngine)
    
    Raises:
        ValueError: 参数超出范围时显示错误提示
    """
```

### 交互特性
- [ ] 滑块实时联动数字输入框
- [ ] 参数超出范围时阻止并显示红色错误提示
- [ ] 帮助信息使用 st.expander 组件
- [ ] 预设案例一键加载所有参数
- [ ] 响应式布局 (移动端友好)

## 验收标准
- [ ] 组件可独立渲染 (不依赖其他页面)
- [ ] 返回标准的 DamBreakConfig 对象
- [ ] 所有8个参数都可正常输入
- [ ] 参数校验逻辑正确
- [ ] UI美观专业 (符合Streamlit最佳实践)

## 参考
- Streamlit widgets文档: https://docs.streamlit.io/library/api-reference/widgets
- SDD.md §3.2.2 组件设计
"@
        labels = "feat,priority/high,module/ui"
        assignees = @("FE")
    },
    @{
        title = "feat(ui): 实现scheme_selector格式选择组件 (#C3)"
        body = @"
## 功能概述
创建**格式多选组件** `src/frontend/components/scheme_selector.py`。

允许用户选择1-6种FVM格式进行对比运行。

## 组件功能
- [ ] 6个Checkbox: LF / LW / MC / Godunov / HLL / MUSCL
- [ ] 默认全选
- [ ] 显示格式简要说明 (名称 + 阶数 + TVD标记)
- [ ] 返回选中的格式名称列表

## API
```python
def render(selected_schemes: list[str] = None) -> list[str]:
    """渲染格式选择器.
    
    Args:
        selected_schemes: 默认选中的格式列表 (如 None 则全选)
    
    Returns:
        list[str]: 用户选中的格式名称列表
    """
```

## 验证标准
- [ ] 6种格式均可选
- [ ] 默认状态为全选
- [ ] 返回 list[str] 类型
"@
        labels = "feat,priority/high,module/ui"
        assignees = @("FE")
    },
    @{
        title = "feat(ui): 实现result_viewer结果查看器组件 (#C4)"
        body = @"
## 功能概述
创建**结果查看器组件** `src/frontend/components/result_viewer.py`。

负责显示模拟结果的图表和数据表格。

## 功能
- [ ] 水深剖面对比图 (h(x) 多曲线叠加)
- [ ] 速度剖面对比图 (u(x)) 多曲线叠加
- [ ] 精确解参考线 (红色虚线)
- [ ] 误差统计表格 (L1/L2/L∞)
- [ ] 图例和颜色映射
- [ ] 结果导出按钮 (PNG/SVG/CSV)

## 验收标准
- [ ] 可接收 SimulationResult 数据并渲染
- [ ] 图表清晰美观
"@
        labels = "feat,priority/medium,module/ui"
        assignees = @("FE")
    },

    # ========== 批次D: 测试 (@QA) ==========
    @{
        title = "test: 搭建pytest测试框架和conftest.py (#D1)"
        body =@"
## 功能概述
搭建完整的 pytest 测试框架，包括 conftest.py 配置、目录结构和基础工具函数。

## 具体工作

### 1. 创建 tests/conftest.py
```python
import sys
import os
import pytest
import numpy as np
from pathlib import Path

# 确保项目根目录在sys.path中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置测试 fixture
@pytest.fixture(scope="session")
def sample_config():
    """提供标准测试配置."""
    from src.core.config import DamBreakConfig
    return DamBreakConfig(
        h_L=1.0, h_R=0.0, u_L=0.0, u_R=0.0,
        g=9.81, cfl=0.9, nx=200, t_end=0.5
    )

@pytest.fixture
def dry_bed_config():
    """干底Ritter解配置."""
    return DamBreakConfig(h_L=1.0, h_R=0.0)

@pytest.fixture
def wet_bed_config():
    """湿底一般解配置."""
    return DamBreakConfig(h_L=1.0, h_R=0.5)
```

### 2. 创建 tests/__init__.py (已存在，更新)
### 3. 创建 tests/unit/__init__.py (空文件)
### 4. 创建 tests/integration/__init__.py (空文件)
### 5. 创建 tests/performance/__init__.py (空文件)

## 验收标准
- [ ] `pytest tests/ --collect-only` 能收集到所有测试文件
- [ ] `pytest tests/unit/test_config.py::test_default_values` 能运行
- [ ] conftest.py fixtures 可被其他测试文件引用
"@
        labels = "test,priority/high,module/tests,status/in-progress"
        assignees = @("QA")
    },
    @{
        title = "test: 编写DamBreakConfig单元测试 (10 cases) (#D2)"
        body = @"
## 功能概述
为 DamBreakConfig 编写全面的单元测试 (≥10个测试用例)。

## 测试用例清单
1. test_default_values - 默认参数正确性
2. test_custom_values - 自定义参数
3. test_frozen - 不可变性 (frozen)
4. test_validation_h_L_negative - h_L≤0 校验
5. test_validation_h_R_negative - h_R<0 校验
6. test_validation_cfl_range - CFL范围校验
7. test_validation_nx_minimum - nx最小值校验
8. test_dx_property - dx计算正确性
9. test_x_grid_property - x_grid生成正确性
10. test_edge_cases - 边界参数组合

## 验收标准
- [ ] 覆盖率 ≥ 90%
- [ ] 所有P0功能都有测试
"@
        labels = "test,priority/high,module/tests"
        assignees = @("QA")
    },
    @{
        title = "test: 编写6种格式单元测试 (#D3)"
        body = @"
## 功能概述
为每种格式(LF/LW/MC/Godunov/HLL/MUSCL)编写核心单元测试。

## 每种格式至少测试:
1. 类实例化和属性
2. 均匀解保持
3. 干底Ritter解 (L∞误差)
4. 质量守恒
5. 正性保持
6. CFL稳定性

## 验收标准
- [ ] 每种格式≥5个测试用例
- [ ] 总覆盖率 ≥ 80%
"@
        labels = "test,priority/high,module/tests"
        assignees = @("QA")
    },

    # ========== 批次E: 文档 (@TW) ==========
    @{
        title = "docs: 完善SRS第3章具体需求-补充验收标准 (#E1)"
        body = @"
## 功能概述
完善 SRS.md 第3章的具体需求部分，为每个FR添加详细的验收标准和测试方法。

## 工作内容
- 为 FR-01~FR-05 (首页模块) 添加验收标准
- 为 FR-11~FR-13 (模拟模块) 添加验收标准
- 补充 NFR-01~NFR-05 (非功能需求) 的量化指标
- 添加测试方法章节

## 验收标准
- [ ] 每个P0需求都有明确的、可测量的验收标准
- [ ] 验收标准包含具体的数值指标 (如"误差<5%","响应时间<3s")
"@
        labels = "docs,priority/medium,module/docs"
        assignees = @("TW")
    },
    @{
        title = "docs: 编写examples/dry_bed_ritter案例文档 (#E2)"
        body = @"
## 功能概述
编写干底Ritter解经典案例的完整文档，包括:
- 案例背景 (物理意义、历史案例)
- 参数配置 (YAML文件)
- 预期结果 (精确解公式、特征图)
- 使用教程 (如何在本软件中运行此案例)
- 结果解读指南

## 文件位置
`examples/dry_bed_ritter/README.md`
"@
        labels = "docs,priority/medium,module/docs"
        assignees = @("TW")
    },
    @{
        title = "docs: 编写examples/wet_bed_general案例文档 (#E3)"
        body = @"
## 功能概述
编写湿底一般解案例文档 (含激波的情况)。

## 文件位置
`examples/wet_bed_general/README.md`
"@
        labels = "docs,priority/low,module/docs"
        assignees = @("TW")
    }
)

# ====== 开始创建Issues ======

Write-Host "`n[$($allIssues.Count)] 个Issues准备创建..." -ForegroundColor Yellow
Write-Host ""

$successCount = 0
$failCount = 0

foreach ($issue in $allIssues) {
    $idx = $allIssues.IndexOf($issue) + 1
    Write-Host "━━━ [$idx/$($allIssues.Count)] $($issue.title)" -ForegroundColor Cyan
    
    try {
        # 构建body (处理多行字符串)
        $cleanBody = $issue.body -replace "`r`n", "\n" -replace "`n", ""
        
        $result = gh issue create `
            --repo $repo `
            --title $issue.title `
            --body $cleanBody `
            --labels $issue.labels `
            --assignees ($issue.assignees -join ",") `
            2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0) {
            $issueUrl = ($result | ConvertFrom-Json).html_url
            Write-Host "  ✅ 成功! → $issueUrl" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "  ❌ 失败 (可能已存在或权限问题)" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "  ❌ 异常: $_" -ForegroundColor Red
        $failCount++
    }
    
    Start-Sleep -Milliseconds 800  # 避免触发GitHub速率限制
}

# ====== 完成 ======
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ 全部任务Issues发布完成!                       ║" -ForegroundColor Green
Write-Host "╠═════════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                             ║" -ForegroundColor Green
Write-Host "║  成功: $successCount 个 | 失败: $failCount | 总计: $($allIssues.Count)    ║" -ForegroundColor Green
Write-Host "║                                                             ║" -ForegroundColor Green
Write-Host "╚═════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📌 下一步:" -ForegroundColor Yellow
Write-Host "   1. 打开 https://github.com/kaklos-cyber/cfd_class/issues 查看所有任务" -ForegroundColor White
Write-Host "   2. 打开 Projects 看板将Issues拖入各列" -ForegroundColor White
Write-Host "   3. 通知团队成员开始认领任务!" -ForegroundColor White
Write-Host ""
