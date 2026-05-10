# CFD-Class Sprint 1 批量Issue创建脚本
# 使用方法: powershell -ExecutionPolicy Bypass -File .\create_sprint1_issues.ps1

$repo = "kaklos-cyber/cfd_class"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CFD-Class Sprint 1 Issue 批量创建工具" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$issues = @(
    # ====== 批次A: 基础设施 (@PM) ======
    @{
        title = "chore: 配置main/develop分支保护规则 (#A1)"
        body = @"
## 任务描述
配置GitHub仓库的分支保护规则，确保代码质量和团队协作规范。

## 具体步骤

### main分支保护:
- [ ] Require a pull request before merging: ✅ 开启
- [ ] Require approvals: **2人审核通过**
- [ ] Dismiss stale PR approvals when new commits: ✅ 开启
- [ ] Require status checks to pass before merging: ✅ 开启
  - ci/test (必须通过)
  - ci/lint (必须通过)
- [ ] Do not allow bypassing: ✅ 开启
- [ ] Include administrators: ✅ 开启（管理员也需遵守）
- [ ] Allow force pushes: ❌ 关闭
- [ ] Allow deletions: ❌ 关闭

### develop分支保护:
- [ ] Require a pull request before merging: ✅ 开启
- [ ] Require approvals: **1人审核通过**
- [ ] Require status checks: ci/test
- [ ] Allow force pushes: ❌ 关闭
- [ ] Allow deletions: ❌ 关闭

## 参考文档
GITHUB_COLLABORATION_GUIDE.md §1.3 分支保护规则配置
"@
        labels = "chore,priority/critical,module/infrastructure"
        assignees = @("PM")
    },
    @{
        title = "chore: 创建完整的Labels标签体系(12个) (#A2)"
        body = @"
## 任务描述
在仓库Settings → Labels中创建以下标签体系。

### 类型标签 (kind/*)
| 标签 | 颜色 | 描述 |
|------|------|------|
| kind/bug | 🔴 红色 #e11d21 | 缺陷 |
| kind/enhancement | 🟣 紫色 #a855f7 | 新功能 |
| kind/docs | 🔵 蓝色 #0075ff | 文档 |
| kind/refactor | 🟡 黄色 #fbca04 | 重构 |
| kind/testing | 🟢 绿色 #2ea44f | 测试 |

### 优先级标签 (priority/*)
| 标签 | 颜色 |
|------|------|
| priority/critical | ❤️ 红色 |
| priority/high | ⚠️ 橙色 |
| priority/medium | ➖ 蓝色 |
| priority/low | ⬇️ 灰色 |

### 模块标签 (module/*)
- module/core (核心引擎)
- module/ui (用户界面)
- module/tests (测试)
- module/docs (文档)
- module/infrastructure (基础设施)

### 状态标签 (status/*)
- status/in-progress 🔄
- status/review 👀
- status/blocked 🚫

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

### 成员列表与权限

| 角色 | GitHub账号 | 权限级别 |
|------|-----------|---------|
| 架构师 @Arch | <待填写> | Admin |
| 后端开发 @BE | <待填写> | Write |
| 前端开发 @FE | <待填写> | Write |
| 测试工程师 @QA | <待填写> | Write |
| 文档工程师 @TW | <待填写> | Write |

### 操作步骤
1. 访问 Settings → Collaborators → Add people
2. 输入成员的GitHub用户名
3. 选择对应的权限级别
4. 发送邀请
5. 确认所有成员接受邀请

### 注意事项
- PM(@你) 已经是Admin，无需重复添加
- 建议先确认所有成员已注册GitHub账号
"@
        labels = "chore,priority/critical,module/infrastructure"
        assignees = @("PM")
    },

    # ====== 批次B: 核心引擎 (@BE) ======
    @{
        title = "feat(core): 实现 DamBreakConfig frozen dataclass (#B1)"
        body = @"
## 功能概述
实现 DamBreakConfig 数据类，统一管理一维溃坝问题的所有运行参数。

## 技术要求
1. 使用 `@dataclass(frozen=True)` 实现不可变配置
2. 包含8个参数: h_L, h_R, u_L, u_R, g, CFL, nx, t_end + x_min, x_max
3. 在 `__post_init__` 中添加参数合法性校验
4. 实现属性: `dx` (网格步长), `x_grid` (网格坐标数组)
5. 完整的类型注解和Google-style docstring

## 接口定义
```python
@dataclass(frozen=True)
class DamBreakConfig:
    h_L: float = 1.0       # 左侧水深 [m]
    h_R: float = 0.0       # 右侧水深 [m] (0=干底)
    u_L: float = 0.0       # 左侧流速 [m/s]
    u_R: float = 0.0       # 右侧流速 [m/s]
    g: float = 9.81        # 重力加速度 [m/s²]
    cfl: float = 0.9       # CFL稳定性数
    nx: int = 200          # 网格单元数
    t_end: float = 0.5     # 终止时间 [s]
    x_min: float = -5.0    # 左边界 [m]
    x_max: float = 5.0     # 右边界 [m]

    def __post_init__(self) -> None: ...
    
    @property
    def dx(self) -> float: ...
    
    @property
    def x_grid(self) -> NDArray[np.float64]: ...
```

## 验收标准
- [ ] 可使用默认值实例化
- [ ] 无效参数抛出 ValueError (含清晰错误信息)
- [ ] Frozen: 尝试修改属性时抛出 FrozenInstanceError
- [ ] dx 属性计算正确: (x_max-x_min)/nx
- [ ] x_grid 返回长度为 nx 的等间距数组
- [ ] 类型检查通过 (mypy)

## 参考文档
SDD.md §3.1.1 配置模块设计
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现精确Riemann求解器 (湿底+干底) (#B2)"
        body = @"
## 功能概述
实现一维浅水方程的精确Riemann求解器，支持湿底和干底两种情况。

## 数学背景
求解以下Riemann问题:

初始条件 (t=0):
```
U_L = [h_L, hu_L]^T   if x < 0
U_R = [h_R, hu_R]^T   if x > 0
```

控制方程 (Saint-Venant):
```
∂U/∂t + ∂F/∂x = 0
其中 U = [h, hu]^T, F = [hu, hu² + gh²/2]^T
```

## 实现要求

### 湿底情况 (h_L>0 且 h_R>0)
1. 计算星区水深 h*: 使用Newton-Raphson迭代求解非线性方程
2. 计算星区流速 u*
3. 判断波系类型:
   - 左稀疏波 / 左激波
   - 右稀疏波 / 右激波
4. 计算波速 S_L, S_R, S_*

### 干底情况 (h_R ≈ 0)
1. 使用 Ritter (1892) 解析解
2. 稀疏波扇区: h(x/t) = (1/g)*(u_L - x/(2t))²
3. 波速: S_L = u_L - √(gh_L), S_* = u_L/3 + 2√(gh_L)/3

### API接口
```python
def exact_riemann_solution(
    U_L: NDArray[np.float64],  # shape=(2,) [h_L, hu_L]
    U_R: NDArray[np.float64],  # shape=(2,) [h_R, hu_R]
    g: float                    # 重力加速度
) -> dict:
    """返回:
    {
        'S_L': float,      # 左波波速
        'S_R': float,      # 右波波速
        'S_star': float,   # 星区接触间断速度
        'h_star': float,   # 星区水深
        'u_star': float,   # 星区流速
        'type': str,       # 波系类型 ('dry_ritter', 'wet_general', etc.)
        'star_region_left': dict,  # 左星区状态
        'star_region_right': dict, # 右星区状态
    }
    """
```

## 验收标准
- [ ] 湿底案例: 与Toro书中的数值结果一致 (误差<1e-6)
- [ ] 干底Ritter解: 与解析解一致 (误差<1e-10)
- [ ] 极限情况: h_L=h_R 时返回均匀流解
- [ ] Newton迭代收敛: 通常<10次迭代
- [ ] 单元测试覆盖率 ≥90%

## 参考资料
- Toro, E.F. (2009) Chapter 4
- George (2008) Chapter 3
- SDD.md §3.1.4 Riemann求解器设计
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现 HLL 近似 Riemann 通量 (#B3)"
        body = @"
## 功能概述
实现HLL (Harten-Lax-van Leer) 两波近似Riemann通量计算。

## HLL公式
```
F_HLL = (S_R * F_L - S_L * F_R + S_L * S_R * (U_R - U_L)) / (S_R - S_L)

其中:
- F_L, F_R: 左右界面的物理通量
- U_L, U_R: 左右守恒变量
- S_L, S_R: 左右波速估计值
```

## 波速估计 (Davis估计)
```
S_L = min(u_L - c_L, u_R - c_R)
S_R = max(u_L + c_L, u_R + c_R)

其中 c = √(gh) 为局部波速
```

## API接口
```python
def hll_flux(
    U_L: NDArray[np.float64],  # shape=(2,)
    U_R: NDArray[np.float64],  # shape=(2,)
    g: float
) -> NDArray[np.float64]:     # shape=(2,) HLL通量向量
```

## 验收标准
- [ ] 正确计算光滑区的数值通量
- [ ] 正确捕捉间断（激波/接触面）
- [ ] 与精确Riemann通量定性一致
- [ ] 计算速度快于精确求解器 (>10x加速)

## 参考
SDD.md §3.1.4 HLL近似求解器
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现 BaseScheme 抽象基类 (#B4)"
        body = @"
## 功能概述
定义所有有限体积格式的抽象基类 BaseScheme，统一接口和公共逻辑。

## 类设计
```python
from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable
import numpy as np
from numpy.typing import NDArray

class BaseScheme(ABC):
    """有限体积格式抽象基类.
    
    所有6种格式(LF/LW/MC/Godunov/HLL/MUSCL)都必须继承此类。
    """

    def __init__(
        self,
        name: str,
        order: int,
        tvd: bool = False
    ) -> None:
        self.name = name          # 格式名称
        self.order = order        # 精度阶数 (1 or 2)
        self.tvd = tvd            # 是否具有TVD性质

    @abstractmethod
    def evolve(
        self,
        U0: NDArray[np.float64],
        config: 'DamBreakConfig',
        progress_callback: Optional[Callable[[float, float], None]] = None
    ) -> Dict[float, NDArray[np.float64]]:
        """执行时间演化计算.
        
        Args:
            U0: 初始守恒变量矩阵, shape=(2, nx)
            config: 运行参数配置
            progress_callback: 进度回调 callback(current_time, end_time)
            
        Returns:
            Dict[float, NDArray]: {时刻t: 解状态U}
        """
        pass

    def _compute_dt(
        self,
        U: NDArray[np.float64],
        config: 'DamBreakConfig'
    ) -> float:
        """基于CFL条件计算稳定时间步长."""
        h = U[0, :]
        u = np.where(h > 1e-12, U[1, :] / h, 0.0)
        c = np.sqrt(config.g * np.maximum(h, 1e-12))
        max_speed = np.max(np.abs(u) + c)
        return config.cfl * config.dx / max_speed

    def _apply_bc(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """应用透射边界条件 (零梯度外推)."""
        U[:, 0] = U[:, 1]
        U[:, -1] = U[:, -2]
        return U

    def _enforce_positivity(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        """正性保持: 防止负水深."""
        U[0, :] = np.maximum(U[0, :], 1e-12)
        return U
```

## 公共方法说明
- `_compute_dt()`: 所有格式共用的CFL自适应时间步长计算
- `_apply_bc()`: 透射边界条件处理
- `_enforce_positivity()`: 正性保持机制

## 验收标准
- [ ] 无法直接实例化 BaseScheme (抽象类)
- [ ] 子类可以正确继承并调用父类方法
- [ ] _compute_dt() 在各种输入下返回合理的正值
- [ ] _apply_bc() 正确复制边界值
- [ ] _enforce_positivity() 将负值修正为小正数

## 参考
SDD.md §3.1.2 格式基类设计
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    },
    @{
        title = "feat(core): 实现 Lax-Friedrichs 格式 (#B5)"
        body = @"
## 功能概述
实现 Lax-Friedrichs (LxF) 一阶有限体积格式。

## 数值格式
LxF 通量:
```
F*_{i+1/2} = (F_i + F_{i+1})/2 - (dx/dt)(U_{i+1} - U_i)/2
```

时间推进:
```
U_i^{n+1} = U_i^n - (dt/dx)(F*_{i+1/2} - F*_{i-1/2})
```

特点:
- 一阶空间精度
- 强数值粘性（耗散大）
- 无条件TVD稳定（对任意CFL<1）
- 适合作为基准对比格式

## 实现要点
1. 继承 BaseScheme
2. 在 evolve() 中实现主循环:
   - 计算 dt (调用 _compute_dt)
   - 计算数值粘性系数 alpha = dx/dt
   - 循环每个时间步:
     - 计算物理通量 F(U)
     - 计算LxF数值通量 F*
     - 更新 U
     - 应用边界条件 (_apply_bc)
     - 正性保持 (_enforce_positivity)
     - 记录快照 (如果需要)
3. 返回 {时刻: 解状态} 字典

## 验收标准
- [ ] 可以成功实例化 LaxFriedrichsScheme(name="Lax-Friedrichs", order=1, tvd=True)
- [ ] evolve() 返回正确类型的字典
- [ ] 对均匀初值: 解不随时间变化 (机器精度内)
- [ ] 对干底Ritter解: L∞误差 < 10% (nx=200)
- [ ] 质量守恒误差 Δm/m₀ < 1e-6
- [ ] 不出现负水深
- [ ] CFL=0.9 时不崩溃

## 参考
- Toro (2009) Chapter 6
- LeVeque (2002) Chapter 12
"@
        labels = "feat,priority/high,module/core"
        assignees = @("BE")
    }
)

# ====== 开始创建Issues ======

$success_count = 0
$fail_count = 0

foreach ($issue in $issues) {
    Write-Host "`n[$($issues.IndexOf($issue)+1)/$($issues.Count)] 创建: $($issue.title)" -ForegroundColor Yellow
    
    try {
        $result = gh issue create `
            --title $issue.title `
            --body $issue.body `
            --labels $issue.labels `
            --assignees ($issue.assignees -join ",") `
            --repo $repo `
            2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ 成功!" -ForegroundColor Green
            $success_count++
        } else {
            Write-Host "  ❌ 失败: $result" -ForegroundColor Red
            $fail_count++
        }
    } catch {
        Write-Host "  ❌ 异常: $_" -ForegroundColor Red
        $fail_count++
    }
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  创建完成!" -ForegroundColor Cyan
Write-Host "  成功: $success_count | 失败: $fail_count | 总计: $($issues.Count)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
