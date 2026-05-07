# 版本变更记录

> **项目**: CFD-Class 一维溃坝CFD教学软件
> **格式**: 基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
> **版本**: v0.1.0-alpha

---

## [Unreleased]

### 新增 (Added)
- 初始化标准化仓库结构与GB/T文档框架
- 添加完整的项目开发规范(CONTRIBUTING.md)
- 建立CI/CD自动化流水线
- 创建Issue/PR协作模板

### 变更 (Changed)
- N/A (初始版本)

### 修复 (Fixed)
- N/A

### 移除 (Removed)
- N/A

### 安全 (Security)
- N/A

---

## [0.1.0-alpha] - 2026-05-07

### 新增 (Added)
- ✅ 完整的GB/T标准目录结构
- ✅ README.md - 项目介绍与快速开始
- ✅ CONTRIBUTING.md - 团队协作规范指南
- ✅ SRS.md - 软件需求规格说明书(框架版)
- ✅ SDD.md - 概要设计说明书(框架版)
- ✅ user_manual.md - 用户操作手册
- ✅ quick_start.md - 快速入门指南
- ✅ test_plan.md - 测试计划(含60+测试用例)
- ✅ CI/CD流水线配置(lint+test+security+build)
- ✅ GitHub Issue模板(Bug/Feature/Document)
- ✅ PR模板与Checklist
- ✅ Python包结构(src/core/src/frontend/tests)
- ✅ pyproject.toml项目元数据配置
- ✅ .gitignore标准化忽略规则

### 技术债务 (Technical Debt)
- [ ] 核心算法代码待迁移(KuiBa → CFD_class标准化重构)
- [ ] Streamlit UI页面待实现
- [ ] 单元测试用例待编写(目标覆盖率≥80%)
- [ ] 示例案例库待建立

### 已知限制 (Known Limitations)
- 当前仅为框架阶段，无实际可运行功能
- 文档为框架版，需后续补充详细内容
- CI/CD尚未经过实际push验证

---

## 版本号说明

本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0/) 规范：

| 格式 | 说明 | 示例 |
|------|------|------|
| `vMAJOR.MINOR.PATCH` | 正式发布版 | `v1.0.0` |
| `vMAJOR.MINOR.PATCH-alpha` | 内部测试版 | `v0.1.0-alpha` |
| `vMAJOR.MINOR.PATCH-beta` | 公开测试版 | `v1.0.0-beta` |
| `vMAJOR.MINOR.PATCH-rc.N` | 候选发布版 | `v1.0.0-rc.1` |

### 各阶段触发条件

- **alpha**: 功能未完成，内部测试
- **beta**: 功能基本完成，外部测试
- **rc**: 发布候选，仅修复bug
- **正式版**: 经过充分验证，可交付用户

---

*维护者: @PM (@TW协助)*
