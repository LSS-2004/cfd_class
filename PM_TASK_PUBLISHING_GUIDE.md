# PM任务发布操作手册

> **目标读者**: 项目经理(@PM)
> **版本**: v1.0
> **适用场景**: 首次在GitHub上为CFD-Class项目创建和分配任务

---

## 目录

1. [前置准备](#1-前置准备)
2. [方法一：网页手动创建（推荐）](#2-方法一网页手动创建)
3. [方法二：CLI批量创建（高效）](#3-方法二cli批量创建)
4. [首批推荐任务清单](#4-首批推荐任务清单)
5. [建立Projects看板](#5-建立projects看板)
6. [日常管理技巧](#6-日常管理技巧)

---

## 1. 前置准备

### 1.1 确认你有仓库管理员权限

访问 https://github.com/kaklos-cyber/cfd_class/settings/access ，确认你的角色是 **Admin**。

### 1.2 准备工作环境

- ✅ 浏览器已登录GitHub账号
- ✅ 已阅读 CONTRIBUTING.md 了解团队规范
- ✅ 已准备好任务清单（本文档提供）

### 1.3 （可选）安装GitHub CLI工具

```bash
# Windows (用winget)
winget install GitHub.cli

# 或使用Chocolatey
choco install gh

# 安装后登录
gh auth login
```

---

## 2. 方法一：网页手动创建（推荐新手使用）

### 2.1 创建单个Issue的完整流程

#### Step 1: 打开Issues页面

```
浏览器访问: https://github.com/kaklos-cyber/cfd_class/issues
```

你应该看到一个空白的Issues页面（因为还没有任何Issue）。

#### Step 2: 点击 "New issue" 按钮

页面右上角有一个绿色的 **"New issue"** 按钮，点击它。

#### Step 3: 选择模板

你会看到三个选项：

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🐛 Bug Report          Report a defect or problem         │
│                                                             │
│   ✨ Feature Request      Suggest a new feature             │
│                                                             │
│   📝 Documentation Task  Write or update documentation       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**选择建议**：
- 开发新功能 → 选择 **Feature Request**
- 发现Bug → 选择 **Bug Report**
- 文档工作 → 选择 **Documentation Task**

#### Step 4: 填写Issue内容

以 **Feature Request** 模板为例：

##### **① Title（标题）栏**

填写简洁的任务标题，格式建议：
```
<type>(<scope>): <简短描述> (#编号)

示例:
feat(core): implement Lax-Friedrichs scheme (#001)
test(config): add unit tests for DamBreakConfig (#D2)
docs(examples): write dry-bed Ritter case documentation (#E2)
```

##### **② 功能概述（必填）**

```markdown
实现Lax-Friedrichs有限体积格式，用于一维溃坝问题的数值求解。

这是6种FVM格式中的第一种，将作为教学入门案例和后续格式的参考基线。
```

##### **③ 动机与用例（必填）**

```markdown
为什么需要这个功能:
- LF是最简单的FVM格式，适合作为教学入门案例
- 具有强TVD稳定性，不会产生非物理振荡
- 可用于验证整个计算框架的正确性
- 为后续更复杂格式(MUSCL-Hancock等)提供性能基准

解决什么问题:
- 当前src/core/schemes/目录下没有任何实际可用的格式实现
- 团队需要第一个可运行的格式来验证端到端流程
```

##### **④ 实现方案建议（可选但推荐）**

```markdown
技术方案:
1. 在 src/core/schemes/lax_friedrichs.py 中创建 LaxFriedrichsScheme 类
2. 继承 BaseScheme 抽象基类（已在base_scheme.py中定义）
3. 实现 evolve() 方法:
   - 计算数值粘性通量: F* = (FL + FR)/2 - α*(UR - UL)/2
     其中 α = dx/dt (数值粘性系数)
   - 时间推进循环:
     for n in range(num_steps):
         compute_dt(U, config)
         F_star = compute_lax_friedrichs_flux(U)
         U = U - dt/dx * (F_star[:, 1:] - F_star[:, :-1])
         apply_bc(U)
         enforce_positivity(U)

参考资源:
- SDD.md §3.1.2 BaseScheme接口定义
- Toro (2009) Chapter 6
- 精确解: src/core/solvers/exact_solution.py (待实现)
```

##### **⑤ 优先级和模块（下拉选择）**

```
优先级: [P0-Must have ▼]     ← 选择 P0-Must have
模块:   [core/engine ▼]      ← 选择 core/engine
```

##### **⑥ 确认勾选（自动生成）

保持默认的两个勾选即可。

#### Step 5: 右侧边栏设置（关键！）

在页面右侧，你需要设置以下信息：

```
┌─ Assignees (指派人员) ─────────────────────┐
│                                              │
│  👤 Search or click to assign...            │
│  输入: @BE                                 │
│  点击搜索结果中的 @BE 名字                   │
│                                              │
└──────────────────────────────────────────────┘

┌─ Labels (标签) ─────────────────────────────┐
│                                              │
│  点击 "Labels" → 选择以下标签:               │
│  ✓ kind/enhancement                          │
│  ✓ priority/high                             │
│  ✓ module/core                               │
│  ✓ status/in-progress                       │
│                                              │
└──────────────────────────────────────────────┘

┌─ Projects (项目看板) ───────────────────────┐
│                                              │
│  选择: CFD-Class Sprint 1                   │
│  (如果还没有Project，先跳过这一步)           │
│                                              │
└──────────────────────────────────────────────┘

┌─ Milestone (里程碑) ────────────────────────┐
│                                              │
│  选择: Sprint 1 - Core Engine               │
│  (如果还没有Milestone，先跳过这一步)          │
│                                              │
└──────────────────────────────────────────────┘
```

#### Step 6: 提交Issue

点击页面底部的绿色按钮 **"Submit issue"**。

恭喜！你成功发布了第一个任务！

---

### 2.2 批量创建多个Issue（重复上述步骤）

按照上面的流程，依次创建批次A到批次E的所有Issues。预计每个Issue需要 **2-3分钟**。

**效率提示**：
- 使用浏览器标签页，同时打开多个 "New issue" 页面
- 先填好标题，再逐个填充内容
- 复制粘贴相似的内容（如格式实现的描述可以复用）

---

## 3. 方法二：CLI批量创建（高效）

如果你已安装 `gh` CLI工具，可以使用脚本批量创建：

### 3.1 创建批处理脚本

创建文件 `create_issues.sh`（Linux/Mac）或 `create_issues.ps1`（Windows）:

```powershell
# create_issues.ps1 (Windows PowerShell版本)

$issues = @(
    @{
        title = "chore: configure branch protection rules for main and develop"
        body = @"
Configure branch protection rules per GITHUB_COLLABORATION_GUIDE.md §1.3

**Tasks:**
- [ ] Main branch: Require PR + 2 approvals + CI pass
- [ ] Develop branch: Require PR + 1 approval + CI pass
- [ ] Disallow force pushes
- [ ] Disallow deletions

**Reference:** GITHUB_COLLABORATION_GUIDE.md §1.3
"@
        labels = "chore,priority/critical"
        assignee = "@PM"
    },
    @{
        title = "feat(core): implement DamBreakConfig frozen dataclass (#B1)"
        body = @"
Implement the DamBreakConfig dataclass in src/core/config.py.

**Requirements:**
- Use @dataclass(frozen=True) for immutability
- Include all 8 parameters: h_L, h_R, u_L, u_R, g, CFL, nx, t_end
- Add domain/range validation in __post_init__
- Implement properties: dx, x_grid
- Write comprehensive docstrings and type hints

**Acceptance Criteria:**
- [ ] Can instantiate with default values
- [ ] Invalid parameters raise ValueError with clear message
- [ ] Frozen: cannot modify attributes after creation
- [ ] Passes all unit tests (10+ test cases)

**Reference:** SDD.md §3.1.1
"@
        labels = "feat,priority/high,module/core"
        assignee = "@BE"
    }
    # ... 更多issues
)

foreach ($issue in $issues) {
    Write-Host "Creating issue: $($issue.title)"
    gh issue create `
        --title $issue.title `
        --body $issue.body `
        --labels $issue.labels `
        --assignee $issue.assignee
}
```

### 3.2 运行脚本

```powershell
cd D:\APaper\MyClaudeCode\CFD\CFD_class
.\create_issues.ps1
```

---

## 4. 首批推荐任务清单

### 4.1 立即发布的20个Issues（按执行顺序）

详见本文档第二节的完整表格。以下是快速复制版：

#### **批次A: 基础设施（4个，@PM）**

| # | 标题 | Assignee | Labels |
|---|------|----------|--------|
| A1 | `chore: configure branch protection rules` | @PM | chore,critical |
| A2 | `chore: create complete label system (12 labels)` | @PM | chore,high |
| A3 | `chore: invite team members and set permissions` | @PM | chore,critical |
| A4 | `docs: setup GitHub Projects Sprint 1 board` | @PM | docs,high |

#### **批次B: 核心引擎（10个，@BE）**

| # | 标题 | Assignee | Labels | Est. |
|---|------|----------|--------|-------|
| B1 | `feat(core): implement DamBreakConfig` | @BE | feat,high,core | 2h |
| B2 | `feat(core): implement exact Riemann solver` | @BE | feat,high,core | 6h |
| B3 | `feat(core): implement HLL approximate flux` | @BE | feat,high,core | 2h |
| B4 | `feat(core): implement BaseScheme abstract class` | @BE | feat,high,core | 2h |
| B5 | `feat(core): implement Lax-Friedrichs scheme` | @BE | feat,high,core | 4h |
| B6 | `feat(core): implement Lax-Wendroff scheme` | @BE | feat,high,core | 4h |
| B7 | `feat(core): implement MacCormack scheme` | @BE | feat,medium,core | 4h |
| B8 | `feat(core): implement Godunov exact scheme` | @BE | feat,high,core | 4h |
| B9 | `feat(core): implement HLL scheme` | @BE | feat,high,core | 3h |
| B10 | `feat(core): implement MUSCL-Hancock TVD scheme` | @BE | feat,high,core | 8h |

#### **批次C: 前端UI（4个，@FE）**

| # | 标题 | Assignee | Labels | Est. |
|---|------|----------|--------|-------|
| C1 | `feat(ui): create app.py entry point with sidebar nav` | @FE | feat,high,ui | 2h |
| C2 | `feat(ui): implement param_panel component` | @FE | feat,high,ui | 4h |
| C3 | `feat(ui): implement scheme_selector component` | @FE | feat,high,ui | 2h |
| C4 | `feat(ui): implement result_viewer component` | @FE | feat,medium,ui | 4h |

#### **批次D: 测试（3个，@QA）**

| # | 标题 | Assignee | Labels | Est. |
|---|------|----------|--------|-------|
| D1 | `test: setup pytest framework and conftest.py` | @QA | test,high,tests | 2h |
| D2 | `test: write DamBreakConfig unit tests (10 cases)` | @QA | test,high,tests | 2h |
| D3 | `test: write scheme unit tests for all 6 formats` | @QA | test,high,tests | 6h |

#### **批次E: 文档（3个，@TW）**

| # | 标题 | Assignee | Labels | Est. |
|---|------|----------|--------|-------|
| E1 | `docs: complete SRS Chapter 3 acceptance criteria` | @TW | docs,medium | 3h |
| E2 | `docs: write dry_bed_ritter example case docs` | @TW | docs,medium | 2h |
| E3 | `docs: write wet_bed_general example case docs` | @TW | docs,low | 2h |

---

## 5. 建立Projects看板

### 5.1 为什么需要Projects看板？

- ✅ 可视化所有任务的进度状态
- ✅ 方便团队成员了解整体进展
- ✅ 便于Sprint规划和管理
- ✅ 自动同步Issue状态

### 5.2 创建步骤

#### Step 1: 进入Projects页面

```
访问: https://github.com/kaklos-cyber/cfd_class/projects
点击 "New Project"
```

#### Step 2: 选择项目类型

选择 **"Team managed"** （团队管理型）

#### Step 3: 设置项目信息

```
Name: CFD-Class Sprint 1
Description: 一维溃坝CFD教学软件 - 第一个Sprint的核心引擎开发
Visibility: Private (仅成员可见)
```

#### Step 4: 配置看板列（Columns）

创建以下列：

```
┌──────────┬───────────┬────────────┬──────────┬──────────┐
│  Backlog  │ In Progress│   Review   │  Testing │   Done   │
│  (待办)   │ (进行中)  │  (待审核)   │ (测试中)  │  (完成)  │
└──────────┴───────────┴────────────┴──────────┴──────────┘
```

#### Step 5: 将Issues添加到看板

有两种方式：

**方式1**: 手动添加
- 在每个Issue右侧边栏的 "Projects" 下拉框中选择 "CFD-Class Sprint 1"
- Issue会自动出现在 "Backlog" 列

**方式2**: 批量添加
- 在Project页面点击 "+"
- 选择 "Add issues"
- 批量选择要添加的Issues

### 5.3 看板管理最佳实践

#### 每日站会时查看看板

```
查看每列的Issue数量:
- Backlog: 是否有可以开始的任务？
- In Progress: 是否有人负载过重？
- Review: 有哪些PR等待审核？
- Testing: QA是否在测试？
- Done: 本周完成了多少？
```

#### WIP限制（Work In Progress限制）

建议设置：
- **In Progress列**: 最多3个Issue（避免并行过多）
- **Review列**: 最多5个PR（及时审核）

---

## 6. 日常管理技巧

### 6.1 PM每日检查清单（5分钟）

每天早上打开GitHub，检查：

```
□ 1. 查看 Issues 页面
   - 新增的Issues？需要分类或指派吗？
   - 有人@你了吗？需要回复吗？
   
□ 2. 查看 Pull Requests 页面
   - 有新的PR需要审核吗？
   - 有PR被Comment了吗？需要回应吗？
   
□ 3. 查看 Projects 看板
   - 各列Issue数量是否合理？
   - 是否有阻塞超过2天的Issue？
   
□ 4. 快速浏览 Activity
   - 团队成员昨天的提交情况
   - 是否有异常活动？
```

### 6.2 高效使用快捷键

在GitHub Issues页面上：

```
快捷键:
- c  → 打开创建新Issue的对话框
- e  → 编辑当前Issue
- l  → 打开标签选择器
- a  → 打开指派选择器
- m  → 打开里程碑选择器
- ?  → 查看所有快捷键帮助
```

### 6.3 使用Issue模板提高效率

你已经配置了3个Issue模板（bug_report / feature_request / documentation_task），团队成员创建Issue时会自动加载对应模板，确保信息完整。

### 6.4 定期清理和维护

**每周五（Sprint结束时）**：

```
□ 关闭已完成的Issues
□ 将未完成的Issues移到下一个Sprint
□ 更新Milestone进度
□ 整理标签（合并重复的、删除无用的）
□ 写Sprint总结报告
```

---

## 附录A: Issue标题命名规范速查

```
格式: <type>(<scope>): <description> (#编号)

Type类型:
  feat     → 新功能
  fix      → Bug修复
  docs     → 文档变更
  test     → 测试相关
  refactor → 代码重构
  chore    → 构建/工具链
  style    → 代码格式
  perf     → 性能优化

Scope范围:
  core     → src/core/
  ui       → src/frontend/
  config   → 配置相关
  test     → tests/
  docs     → docs/
  ci       → .github/workflows/

示例:
  feat(core): add TVD limiter support (#015)
  fix(ui): resolve sidebar collapse bug (#023)
  docs(examples): add convergence study case (#E4)
  test(schemes): add boundary condition tests (#D7)
```

---

## 附录B: 标签体系完整列表

### 类型标签 (kind/*)
- kind/bug 🔴
- kind/enhancement 🟣
- kind/docs 🔵
- kind/refactor 🟡
- kind/testing 🟢

### 优先级标签 (priority/*)
- priority/critical ❤️ (P0)
- priority/high ⚠️ (P1)
- priority/medium ➖ (P2)
- priority/low ⬇️ (P3)

### 模块标签 (module/*)
- module/core
- module/ui
- module/tests
- module/docs
- module/infrastructure

### 状态标签 (status/*)
- status/in-progress 🔄
- status/review 👀
- status/blocked 🚫

---

*文档结束*
*最后更新: 2026-05-07 | 维护者: @PM*
