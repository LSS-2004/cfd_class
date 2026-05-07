# CFD-Class 贡献者指南

> **版本**: v1.0 | **最后更新**: 2026-05-07
> **适用范围**: 所有参与CFD-Class开发的团队成员

感谢你对CFD-Class项目的关注！本文档将指导你如何规范地参与项目开发。

---

## 目录

1. [环境搭建](#1-环境搭建)
2. [分支策略](#2-分支策略)
3. [Commit Message 规范](#3-commit-message-规范)
4. [Pull Request 流程](#4-pull-request-流程)
5. [Code Review 标准](#5-code-review-标准)
6. [Issue 管理](#6-issue-管理)
7. [编码规范](#7-编码规范)
8. [本地开发命令速查](#8-本地开发命令速查)

---

## 1. 环境搭建

### 1.1 前置要求

| 工具 | 版本要求 | 用途 |
|------|---------|------|
| Python | >= 3.10, < 3.12 | 核心开发语言 |
| Git | >= 2.30 | 版本控制 |
| pip | >= 23.0 | 包管理器 |
| VS Code (推荐) | 最新版 | IDE（安装Python扩展）|

### 1.2 安装步骤

```bash
# Step 1: 克隆仓库
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class

# Step 2: 创建虚拟环境
python -m venv .venv

# Step 3: 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Step 4: 安装依赖
pip install -r requirements.txt

# Step 5: 安装开发工具
pip install -e ".[dev]"

# Step 6: 验证安装
python -c "from src.core import DamBreakConfig; print('✅ Environment OK')"
pytest tests/ --collect-only  # 收集测试用例但不运行
```

### 1.3 VS Code 推荐扩展

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "charliermarsh.ruby-extension",  // 替换为 Python 相关
    "streetsidesoftware.code-spell-checker",
    "ms-vscode.live-server"
  ]
}
```

在 VS Code 中按 `Ctrl+Shift+P` → 输入 `Extensions: Show Recommended Extensions` 即可安装。

---

## 2. 分支策略

本项目采用 **Git Flow** 分支管理策略：

```
main (生产环境) ← 仅 @PM 和 @Arch 可合并
  ↑
develop (开发集成分支) ← 功能分支合并到此
  ├─ feature/#XXX-description    新功能开发
  ├─ bugfix/#XXX-description     Bug修复
  ├─ docs/#XXX-description      文档更新
  └── hotfix/#XXX-description   紧急修复（从main分出）
```

### 2.1 分支命名规范

```bash
# 功能分支
feature/001-add-tvd-solver

# Bug修复分支
bugfix/002-fix-memory-leak-in-mesh

# 文档分支
docs/003-update-srs-chapter4

# 热修复分支
hotfix/004-fix-crash-on-startup
```

### 2.2 工作流程示例

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/005-add-k-epsilon-model

# 2. 开发代码...
# 编辑文件、编写测试...

# 3. 提交代码（遵循Commit Message规范）
git add src/core/schemes/k_epsilon.py tests/unit/test_k_epsilon.py
git commit -m "feat(scheme): add k-epsilon turbulence model"

# 4. 推送到远程
git push origin feature/005-add-k-epsilon-model

# 5. 在GitHub创建Pull Request（目标：develop）
# 等待Code Review...
```

---

## 3. Commit Message 规范

### 3.1 格式

```
<type>(<scope>): <subject>

<body> (可选)

<footer> (可选)
```

### 3.2 Type 类型

| Type | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(solver): add TVD scheme` |
| `fix` | Bug修复 | `fix(ui): resolve layout overflow` |
| `docs` | 文档变更 | `docs(srs): update performance requirements` |
| `style` | 代码格式调整（不影响逻辑）| `style(code): apply black formatting` |
| `refactor` | 重构（非新功能非Bug）| `refactor(core): extract utilities` |
| `test` | 测试相关 | `test(mesh): add regression test` |
| `chore` | 构建/工具链/辅助工具 | `chore(ci): upgrade pytest to 8.0` |
| `perf` | 性能优化 | `perf(grid): optimize cell indexing` |

### 3.3 Scope 范围

常用的 Scope：

| Scope | 对应模块 |
|-------|---------|
| `scheme` | src/core/schemes/ |
| `solver` | src/core/solvers/ |
| `config` | src/core/config.py |
| `ui` / `page` | src/frontend/pages/ |
| `component` | src/frontend/components/ |
| `engine` | src/frontend/engines/ |
| `test` | tests/ |
| `docs` | docs/ |
| `ci` | .github/workflows/ |

### 3.4 示例

```bash
# ✅ 好的 Commit Message
feat(solver): add TVD scheme for shock capturing

- Implement second-order TVD limiter
- Support minmod, van Leer, superbee limiters
- Add unit tests with 95% coverage
- Reference: Harten 1983, JCP

Closes #123

# ❌ 不好的 Commit Message
fix bug
update code
add stuff
```

---

## 4. Pull Request 流程

### 4.1 PR Checklist（提交前必读）

创建 PR 前，请确保：

- [ ] 我已阅读并遵循本 CONTRIBUTING.md 规范
- [ ] 代码通过了本地测试 (`pytest tests/ -v`)
- [ ] 代码通过了 lint 检查 (`black . && isort . && flake8`)
- [ ] 我已经自测了相关功能
- [ ] 文档已更新（如适用）
- [ ] 没有引入新的 warnings 或 deprecations
- [ ] Commit message 符合第3节的规范

### 4.2 PR 标题格式

```
<type>(<scope>): <description> (#issue-number)

例: feat(solver): add k-epsilon turbulence model (#042)
```

### 4.3 PR 描述模板

PR 创建时会自动加载 `.github/PULL_REQUEST_REQUEST_TEMPLATE.md` 模板。

关键内容：

```markdown
## 变更概述
简要描述这次PR做了什么

## 变变类型
- [ ] 🚀 新功能 (Feature)
- [ ] 🐛 Bug修复 (Bug fix)
- [ ] 📝 文档更新 (Documentation)
- [ ] ♻️ 代码重构 (Refactor)
- [ ] 🧪 测试相关 (Test)
- [ ] 🔧 其他 (Other)

## 相关Issue
Closes #XXX

## 测试计划
- [ ] 单元测试：测试了哪些函数/类
- [ ] 集成测试：验证了哪些场景
- [ ] 手动测试：如何手动验证

## 截图/GIF（UI变更时必须）
[附上前后对比截图]
```

### 4.4 PR 审核流程

```
开发者提交PR → CI自动检查(通过?) → 第一轮审核(@Arch+@QA)
→ 修改意见?(有→修改后重新提交) → 第二轮审核(@PM最终批准)
→ 合并到develop分支
```

**审核响应时间要求**：

| 角色 | 响应时间 |
|------|---------|
| 开发者 | 提交PR后24小时内确保CI通过 |
| 审核者 | PR分配后48小时内给出初审 |
| 最终批准 | PR就绪后24小时内决定 |

---

## 5. Code Review 标准

### 5.1 通用 Checklist

#### 正确性
- [ ] 逻辑是否正确？有无边界 case 遗漏？
- [ ] 是否处理了错误和异常情况？
- [ ] 是否有潜在的除零/越界/空指针问题？

#### 可读性
- [ ] 变量和函数命名是否清晰？
- [ ] 复杂逻辑是否有注释说明？
- [ ] 函数长度是否合理（<50行）？
- [ ] 是否避免了过深的嵌套（<4层）？

#### 性能
- [ ] 是否有不必要的循环或拷贝？
- [ ] 大数据量时的性能表现？
- [ ] 内存使用是否合理？

#### 安全性
- [ ] 是否有注入攻击风险？
- [ ] 敏感数据是否加密存储？
- [ ] 输入是否做了校验？

#### 测试
- [ ] 是否有对应的单元测试？
- [ ] 测试覆盖了正常和异常路径？
- [ ] 测试用例是否具有代表性？

### 5.2 后端专项 (@BE 的代码)

- [ ] 数值算法实现是否符合文献/理论？
- [ ] 数值稳定性是否验证过？
- [ ] 精度是否满足要求？
- [ ] 是否遵循 PEP 8 + Black + isort？
- [ ] 类型注解是否完整？

### 5.3 前端专项 (@FE 的代码)

- [ ] UI 组件职责是否单一？
- [ ] Props/State 使用是否合理？
- [ ] CSS 是否使用了统一的设计系统？
- [ ] 响应式布局是否正确？
- [ ] 加载状态和错误状态是否处理？

---

## 6. Issue 管理

### 6.1 Issue 类型

本项目定义了三种 Issue 模板：

| 模板 | 用途 | 触发场景 |
|------|------|---------|
| `bug_report.yml` | 报告软件缺陷 | 发现Bug时 |
| `feature_request.yml` | 提出新功能建议 | 有新想法时 |
| `documentation_task.yml` | 文档编写任务 | 需要写/更新文档时 |

### 6.2 Issue 生命周期

```
新建(Triaged) → 已指派(Assigned) → 进行中(In Progress)
→ 待审核(Review) → 已完成(Done/Closed)
```

### 6.3 Issue 标签体系

**类型标签**：
- `kind/bug` — 缺陷
- `kind/enhancement` — 增强
- `kind/docs` — 文档
- `kind/refactor` — 重构
- `kind/testing` — 测试

**优先级标签**：
- `priority/critical` ❤️ 紧急 (P0)
- `priority/high` ⚠️ 高 (P1)
- `priority/medium` ➖ 中 (P2)
- `priority/low` ⬇️ 低 (P3)

**状态标签**：
- `status/in-progress` 🔄 进行中
- `status/review` 👀 待审核
- `status/blocked` 🚫 被阻塞

**模块标签**：
- `module/core` — 核心引擎
- `module/ui` — 用户界面
- `module/tests` — 测试
- `module/docs` — 文档

---

## 7. 编码规范

### 7.1 Python 编码规范

本项目严格遵循以下规范：

#### PEP 8 基础规范

```python
# ✅ 正确的命名
class DamBreakConfig:          # PascalCase 类名
    def compute_time_step(self):  # snake_case 方法名
        max_wave_speed = 10.0     # snake_case 变量名
        EPS_H = 1e-12             # UPPER_SNAKE 常量名
```

#### 类型注解（必需）

```python
from typing import Dict, List, Optional, Callable
import numpy as np
from numpy.typing import NDArray

def compute_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    p: int = 2
) -> float:
    """计算p范数误差.

    Args:
        numerical: 数值解数组
        exact: 精确解数组
        p: 范数阶数 (1=L1, 2=L2, inf=L∞)

    Returns:
        p范数误差值
    """
    dx = 1.0 / len(numerical)
    if p == float('inf'):
        return np.max(np.abs(numerical - exact))
    return (np.sum(np.abs(numerical - exact) ** p) * dx) ** (1.0 / p)
```

#### Docstring 规范（Google Style）

```python
class BaseScheme(ABC):
    """有限体积格式抽象基类.

    定义所有数值格式必须实现的接口。
    子类需要实现 evolve() 方法来执行时间推进。

    Attributes:
        name: 格式名称
        order: 精度阶数
        tvd: 是否具有TVD性质
    """

    def __init__(self, name: str, order: int, tvd: bool = False) -> None:
        """初始化格式实例.

        Args:
            name: 格式名称（如 "Lax-Friedrichs"）
            order: 空间精度阶数（1或2）
            tvd: 是否为TVD格式
        """
        self.name = name
        self.order = order
        self.tvd = tvd

    def evolve(
        self,
        U0: NDArray[np.float64],
        config: 'DamBreakConfig'
    ) -> Dict[float, NDArray[np.float64]]:
        """执行时间演化计算.

        Args:
            U0: 初始守恒变量矩阵 (2×nx)
            config: 运行参数配置

        Returns:
            字典 {时刻t: 解状态U}

        Raises:
            ValueError: 当输入参数不合法时
            NotImplementedError: 当子类未实现时
        """
        raise NotImplementedError
```

### 7.2 格式化工具配置

项目已配置自动化格式化工具：

```bash
# 代码格式化 (Black)
black src/ tests/

# 导入排序 (isort)
isort src/ tests/

# 一键格式化 (推荐)
black . && isort .

# 检查是否符合规范 (CI中使用)
black --check .
isort --check-only .
flake8 src/ tests/
mypy src/
```

### 7.3 导入顺序

```python
# 1. 标准库
import os
import sys
from typing import Dict, List

# 2. 第三方库
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 3. 本地模块
from src.core.config import DamBreakConfig
from src.core.schemes.base_scheme import BaseScheme
from src.utils.visualization import plot_water_depth
```

---

## 8. 本地开发命令速查

### 8.1 日常开发

```bash
# 运行应用
streamlit run src/frontend/app.py

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/unit/test_schemes.py -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=src/ --cov-report=html

# 代码格式化
black src/ tests/
isort src/ tests/

# 代码质量检查
flake8 src/ tests/
mypy src/
```

### 8.2 Git 操作速查

```bash
# 查看当前状态
git status
git log --oneline -5

# 创建并切换分支
git checkout -b feature/my-feature

# 添加并提交
git add <files>
git commit -m "type(scope): description"

# 推送分支
git push origin feature/my-feature

# 更新当前分支
git pull origin develop

# 同步最新develop
git fetch origin
git rebase origin/develop
```

### 8.3 问题排查

```bash
# 检查Python环境
python --version
pip list | grep -E "(numpy|scipy|matplotlib|streamlit)"

# 检查导入是否正常
python -c "from src.core import DamBreakConfig; print('OK')"

# 查看测试收集情况
pytest tests/ --collect-only

# 运行单个测试函数
pytest tests/unit/test_schemes.py::TestLaxFriedrichs::test_evolve -v
```

---

## 📞 获取帮助

如果你在贡献过程中遇到任何问题：

1. **查看现有 Issues**: 可能在 [Issues 页面](https://github.com/kaklos-cyber/cfd_class/issues) 有类似问题
2. **创建新 Issue**: 使用对应的模板详细描述你的问题
3. **联系团队**: 通过 Issue @相关角色的成员

---

*最后更新: 2026-05-07 | 维护者: @PM*
