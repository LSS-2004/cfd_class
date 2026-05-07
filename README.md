# CFD-Class: 一维溃坝CFD教学软件

<p align="center">
  <strong>符合GB/T国标的计算流体动力学(CFD)教学软件</strong>
</p>

<p align="center">
  <a href="#-项目简介">简介</a> •
  <a href="#-功能特性">特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-团队成员">团队</a> •
  <a href="#-目录结构">结构</a> •
  <a href="#-开发规范">规范</a>
  <a href="#-license">License</a>
</p>

---

## 📖 项目简介

**CFD-Class** 是一款面向具有流体力学基础知识的学生的一维溃坝问题研究演示教学软件。通过参数化交互探索一维溃坝问题的物理本质、浅水方程数值求解方法、不同有限体积格式在激波捕捉中的表现差异。

### 核心价值

- 🎓 **教学导向**: 从物理背景到数值实现的全链路学习体验
- 🔬 **格式对比**: 6种经典FVM格式的性能与精度对比分析
- 🎮 **交互探索**: 参数化输入 + 实时可视化 + 动画演示
- 📊 **自动报告**: 一键生成符合学术规范的HTML分析报告

### 符合的国家标准

| 标准 | 名称 | 应用场景 |
|------|------|---------|
| GB/T 8567-2006 | 计算机软件文档编制规范 | 全套交付文档 |
| GB/T 9385-2008 | 计算机软件需求规格说明 | 需求规格说明书 |
| GB/T 9386-2008 | 计算机软件测试文档编制规范 | 测试计划与报告 |

---

## ✨ 功能特性

### 四大功能模块

| 模块 | 图标 | 描述 | 状态 |
|------|------|------|------|
| **首页 - 理论背景** | 🏠 | 浅水方程推导、波系结构图解、TVD概念讲解 | 🚧 开发中 |
| **模拟 - 参数运行** | 📊 | 物理参数面板、格式选择器、误差统计表格 | 🚧 开发中 |
| **动画 - 动态可视化** | 🎬 | 时间演化GIF、六格式对比动画、参数扫描 | 🚧 开发中 |
| **报告 - 对比分析** | 📝 | 一键HTML报告、收敛性分析、敏感性矩阵 | 🚧 开发中 |

### 支持的数值格式（共6种）

| 格式 | 阶数 | TVD稳定性 | 适用场景 |
|------|------|----------|---------|
| Lax-Friedrichs | 一阶 | ✅ 强稳定 | 基准对比 |
| Lax-Wendroff | 二阶 | ❌ 光滑区 | 光滑解测试 |
| MacCormack | 二阶 | ❌ 光滑区 | 高效预测校正 |
| Godunov | 一阶+ | ✅ 精确 | 激波捕捉基准 |
| HLL | 一阶+ | ✅ 近似 | 工程实用 |
| MUSCL-Hancock | 二阶 | ✅ TVD | 高精度推荐 |

---

## 🚀 快速开始

### 环境要求

