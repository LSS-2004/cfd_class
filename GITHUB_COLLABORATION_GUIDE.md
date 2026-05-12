# CFD-Class GitHub 团队协作指南

| 属性 | 内容 |
|------|------|
| **文档编号** | CFD-CLASS-GCG-001 |
| **版本** | v1.0 |
| **日期** | 2026-05-09 |
| **维护者** | @PM |

---

## 目录

1. [引言](#1-引言)
2. [仓库管理](#2-仓库管理)
3. [分支策略详解](#3-分支策略详解)
4. [Issue 管理](#4-issue-管理)
5. [Pull Request 流程](#5-pull-request-流程)
6. [CI/CD 流程](#6-cicd-流程)
7. [沟通规范](#7-沟通规范)
8. [发布管理](#8-发布管理)
9. [常见问题](#9-常见问题)

---

## 1. 引言

### 1.1 编写目的

本文档旨在为 CFD-Class 项目团队提供一套完整、标准化的 GitHub 协作规范，确保 6 人团队能够高效、有序地进行协同开发，降低沟通成本，保障代码质量与项目进度。

### 1.2 适用范围

本指南适用于所有参与 CFD-Class 项目开发的团队成员，包括以下 6 个角色：

| 角色 | 代号 | 主要职责 |
|------|------|----------|
| 项目经理 | @PM | 统筹管理、需求分析、最终交付审批 |
| 架构师 | @Arch | 系统设计、技术选型、代码终审 |
| 后端开发 | @BE | 核心算法实现、数值求解器开发 |
| 前端开发 | @FE | UI 界面开发、交互设计实现 |
| 测试工程师 | @QA | 质量保障、测试用例设计与执行 |
| 文档工程师 | @TW | 技术文档编写、用户手册维护 |

### 1.3 团队结构

```
        ┌─────────────┐
        │     @PM     │  最终审批 / 发布管理
        └──────┬──────┘
               │
        ┌──────┴──────┐
        │    @Arch    │  技术决策 / 代码终审
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│  @BE  │ │  @FE  │ │  @QA  │  开发执行 / 测试验证
└───────┘ └───────┘ └───┬───┘
                        │
                   ┌────┴────┐
                   │   @TW   │  文档维护
                   └─────────┘
```

---

## 2. 仓库管理

### 2.1 仓库结构说明

```
cfd_class/
├── .github/                  # GitHub 协作配置
│   ├── workflows/            # CI/CD 流水线 (ci.yml, cd.yml)
│   ├── ISSUE_TEMPLATE/       # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md  # PR 模板
├── docs/                     # 产品交付文档 (GB/T 国标)
│   ├── requirements/         # 需求规格说明书
│   ├── design/               # 设计说明书
│   ├── user/                 # 用户手册
│   └── test/                 # 测试文档
├── src/                      # 源代码
│   ├── core/                 # 核心计算引擎
│   │   ├── schemes/          # 6 种 FVM 格式
│   │   ├── solvers/          # Riemann 求解器
│   │   └── analysis/         # 分析工具
│   ├── frontend/             # Streamlit 前端
│   │   ├── pages/            # 多页面组件
│   │   ├── components/       # UI 组件
│   │   └── engines/          # 业务逻辑引擎
│   └── utils/                # 公共工具库
├── tests/                    # 测试代码
│   ├── unit/                 # 单元测试
│   └── integration/          # 集成测试
├── examples/                 # 示例案例
├── scripts/                  # 构建脚本
├── requirements.txt          # 依赖清单
├── pyproject.toml            # 项目配置
└── README.md                 # 项目说明
```

### 2.2 分支保护规则

#### main 分支保护（生产环境）

| 保护项 | 规则 |
|--------|------|
| 强制要求 PR | ✅ 禁止直接推送，必须通过 Pull Request 合并 |
| 最少审核人数 | 2 人（@Arch + @PM） |
| 状态检查 | 必须通过 CI 全部检查 |
| 分支更新 | 要求分支为最新才可合并 |
| 可合并角色 | 仅 @PM 和 @Arch 拥有合并权限 |
| 删除保护 | 禁止删除 main 分支 |

#### develop 分支保护（开发集成）

| 保护项 | 规则 |
|--------|------|
| 强制要求 PR | ✅ 禁止直接推送，必须通过 Pull Request 合并 |
| 最少审核人数 | 1 人（@Arch 或 @QA） |
| 状态检查 | 必须通过 CI 全部检查 |
| 分支更新 | 要求分支为最新才可合并 |
| 删除保护 | 禁止删除 develop 分支 |

### 2.3 权限分配

| 角色 | 仓库权限 | 分支权限 | 特殊权限 |
|------|----------|----------|----------|
| @PM | Admin | 可合并 main/develop | 发布管理、分支保护配置 |
| @Arch | Maintain | 可合并 main/develop | 分支保护配置、代码终审 |
| @BE | Write | 可推送 feature/bugfix 分支 | 无 |
| @FE | Write | 可推送 feature/bugfix 分支 | 无 |
| @QA | Write | 可推送 feature/bugfix 分支 | 测试相关配置 |
| @TW | Write | 可推送 docs 分支 | 无 |

---

## 3. 分支策略详解

### 3.1 Git Flow 工作流

本项目采用 **Git Flow** 分支管理策略，核心分支结构如下：

```
main (生产环境)
  ↑
develop (开发集成)
  ├─ feature/#XXX-description    新功能开发
  ├─ bugfix/#XXX-description     Bug 修复
  ├─ docs/#XXX-description       文档更新
  ├─ test/#XXX-description       测试补充
  └─ hotfix/#XXX-description     紧急修复（从 main 分出）
```

#### 工作流说明

1. **日常开发**：从 `develop` 创建功能分支 → 开发 → PR 合并回 `develop`
2. **版本发布**：`develop` 稳定后 → PR 合并到 `main` → 打标签发布
3. **紧急修复**：从 `main` 创建 `hotfix` 分支 → 修复 → 同时合并回 `main` 和 `develop`

### 3.2 分支类型与创建规则

| 分支类型 | 来源分支 | 目标分支 | 命名规范 | 生命周期 |
|----------|----------|----------|----------|----------|
| feature | develop | develop | `feature/#<issue>-<描述>` | 功能完成后删除 |
| bugfix | develop | develop | `bugfix/#<issue>-<描述>` | 修复完成后删除 |
| docs | develop | develop | `docs/#<issue>-<描述>` | 文档更新后删除 |
| test | develop | develop | `test/#<issue>-<描述>` | 测试补充后删除 |
| hotfix | main | main + develop | `hotfix/#<issue>-<描述>` | 紧急修复后删除 |
| release | develop | main | `release/v<版本号>` | 发布完成后删除 |

### 3.3 分支命名规范

#### 命名格式

```
<type>/#<issue-number>-<short-description>
```

#### 命名示例

```bash
# 功能分支
feature/001-add-tvd-solver
feature/042-implement-muscl-hancock

# Bug 修复分支
bugfix/015-fix-memory-leak-in-mesh
bugfix/023-correct-boundary-condition

# 文档分支
docs/003-update-srs-chapter4
docs/031-add-user-manual-quickstart

# 测试分支
test/028-add-regression-tests-for-hll
test/035-improve-coverage-for-schemes

# 热修复分支
hotfix/004-fix-crash-on-startup
hotfix/009-fix-security-vulnerability
```

#### 命名约束

- 使用小写字母和数字
- 使用连字符 `-` 分隔单词
- 描述长度控制在 3-5 个单词
- 必须关联 Issue 编号
- 禁止使用下划线 `_` 或特殊字符

---

## 4. Issue 管理

### 4.1 Issue 创建规范

#### 创建前检查

- [ ] 搜索现有 Issue，确认没有重复
- [ ] 选择正确的 Issue 模板
- [ ] 标题清晰描述问题或需求
- [ ] 提供足够上下文信息

#### Issue 模板类型

| 模板 | 用途 | 适用场景 |
|------|------|----------|
| `bug_report.yml` | 报告软件缺陷 | 发现 Bug 时 |
| `feature_request.yml` | 提出新功能建议 | 有新想法时 |
| `documentation_task.yml` | 文档编写任务 | 需要写/更新文档时 |

#### 标题规范

```
[<类型>] <简明描述>

示例：
[Bug] 激波捕捉时出现数值振荡
[Feature] 添加收敛性分析图表
[Docs] 补充 MUSCL-Hancock 格式理论说明
```

### 4.2 标签体系说明

#### 类型标签 (kind/)

| 标签 | 颜色 | 说明 |
|------|------|------|
| `kind/bug` | 🔴 | 软件缺陷 |
| `kind/enhancement` | 🟢 | 功能增强 |
| `kind/docs` | 🔵 | 文档相关 |
| `kind/refactor` | 🟣 | 代码重构 |
| `kind/testing` | 🟡 | 测试相关 |

#### 优先级标签 (priority/)

| 标签 | 颜色 | 级别 | 响应时间 |
|------|------|------|----------|
| `priority/critical` | ❤️ | P0 - 紧急 | 立即处理 |
| `priority/high` | ⚠️ | P1 - 高 | 24 小时内 |
| `priority/medium` | ➖ | P2 - 中 | 3 个工作日内 |
| `priority/low` | ⬇️ | P3 - 低 | 排期处理 |

#### 状态标签 (status/)

| 标签 | 说明 |
|------|------|
| `status/in-progress` | 🔄 进行中 |
| `status/review` | 👀 待审核 |
| `status/blocked` | 🚫 被阻塞 |

#### 模块标签 (module/)

| 标签 | 对应模块 |
|------|----------|
| `module/core` | 核心引擎 (src/core/) |
| `module/ui` | 用户界面 (src/frontend/) |
| `module/tests` | 测试 (tests/) |
| `module/docs` | 文档 (docs/) |
| `module/ci` | CI/CD 配置 (.github/workflows/) |

### 4.3 Issue 生命周期管理

```
新建(New)
  ↓
分类(Triaged) —— @PM 或 @Arch 添加标签、评估优先级
  ↓
已指派(Assigned) —— 分配给具体执行人
  ↓
进行中(In Progress) —— 执行人开始处理，添加 status/in-progress
  ↓
待审核(Review) —— 完成开发，提交 PR，添加 status/review
  ↓
已完成(Done) —— PR 合并，关闭 Issue
```

#### 状态转换规则

| 转换 | 触发条件 | 操作人 |
|------|----------|--------|
| New → Triaged | Issue 创建后 | @PM / @Arch |
| Triaged → Assigned | 确定执行人 | @PM |
| Assigned → In Progress | 开始开发 | 执行人 |
| In Progress → Review | 提交 PR | 执行人 |
| Review → Done | PR 合并 | @PM / @Arch |
| 任意 → Blocked | 遇到阻塞 | 执行人 |

### 4.4 任务分配流程

1. **需求提出**：任何角色可创建 Issue
2. **需求评审**：@PM 组织评审，确定优先级和迭代计划
3. **任务指派**：@PM 根据迭代计划指派给具体开发者
4. **开发执行**：开发者按规范完成开发
5. **验收关闭**：PR 合并后，@QA 验证并关闭 Issue

---

## 5. Pull Request 流程

### 5.1 PR 创建规范

#### 创建前检查清单

- [ ] 我已阅读并遵循 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 规范
- [ ] 代码通过了本地测试 (`pytest tests/ -v`)
- [ ] 代码通过了 lint 检查 (`black . && isort . && flake8`)
- [ ] 我已经自测了相关功能
- [ ] 文档已更新（如适用）
- [ ] 没有引入新的 warnings 或 deprecations
- [ ] Commit message 符合规范

#### PR 标题格式

```
<type>(<scope>): <description> (#<issue-number>)

示例：
feat(solver): add k-epsilon turbulence model (#042)
fix(ui): resolve layout overflow on mobile (#015)
docs(srs): update performance requirements chapter (#003)
```

#### PR 描述模板

创建 PR 时会自动加载 `.github/PULL_REQUEST_TEMPLATE.md` 模板，必须包含：

1. **变更概述**：简洁描述这次 PR 做了什么
2. **变更类型**：勾选适用的类型（Feature/Bug fix/Documentation 等）
3. **相关 Issue**：`Closes #XXX`
4. **详细变更说明**：技术实现、设计决策
5. **测试计划**：单元测试、集成测试、手动测试
6. **截图/GIF**：UI 变更时必须附上
7. **影响范围**：勾选受影响的模块
8. **向后兼容性**：是否破坏兼容

### 5.2 Code Review 流程

#### 审核流程图

```
开发者提交 PR
    ↓
CI 自动检查（lint + test + security）
    ↓
通过? ──否──→ 开发者修复，重新提交
    ↓ 是
第一轮审核 (@Arch + @QA)
    ↓
修改意见? ──是──→ 开发者修改，请求重新审核
    ↓ 否
第二轮审核 (@PM 最终批准)
    ↓
合并到目标分支
```

#### 审核响应时间要求

| 角色 | 响应时间 | 说明 |
|------|----------|------|
| 开发者 | 24 小时内 | 提交 PR 后确保 CI 通过 |
| 初审者 | 48 小时内 | PR 分配后给出初审意见 |
| 终审者 | 24 小时内 | PR 就绪后决定是否合并 |

### 5.3 各角色的审核职责

#### @Arch（架构师）审核重点

- [ ] 架构设计是否合理
- [ ] 技术选型是否恰当
- [ ] 代码是否符合设计规范
- [ ] 性能影响评估
- [ ] 是否引入技术债务

#### @QA（测试工程师）审核重点

- [ ] 测试覆盖是否充分
- [ ] 测试用例是否合理
- [ ] 边界条件是否覆盖
- [ ] 是否有回归测试
- [ ] 代码质量指标是否达标

#### @PM（项目经理）终审重点

- [ ] 是否满足需求
- [ ] 是否影响项目进度
- [ ] 风险是否可控
- [ ] 是否可合并发布

#### @BE / @FE / @TW 互审重点

- [ ] 代码逻辑正确性
- [ ] 编码规范遵循情况
- [ ] 可读性和可维护性
- [ ] 与相关模块的兼容性

---

## 6. CI/CD 流程

### 6.1 CI 流水线说明

CI 流水线在以下场景触发：
- Push 到 `develop` 或 `main` 分支
- Pull Request 到 `develop` 或 `main` 分支

#### CI 阶段详解

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Lint     │ → │    Test     │ → │  Security   │ → │    Build    │
│  代码质量    │    │  测试执行    │    │  安全扫描    │    │  构建验证    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

##### Stage 1: Lint（代码风格与质量）

| 检查项 | 工具 | 通过标准 |
|--------|------|----------|
| 代码格式化 | Black | `black --check src/ tests/` |
| 导入排序 | isort | `isort --check-only src/ tests/` |
| 代码规范 | flake8 | 无错误，max-line-length=88 |
| 类型检查 | mypy | 无类型错误 |

##### Stage 2: Test（测试执行）

| 检查项 | 说明 | 通过标准 |
|--------|------|----------|
| 单元测试 | pytest tests/unit/ | 全部通过 |
| 集成测试 | pytest tests/integration/ | 全部通过 |
| 覆盖率 | pytest-cov | ≥ 80% |
| 多版本测试 | Python 3.10 + 3.11 | 均通过 |

##### Stage 3: Security（安全扫描）

| 检查项 | 工具 | 说明 |
|--------|------|------|
| 依赖漏洞 | safety | 检查 requirements.txt 中的已知漏洞 |
| 代码安全 | bandit | 扫描 Python 代码中的安全问题 |

##### Stage 4: Build（构建验证）

| 检查项 | 说明 |
|--------|------|
| 跨平台构建 | Ubuntu / Windows / macOS |
| 包构建 | `python -m build` |
| 导入验证 | 确认模块可正常导入 |

### 6.2 CD 流水线说明

CD 流水线在以下场景触发：
- Push 到 `main` 分支（自动部署文档）
- 推送 `v*` 标签（自动创建 Release）
- 手动触发（workflow_dispatch）

#### Release 创建流程

```
推送版本标签 (如 v1.0.0)
    ↓
提取版本号
    ↓
生成 Release Notes
    ↓
创建 GitHub Release
    ↓
上传构建产物 (.whl, .tar.gz)
```

#### 文档自动部署

```
Push 到 main 分支
    ↓
安装 Sphinx 文档工具
    ↓
构建文档站点
    ↓
部署到 GitHub Pages
```

### 6.3 状态检查要求

#### PR 合并前必须通过的检查

| 检查项 | 必需 | 说明 |
|--------|------|------|
| CI / Lint | ✅ | 代码风格检查 |
| CI / Test (3.10) | ✅ | Python 3.10 测试 |
| CI / Test (3.11) | ✅ | Python 3.11 测试 |
| CI / Security | ✅ | 安全扫描 |
| CI / Build | ✅ | 构建验证 |
| Code Review | ✅ | 至少 1-2 人审核 |

#### 检查失败处理

1. **Lint 失败**：本地运行 `black . && isort .` 修复后重新提交
2. **Test 失败**：修复代码或补充测试后重新提交
3. **Coverage 不足**：补充测试用例，确保覆盖率达到 80%
4. **Security 警告**：评估风险，必要时更新依赖或修复代码

---

## 7. 沟通规范

### 7.1 评论规范

#### 评论基本原则

- **建设性**：提出问题时同时给出改进建议
- **具体性**：指出具体文件、行号、问题
- **尊重性**：保持专业礼貌，对事不对人
- **及时性**：收到评论后及时响应

#### 评论模板

```markdown
## 问题描述
[具体说明问题是什么]

## 建议修改
```python
# 建议的代码
```

## 原因
[解释为什么这样修改更好]

## 优先级
- [ ] 阻塞（必须修改）
- [ ] 建议（推荐修改）
- [ ] 疑问（需要讨论）
```

### 7.2 @提及规则

| 场景 | 提及对象 | 说明 |
|------|----------|------|
| 需要技术决策 | @Arch | 架构设计、技术选型问题 |
| 需要项目决策 | @PM | 进度调整、需求变更、发布计划 |
| 代码有 Bug | @QA | 需要验证或补充测试 |
| 文档问题 | @TW | 文档缺失、描述不清 |
| 后端相关问题 | @BE | 算法实现、性能问题 |
| 前端相关问题 | @FE | UI 问题、交互问题 |
| 需要多人讨论 | @PM @Arch @BE @FE @QA @TW | 重大问题全员参与 |

#### 使用示例

```markdown
@Arch 这个数值格式的边界处理方案需要您确认一下，
我采用了反射边界条件，是否符合设计预期？

@QA 这个 PR 修改了核心求解器，请重点验证激波捕捉场景。

@TW 新添加的 TVD 限制器需要在用户手册中补充说明。
```

### 7.3 通知设置建议

#### 推荐的通知配置

| 角色 | 通知级别 | 说明 |
|------|----------|------|
| @PM | 所有活动 | 关注项目全局动态 |
| @Arch | 提及 + 审查请求 + Issue/PR 创建 | 关注技术相关动态 |
| @BE | 提及 + 审查请求 + 相关模块 Issue | 关注后端相关动态 |
| @FE | 提及 + 审查请求 + 相关模块 Issue | 关注前端相关动态 |
| @QA | 提及 + 审查请求 + 所有 PR | 关注质量相关动态 |
| @TW | 提及 + docs 标签 Issue/PR | 关注文档相关动态 |

#### 通知渠道

- **GitHub 站内通知**：主要渠道，及时查看
- **邮件通知**：作为备份，建议开启
- **Slack/飞书集成**（如有）：实时推送重要事件

---

## 8. 发布管理

### 8.1 版本号规范（SemVer）

本项目采用 [语义化版本控制](https://semver.org/lang/zh-CN/)（Semantic Versioning）：

```
版本格式：主版本号.次版本号.修订号（MAJOR.MINOR.PATCH）

示例：1.2.3
```

#### 版本号递增规则

| 版本类型 | 递增时机 | 示例 |
|----------|----------|------|
| MAJOR | 不兼容的 API 修改 | 1.x.x → 2.0.0 |
| MINOR | 向下兼容的功能新增 | 1.1.x → 1.2.0 |
| PATCH | 向下兼容的问题修复 | 1.1.1 → 1.1.2 |

#### 预发布版本

```
格式：MAJOR.MINOR.PATCH-<预发布标识>.<序号>

示例：
1.0.0-alpha.1   # 内测版
1.0.0-beta.1    # 公测版
1.0.0-rc.1      # 候选发布版
```

### 8.2 Release 创建流程

#### 发布前准备

1. **确认发布内容**
   - 检查所有相关 Issue 已关闭
   - 确认 CHANGELOG.md 已更新
   - 确认版本号已更新（pyproject.toml, __version__）

2. **创建发布分支**（如需要）
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.0.0
   ```

3. **版本冻结**
   - 仅允许 Bug 修复进入发布分支
   - 新功能推迟到下一个版本

#### 发布执行

```bash
# 1. 合并到 main
git checkout main
git merge --no-ff release/v1.0.0

# 2. 打标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 3. 推送标签
git push origin main
git push origin v1.0.0

# 4. 合并回 develop
git checkout develop
git merge --no-ff main
```

#### 发布后验证

- [ ] GitHub Release 页面显示正常
- [ ] 构建产物可下载
- [ ] 文档站点已更新
- [ ] 应用可正常安装运行

### 8.3 变更日志维护

#### CHANGELOG.md 格式

```markdown
# Changelog

## [Unreleased]

### Added
- 新功能描述

### Changed
- 变更描述

### Fixed
- 修复描述

## [1.0.0] - 2026-05-09

### Added
- 初始版本发布
- 支持 6 种 FVM 数值格式
- Streamlit 交互式 UI
```

#### 变更类型说明

| 类型 | 说明 |
|------|------|
| Added | 新功能 |
| Changed | 现有功能的变更 |
| Deprecated | 即将移除的功能 |
| Removed | 移除的功能 |
| Fixed | Bug 修复 |
| Security | 安全相关修复 |

#### 维护责任

- **@TW**：负责 CHANGELOG.md 的格式维护和文字润色
- **各开发者**：在 PR 中提供变更摘要，由 @TW 汇总
- **@PM**：在发布前审核 CHANGELOG 的完整性

---

## 9. 常见问题

### 9.1 冲突解决

#### 场景：合并时发生冲突

```bash
# 1. 获取最新代码
git fetch origin

# 2. 变基到最新 develop
git rebase origin/develop

# 3. 解决冲突（编辑冲突文件）
# 冲突标记格式：
# <<<<<<< HEAD
# 当前分支的代码
# =======
# 目标分支的代码
# >>>>>>> develop

# 4. 标记冲突已解决
git add <冲突文件>

# 5. 继续变基
git rebase --continue

# 6. 强制推送（注意：仅在自己的 feature 分支上）
git push --force-with-lease origin feature/XXX
```

#### 冲突解决原则

1. **先沟通**：与冲突代码的作者沟通，了解意图
2. **保留双方**：尽量保留双方的有效代码
3. **测试验证**：解决冲突后必须重新运行测试
4. **及时提交**：解决后尽快提交，避免再次冲突

### 9.2 回滚操作

#### 场景：需要撤销已合并的代码

```bash
# 方法 1: 使用 git revert（推荐，保留历史）
# 创建一个新的提交，撤销指定提交的更改
git revert <commit-hash>

# 方法 2: 使用 git reset（仅本地未推送时）
# 回退到指定提交，丢弃之后的更改
git reset --hard <commit-hash>

# 方法 3: 回滚 Merge Commit
git revert -m 1 <merge-commit-hash>
```

#### 回滚决策流程

```
发现问题
  ↓
评估影响范围
  ↓
影响大? ──是──→ 立即 revert → 创建 hotfix → 紧急发布
  ↓ 否
创建 bugfix Issue → 在下一个迭代修复
```

### 9.3 紧急修复流程

#### Hotfix 流程图

```
生产环境发现严重 Bug
    ↓
@PM 确认紧急程度
    ↓
从 main 创建 hotfix 分支
    ↓
快速修复（绕过常规迭代）
    ↓
PR 到 main（@Arch + @PM 快速审核）
    ↓
合并到 main，打补丁版本标签
    ↓
同步合并到 develop
    ↓
部署到生产环境
```

#### Hotfix 执行步骤

```bash
# 1. 从 main 创建 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/009-fix-critical-bug

# 2. 修复代码并提交
git add .
git commit -m "fix(core): resolve critical bug in solver (#009)"

# 3. 推送到远程
git push origin hotfix/009-fix-critical-bug

# 4. 创建 PR 到 main（标记为 hotfix，请求紧急审核）

# 5. 合并后，同步到 develop
git checkout develop
git merge --no-ff hotfix/009-fix-critical-bug

# 6. 打补丁标签
git tag -a v1.0.1 -m "Hotfix: resolve critical bug"
git push origin v1.0.1
```

#### Hotfix 注意事项

- **快速响应**：P0 级问题 4 小时内开始修复
- **最小改动**：仅修复问题，不引入其他变更
- **充分测试**：即使紧急，也要验证修复有效
- **文档记录**：事后补充文档，分析根因
- **回顾总结**：在团队会议中分享，避免重复发生

---

## 附录

### A. 快速参考卡片

```bash
# 日常开发流程
git checkout develop
git pull origin develop
git checkout -b feature/XXX-description
# ... 开发 ...
git add .
git commit -m "feat(scope): description"
git push origin feature/XXX-description
# 在 GitHub 创建 PR

# 代码质量检查
black . && isort . && flake8 src/ tests/
pytest tests/ -v

# 更新分支
git fetch origin
git rebase origin/develop
```

### B. 相关文档链接

| 文档 | 路径 | 说明 |
|------|------|------|
| 贡献者指南 | [CONTRIBUTING.md](./CONTRIBUTING.md) | 详细开发规范 |
| 项目说明 | [README.md](./README.md) | 项目概览 |
| PR 模板 | [.github/PULL_REQUEST_TEMPLATE.md](./.github/PULL_REQUEST_TEMPLATE.md) | PR 描述模板 |
| CI 配置 | [.github/workflows/ci.yml](./.github/workflows/ci.yml) | 持续集成配置 |
| CD 配置 | [.github/workflows/cd.yml](./.github/workflows/cd.yml) | 持续部署配置 |

### C. 联系方式

如有疑问或建议，请通过以下方式联系：

- 创建 Issue：使用 `documentation_task.yml` 模板
- 在现有 Issue/PR 中 @PM
- 团队会议中提出

---

*本文档由 CFD-Class 团队维护，遵循 MIT License 开源协议。*

*最后更新: 2026-05-09 | 文档编号: CFD-CLASS-GCG-001 | 版本: v1.0*
