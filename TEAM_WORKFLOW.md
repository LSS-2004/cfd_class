# CFD-Class 团队成员工作流程指南

> **版本**: V1.0  
> **更新日期**: 2026-05-09  
> **适用对象**: 所有开发团队成员 (@PM, @BE, @FE, @QA, @TW, @Arch)  
> **预计阅读时间**: 15分钟 (快速开始 5分钟)

---

## 📋 目录

1. [快速开始 (5分钟)](#-快速开始-5分钟)
2. [日常开发工作流](#-日常开发工作流)
3. [Git 命令速查表](#-git-命令速查表)
4. [Issue 管理规范](#-issue-管理规范)
5. [代码审核流程](#-代码审核流程)
6. [各角色职责详解](#-各角色职责详解)
7. [常见问题与解决方案](#-常见问题与解决方案)

---

## 🚀 快速开始 (5分钟)

### 第1步: 克隆仓库

```bash
# 克隆仓库到本地
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class

# 查看远程分支
git branch -r
```

### 第2步: 配置开发环境

```bash
# 创建虚拟环境 (推荐)
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证安装成功
python -c "import streamlit; import numpy; print('✅ Environment ready!')"
```

### 第3步: 查看你的任务

```bash
# 使用 GitHub CLI 查看分配给你的 Issues
gh issue list --assignee @你的GitHub用户名

# 或者在浏览器访问:
# https://github.com/kaklos-cyber/cfd_class/issues?q=is%3Aissue+is%3Aopen+assignee%3A%40你的用户名
```

### 第4步: 开始第一个任务

```bash
# 1. 切换到 develop 分支 (永远不要直接在 main 上工作!)
git checkout develop
git pull origin develop

# 2. 为你的任务创建功能分支
# 格式: feature/任务编号-简短描述
git checkout -b feature/#B1-dambreak-config

# 3. 开始编码...
# (编辑文件, 运行测试)

# 4. 提交你的更改
git add .
git commit -m "feat(core): implement DamBreakConfig class (#B1)"

# 5. 推送到远程仓库
git push origin feature/#B1-dambreak-config

# 6. 创建 Pull Request
gh pr create --base develop \
  --title "feat(core): implement DamBreakConfig class (#B1)" \
  --body "## Summary\n\nCompleted DamBreakConfig dataclass implementation.\n\n## Changes\n- Added src/core/config.py\n- Implemented validation logic\n- Added unit tests\n\n## Test Results\n- All tests passing ✅\n- Coverage: 92%"
```

**恭喜! 你已经完成了第一个任务的提交流程! 🎉**

---

## 🔄 日常开发工作流

### 每日工作流程 (推荐)

```
早晨开始工作时:
┌─────────────────────────────────────┐
│ 1. git checkout develop             │
│ 2. git pull origin develop          │
│ 3. git checkout your-feature-branch│
│ 4. git merge develop               │
│ 5. 开始工作                         │
└─────────────────────────────────────┘

工作中:
┌─────────────────────────────────────┐
│ • 编码                              │
│ • 频繁提交 (每完成一个小功能点)      │
│ • 本地测试                          │
└─────────────────────────────────────┘

下班前 / 完成功能时:
┌─────────────────────────────────────┐
│ 1. 运行完整测试套件                  │
│ 2. git push origin your-branch      │
│ 3. 创建/更新 PR                     │
│ 4. 回复 reviewer 的评论              │
└─────────────────────────────────────┘
```

### 分支策略 (Git Flow)

我们采用 **Git Flow** 工作流:

```
main (生产分支)
  ↑ 合并经过充分测试的功能
  │
develop (开发主分支)
  ↑ PR合并到这里
  │
  ├── feature/#B1-xxx    ← 你的功能分支
  ├── feature/#B2-xxx
  ├── feature/#C1-xxx
  ├── bugfix/#xxx        ← Bug修复分支
  └── hotfix/#xxx        ← 紧急修复(从main分出)
```

#### 分支命名规则:

| 类型 | 格式 | 示例 |
|------|------|------|
| 新功能 | `feature/#编号-简短描述` | `feature/#B5-upwind-scheme` |
| Bug修复 | `bugfix/#编号-描述` | `bugfix/#42-fix-memory-leak` |
| 文档 | `docs/#编号-描述` | `docs/#E1-complete-srs` |
| 重构 | `refactor/#描述` | `refactor/improve-flux-calculation` |

---

## 💻 Git 命令速查表

### 基础操作

```bash
# ===== 初始化与克隆 =====
git clone <url>                    # 克隆仓库
git status                         # 查看当前状态
git log --oneline -10              # 查看最近10条提交

# ===== 分支操作 =====
git branch -a                      # 查看所有分支(本地+远程)
git checkout -b new-branch         # 创建并切换到新分支
git branch -d branch-name          # 删除本地分支

# ===== 同步远程 =====
git fetch origin                   # 获取远程更新(不合并)
git pull origin develop            # 拉取并合并develop
git push origin your-branch        # 推送你的分支

# ===== 提交操作 =====
git add <file>                     # 暂存文件
git add .                          # 暂存所有更改
git commit -m "type(#id): message" # 提交(遵循规范!)
git commit --amend                 # 修改最近一次提交(谨慎使用!)

# ===== 合并与变基 =====
git merge develop                  # 将develop合并到当前分支
git rebase develop                 # 将当前分支变基到develop(保持历史整洁!)
```

### 提交信息规范 (Conventional Commits)

```
格式: type(scope): subject (#issue-number)

类型 (type):
  feat     - 新功能
  fix      - Bug修复
  docs     - 文档变更
  style    - 代码格式(不影响功能)
  refactor - 重构(既不是新功能也不是修复)
  test     - 测试相关
  chore    - 构建/工具/辅助工具变更

示例:
  feat(core): implement Riemann solver (#B2)
  fix(ui): correct animation timing issue (#C3)
  docs(readme): update installation guide
  test(config): add validation edge cases (#D2)
  refactor(schemes): extract base class methods
  style(core): apply black formatting
  chore(ci): update pytest configuration
```

---

## 📝 Issue 管理规范

### Issue 状态流转

```
Backlog → In Progress → Review → Testing → Done
   ↓          ↓           ↓         ↓        ↓
 (待办)    (进行中)   (待审核)  (测试中)  (已完成)
```

### 如何认领和更新 Issue

#### 1. 认领任务

```bash
# 方法1: 使用 GitHub CLI
gh issue take #Issue编号

# 方法2: 在网页上操作
# 打开 Issue → 右侧 Assignees → 选择你自己
```

#### 2. 更新进度

**开始工作时:**
```bash
# 添加 "in-progress" 标签
gh issue edit #编号 --add-label "status/in-progress"

# 可选: 在 Issue 中评论
gh issue comment #编号 --body "🔄 Started working on this task. ETA: ~2 days"
```

**完成草稿时:**
```bash
# 添加 "review" 标签
gh issue edit #编号 --remove-label "status/in-progress" --add-label "status/review"

# 评论说明已完成
gh issue comment #编号 --body "✅ Draft complete. Ready for review. PR: #PR编号"
```

**遇到阻塞时:**
```bash
# 添加 "blocked" 标签
gh issue edit #编号 --add-label "status/blocked"

# 详细说明阻塞原因
gh issue comment #编号 --body "⛔ Blocked by: 需要等待 B2 (Riemann solver) 完成. 
@BE 请优先处理 B2."
```

### Issue 评论模板

```markdown
## Progress Update

**Status**: 🔨 In Progress / ⏸️ Pending Review / ✅ Complete / ⛔ Blocked

**Work Completed**:
- [x] 完成了什么...

**Current Work**: 
- 正在做什么...

**Blockers** (if any):
- 有什么阻碍...

**Next Steps**:
- 下一步计划...

**Questions** (if any):
- 有什么问题需要讨论...
```

---

## 👀 代码审核流程

### 提交 PR 前的自检清单

在创建 Pull Request 前，请确保:

- [ ] **代码质量**
  - [ ] 遵循 PEP 8 代码风格 (已运行 `black`, `isort`)
  - [ ] 无 lint 错误 (`flake8` 通过)
  - [ ] 类型注解完整 (`mypy` 通过)
  
- [ ] **测试覆盖**
  - [ ] 新增功能的单元测试覆盖率 ≥ 目标值
  - [ ] 所有现有测试仍然通过 (`pytest` 全绿)
  - [ ] 边界情况和异常处理有测试
  
- [ ] **文档**
  - [ ] 公共函数/类有 docstring
  - [ ] 复杂算法有注释说明
  - [ ] README/CHANGELOG 已更新(如适用)
  
- [ ] **提交历史**
  - [ ] 提交信息符合规范
  - [ ] 一次提交只做一件事
  - [ ] 无敏感信息(token, 密码等)

### 创建高质量 PR

```bash
# 创建 PR 时包含详细信息
gh pr create --base develop \
  --title "feat(core): implement HLL Riemann solver (#B3)" \
  --body '## 📋 变更概述 (Summary)
实现HLL近似黎曼求解器，作为精确求解器的鲁棒替代方案。

## 🔧 主要改动 (Changes)
- 新增 `src/core/riemann.py` 中 HLLSolver 类
- 实现 Davis (1988) 和 Einfeldt (1991) 波速估计方法
- 与精确求解器的对比测试
- 性能基准测试 (5x 加速)

## ✅ 测试结果 (Test Results)
- 单元测试: 18/18 通过 ✅
- 覆盖率: 87% (目标 ≥85%) ✅
- 集成测试: 通过 ✅
- 性能: 0.3ms/call (精确求解器: 1.5ms/call) 🚀

## 📊 截图/Screenshot (如果涉及UI变更)
[在此处添加截图]

## 🔄 关联 Issue
Closes #B3

## ⚠️ 注意事项 (Notes for Reviewers)
- 波速估计方法可在初始化时选择 (默认 Davis)
- 干河床情况已测试通过
- 与 B2 (精确求解器) 对比误差 < 1% (光滑区域)

## 📝 Checklist
- [x] 代码遵循项目风格指南
- [x] 自测通过
- [x] 文档已更新
- [x] 无破坏性变更'
```

### 审核流程图

```
开发者提交 PR
     ↓
自动CI检查 (lint + test)
     ↓ (通过)                    ↓ (失败)
@Arch/@PM 初审                开发者修复后重新提交
     ↓
代码审核 (至少1人审核)
     ↓ (批准)                  ↓ (请求修改)
@PM/@Arch 终审 (main分支需2人)  开发者修改并回复
     ↓
合并到 develop
     ↓
触发 CI + 部署到测试环境
     ↓
@QA 进行集成测试
     ↓ (通过)
Sprint 结束时合并到 main
```

### 回复审核意见

当收到审核反馈时:

```markdown
## Response to Review

感谢 @reviewer-name 的详细审核!

### 已完成的修改:
- [x] 问题1: 已按照建议重构了 XXX
- [x] 问题2: 已添加单元测试覆盖 YYY

### 需要进一步讨论的:
- **问题3**: 关于 ZZZ 的实现方式, 我选择了方案A因为... 
  如果您认为方案B更好, 请告知原因.

### 未采纳的建议及原因:
- **问题4**: 暂未修改 AAA 部分, 因为这与 #未来Issue 相关,
  计划在该Issue中统一处理.
```

---

## 👥 各角色职责详解

### @PM (项目经理)

**主要职责**:
- 项目规划和进度管理
- 仓库基础设施维护
- 团队协调和沟通
- 文档标准化

**本周任务 (Sprint 1)**:
- [ ] #A1: 配置分支保护规则
- [ ] #A2: 创建标签体系和Milestone
- [ ] #A3: 发布团队工作流程指南 (本文档!)
- [ ] #A4: 设置Projects看板

**常用命令**:
```bash
# 查看整体进度
gh issue list --state open --json number,title,labels,assignees

# 查看 Milestone 进度
gh api repos/kaklos-cyber/cfd_class/milestones --jq '.[] | select(.title=="Sprint 1")'

# 批量创建/管理 Issues (使用脚本)
python scripts/create_issues.py
```

---

### @BE (后端工程师 - 核心引擎)

**主要职责**:
- 实现数值计算核心引擎
- 开发有限体积法数值格式
- 确保计算精度和性能

**本周任务 (Sprint 1)**:
- [ ] #B1: DamBreakConfig 配置类
- [ ] #B2: 精确 Riemann 求解器
- [ ] #B3: HLL 近似求解器
- [ ] #B4: BaseScheme 抽象基类
- [ ] #B5-B10: 6种数值格式实现

**开发顺序建议**:
```
B1 (配置) → B4 (基类) → B2/B3 (黎曼解) 并行 → B5-B10 (格式实现)
```

**代码位置**:
```
src/core/
├── config.py          # B1
├── riemann.py         # B2, B3
└── schemes/
    ├── __init__.py
    ├── base.py        # B4
    ├── upwind.py      # B5
    ├── lax_friedrichs.py  # B6
    ├── lax_wendroff.py    # B7
    ├── maccormack.py      # B8
    ├── beam_warming.py    # B9
    └── fromm.py           # B10
```

---

### @FE (前端工程师 - 用户界面)

**主要职责**:
- 构建Streamlit用户界面
- 实现交互式可视化系统
- 参数输入和结果展示组件

**本周任务 (Sprint 1)**:
- [ ] #C1: Streamlit 主入口和多页面结构
- [ ] #C2: 参数输入面板组件
- [ ] #C3: 可视化和动画系统
- [ ] #C4: 方案对比仪表板

**依赖关系**:
- C1 可以立即开始 (不依赖后端)
- C2-C4 需要 B1 完成后才能完全集成测试

**代码位置**:
```
streamlit_app.py       # C1: 主页面
pages/
├── 1_Simulation.py    # C1+C2+C3: 模拟页面
├── 2_Comparison.py    # C4: 对比页面
└── 3_Theory.py        # 未来: 理论教学页
src/frontend/
├── components/        # C2: UI组件
└── visualization/     # C3: 绘图模块
```

---

### @QA (质量保证工程师)

**主要职责**:
- 搭建测试框架
- 编写单元/集成/回归测试
- 维护CI/CD流水线

**本周任务 (Sprint 1)**:
- [ ] #D1: pytest框架搭建和CI集成
- [ ] #D2: 核心引擎单元测试
- [ ] #D3: 集成测试和回归测试

**测试目标**:
| 模块 | 目标覆盖率 | 测试数量 |
|------|-----------|---------|
| B1 Config | ≥90% | 15+ |
| B2 Riemann | ≥85% | 20+ |
| B3 HLL | ≥85% | 15+ |
| B4-B10 Schemes | ≥85-90% | 各12-18个 |
| **总体** | **≥80%** | **150+** |

**代码位置**:
```
tests/
├── conftest.py              # D1: 共享fixtures
├── unit/
│   ├── test_config.py       # D2
│   ├── test_riemann.py      # D2
│   └── test_schemes/        # D2
├── integration/
│   ├── test_full_simulation.py  # D3
│   └── test_regression.py       # D3
└── performance/
    └── bench_schemes.py
.github/workflows/
└── ci.yml                   # D1: CI配置
```

---

### @TW (技术写手 - 文档工程师)

**主要职责**:
- 编写和维护技术文档
- 确保符合GB/T国家标准
- 创建用户手册和教程

**本周任务 (Sprint 1)**:
- [ ] #E1: 完善 SRS (软件需求规格说明书)
- [ ] #E2: 完善 SDD (软件设计文档)
- [ ] #E3: 创建用户手册和理论指南

**文档标准**:
- GB/T 9385-2008 《计算机软件需求规格说明》
- GB/T 8567-2006 《计算机软件文档编制规范》
- 中英文术语对照表

**文档位置**:
```
docs/
├── requirements/
│   └── SRS.md            # E1: 需求规格说明书
├── design/
│   └── SDD.md            # E2: 设计文档
├── user_manual/
│   ├── installation.md   # E3: 安装指南
│   ├── quick_start.md    # E3: 快速开始
│   └── user_guide.md     # E3: 用户手册
└── theory/
    └── numerical_methods.md  # E3: 数值方法理论
```

---

### @Arch (架构师 - 技术审核)

**主要职责**:
- 技术方案审核
- 代码质量和架构把关
- 解决关键技术难题

**参与流程**:
- 审核 PR 到 main 分支的合并 (必须2人审批: PM + Arch)
- 参与 Sprint Planning 和技术决策
- 回答团队技术疑问

**审核重点**:
- ✅ 设计模式和架构合理性
- ✅ 算法正确性和数值稳定性
- ✅ 代码可维护性和扩展性
- ✅ 性能和安全性考虑
- ✅ 符合GB/T标准和行业最佳实践

---

## ❓ 常见问题与解决方案

### Q1: Git 冲突如何解决?

```bash
# 1. 先拉取最新代码
git fetch origin
git merge origin/develop

# 2. 查看冲突文件
git status  # 会显示 "both modified"

# 3. 手动编辑冲突文件
# 查找 <<<<<<<, =======, >>>>>>> 标记
# 保留需要的代码, 删除标记

# 4. 标记冲突已解决
git add <conflicted-file>
git commit  # 自动生成merge commit

# 5. 继续工作或推送
git push origin your-branch

# 如果遇到困难, 可以请求帮助:
gh issue comment #编号 --body "@Arch @PM 遇到Git冲突, 请求协助解决"
```

### Q2: 我的任务被阻塞了怎么办?

```bash
# 1. 更新 Issue 状态
gh issue edit #编号 --add-label "status/blocked"

# 2. 在 Issue 中详细说明
gh issue comment #编号 --body """⛔ 任务被阻塞

**阻塞原因**: 等待 #XXX (其他任务) 完成

**影响**: 无法继续开发 YYY 功能

**建议**: 
- @相关负责人 能否优先处理 #XXX?
- 或者我可以先并行开发 ZZZ 部分?

**预估延迟**: ~2天"""

# 3. 同时通知相关人员 (可选)
# 在团队的 Slack/微信/Discord 群组中提及
```

### Q3: 如何请求紧急帮助?

**优先级分级**:
- 🔴 **P0/Critical**: 阻塞整个团队 → 立即联系 @PM + @Arch
- 🟠 **P1/High**: 阻塞自己的关键路径 → Issue评论 + @相关人
- 🟡 **P2/Medium**: 一般技术问题 → Issue评论 或 Discussions
- 🟢 **P3/Low**: 改进建议/疑问 → Discussions 或 等待下次会议

### Q4: CI 测试失败了怎么办?

```bash
# 1. 查看失败日志
# 在 PR 页面点击红色的 "X" 详情

# 2. 本地重现错误
pip install -r requirements.txt
pytest tests/unit/test_xxx.py -v  # 运行失败的测试

# 3. 修复代码
# ... 编辑文件 ...

# 4. 验证修复
pytest  # 运行全部测试

# 5. 提交修复
git add .
git commit -m "fix(tests): resolve CI failure in xxx"
git push origin your-branch

# CI会自动重新运行
```

### Q5: 如何编写好的提交信息?

❌ **差的例子**:
```
fix bug
update
asdf
done
```

✅ **好的例子**:
```
feat(core): implement HLL wave speed estimation (#B3)

Add Davis (1988) two-rarefaction and Einfeldt (1991) PVDE 
methods for estimating left/right wave speeds in HLL solver.
Includes unit tests comparing with exact solution.
```

### Q6: 代码风格要求?

本项目强制执行:

```bash
# 格式化代码
black src/ tests/
isort src/ tests/

# Lint 检查
flake8 src/ tests/

# 类型检查
mypy src/

# 一键全部检查 (在CI中也会运行)
pre-commit run --all-files
```

**IDE 配置推荐**:
- VS Code: 安装 Python, Black, isort, flake8, mypy 扩展
- PyCharm: 启用 Black integration, 配置 code style

---

## 📚 重要链接和资源

### 项目资源
- **GitHub 仓库**: https://github.com/kaklos-cyber/cfd_class
- **Issues 看板**: https://github.com/kaklos-cyber/cfd_class/projects
- **Projects Dashboard**: https://github.com/kaklos-cyber/cfd_class/projects/1

### 文档索引
- [README.md](./README.md) - 项目概览和快速开始
- [CONTRIBUTING.md](./CONTRIBUTING.md) - 详细贡献指南和代码规范
- [TEAM_WORKFLOW.md](./TEAM_WORKFLOW.md) - **本文档**
- [PM_TASK_PUBLISHING_GUIDE.md](./PM_TASK_PUBLISHING_GUIDE.md) - PM任务发布指南

### 外部参考
- [Git 官方文档](https://git-scm.com/doc)
- [GitHub Skills](https://skills.github.com/)
- [Streamlit 文档](https://docs.streamlit.io/)
- [pytest 最佳实践](https://docs.pytest.org/goodpractices.html)

---

## 📞 联系方式和沟通渠道

### 正式沟通 (记录留痕)
- **GitHub Issues**: 任务、Bug、功能请求
- **Pull Requests**: 代码审核和技术讨论
- **GitHub Discussions**: 一般性问题和知识分享

### 即时沟通 (紧急事项)
- **团队群组**: [在此处填入群组名称和链接]
- **邮件**: team@cfd-class.org (如需要)

### 定期会议
- **Sprint Planning**: 每个 Sprint 开始时 (1小时)
- **Daily Standup**: 每日早上 (15分钟, 可选)
- **Sprint Review**: 每个 Sprint 结束时 (30分钟)
- **Retrospective**: Review 后进行 (30分钟)

---

## ✅ 检查清单: 我可以开始了吗?

在你开始第一个任务前, 请确认:

- [ ] ✅ 已成功克隆仓库
- [ ] ✅ 已创建并激活Python虚拟环境
- [ ] ✅ 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] ✅ 已配置 Git 用户信息 (`git config user.email/name`)
- [ ] ✅ 已阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解代码规范
- [ ] ✅ 已查看自己被分配的 Issues
- [ ] ✅ 了解本文档的工作流程

**全部完成? 太棒了! 现在可以开始了! 🚀**

---

## 📝 文档版本历史

| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|----------|
| V1.0 | 2026-05-09 | @PM | 初始版本, 包含完整工作流程 |

---

*最后更新: 2026-05-09 by @PM*  
*如有疑问或建议, 请在 GitHub Discussions 中提出或联系 @PM*