- Python >= 3.10 (推荐 3.10 或 3.11)
- pip 包管理器
- Git 版本控制

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
streamlit run src/frontend/app.py
```

### Docker方式（可选）

```bash
docker build -t cfd-class .
docker run -p 8501:8501 cfd-class
```

访问 http://localhost:8501 查看应用。

---

## 👥 团队成员

本项目由6人团队协作开发，角色分工如下：

| 角色 | 代号 | 主要职责 | 负责模块 |
|------|------|----------|----------|
| 项目经理 | @PM | 统筹管理、需求分析、最终交付 | docs/, 项目管理 |
| 架构师 | @Arch | 系统设计、技术选型、代码审核 | src/core/, 技术决策 |
| 后端开发 | @BE | 核心算法实现、数值求解器 | src/core/schemes/, solvers/ |
| 前端开发 | @FE | UI界面开发、交互设计 | src/frontend/ |
| 测试工程师 | @QA | 质量保障、测试用例、验证确认 | tests/ |
| 文档工程师 | @TW | 技术文档编写、用户手册 | docs/user/, examples/ |

---

## 📁 目录结构

```
CFD_class/
├── .github/                  # GitHub协作配置
│   ├── workflows/            # CI/CD流水线
│   └── ISSUE_TEMPLATE/       # Issue模板
├── docs/                     # 产品交付文档 (GB/T国标)
│   ├── requirements/         # 需求规格说明书
│   ├── design/               # 设计说明书
│   ├── user/                 # 用户手册
│   └── test/                 # 测试文档
├── src/                      # 源代码
│   ├── core/                 # 核心计算引擎
│   │   ├── schemes/          # 6种FVM格式
│   │   ├── solvers/          # Riemann求解器
│   │   └── analysis/         # 分析工具
│   ├── frontend/             # Streamlit前端
│   │   ├── pages/            # 多页面组件
│   │   ├── components/       # UI组件
│   │   └── engines/          # 业务逻辑引擎
│   └── utils/                # 公共工具库
├── tests/                    # 测试代码
├── examples/                 # 示例案例
└── scripts/                  # 构建脚本
```

详见 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解完整的开发规范。

---

## 🛠️ 开发规范

本仓库严格遵循以下标准和流程：

| 规范文档 | 内容 |
|---------|------|
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 贡献者指南、分支策略、Commit规范、PR流程 |
| [PRODUCT_DELIVERY_STANDARD.md](./PRODUCT_DELIVERY_STANDARD.md) | GB/T产品交付规范 |
| [GITHUB_COLLABORATION_GUIDE.md](./GITHUB_COLLABORATION_GUIDE.md) | 团队协同工作流指南 |

### 快速参考

```bash
# 分支策略 (Git Flow)
main        ← 生产环境（仅PM/Arch可合并）
develop     ← 开发集成分支
feature/*   ← 新功能分支
bugfix/*    ← Bug修复分支
hotfix/*    ← 紧急修复分支

# Commit Message格式
type(scope): description

# 类型: feat / fix / docs / style / refactor / test / chore
```

---

## 📊 项目进度

当前版本: **v0.1.0-alpha** (初始化阶段)

| 阶段 | 内容 | 状态 | 完成度 |
|------|------|------|--------|
| Phase 0 | 仓库初始化与标准建立 | ✅ 进行中 | 90% |
| Phase 1 | 核心算法实现 (6种格式) | ⏳ 待开始 | 0% |
| Phase 2 | Streamlit UI开发 (4页面) | ⏳ 待开始 | 0% |
| Phase 3 | 动画与报告引擎 | ⏳ 待开始 | 0% |
| Phase 4 | 测试与文档完善 | ⏳ 待开始 | 0% |
| Phase 5 | 打包交付 | ⏳ 待开始 | 0% |

详细需求规格见 [SRS.md](./docs/requirements/SRS.md)。

---

## 📄 相关文档

| 文档 | 说明 | 国标依据 |
|------|------|---------|
| [SRS.md](./docs/requirements/SRS.md) | 软件需求规格说明书 | GB/T 9385-2008 |
| [SDD.md](./docs/design/SDD.md) | 概要设计说明书 | GB/T 8567 |
| [architecture.md](./docs/design/architecture.md) | 架构设计详细文档 | 自定义 |
| [user_manual.md](./docs/user/user_manual.md) | 用户操作手册 | GB/T 8567 |
| [test_plan.md](./docs/test/test_plan.md) | 测试计划 | GB/T 9386-2008 |

---

## 📈 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.10+ | 核心开发语言 |
| 前端 | Streamlit | Web用户界面 |
| 数值计算 | NumPy, SciPy | 向量运算、方程求解 |
| 可视化 | Matplotlib | 科学绑图、动画生成 |
| 测试 | pytest | 单元测试、集成测试 |
| 代码质量 | Black, isort, flake8, mypy | 格式化、静态检查 |
| 文档 | Sphinx, Markdown | 技术文档 |

---

## 🤝 如何参与贡献

我们欢迎所有形式的贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

详见 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细的贡献流程。

---

## 📝 License

本项目基于 [MIT License](./LICENSE) 开源。

```
Copyright (c) 2026 CFD-Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🙏 致谢

- 感谢所有开源社区提供的优秀工具和库
- 感谢流体力学领域的先驱者们奠定的理论基础
- 感谢GB/T国家标准为软件开发提供的规范化指导

---

<p align="center">
  <sub>Made with ❤️ by CFD-Team | 符合GB/T国标的教学软件</sub>
</p>
