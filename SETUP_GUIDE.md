# 🚀 CFD-Class 仓库初始化 - 完整执行指南

> **面向对象**: @PM (项目经理)  
> **目的**: 一键完成仓库基础设施 + Issues发布  
> **预计时间**: 10-15分钟 (含GitHub登录)

---

## ✅ 已完成的准备工作

我已经为你创建了以下自动化脚本和文档:

### 📁 创建的文件

```
cfd_class/
├── scripts/
│   ├── setup_repo.py              ✅ 仓库基础设施设置脚本
│   └── create_issues.py           ✅ 批量创建20个Issues脚本
├── TEAM_WORKFLOW.md               ✅ 团队成员工作流程指南 (已发布!)
└── PM_TASK_PUBLISHING_GUIDE.md    ✅ PM任务发布指南 (已有)
```

---

## 🔧 步骤1: GitHub CLI 认证 (必须先完成!)

### 方法A: 浏览器授权 (推荐)

打开 **PowerShell** 或 **命令提示符**, 运行:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth login --web --git-protocol https
```

**操作流程**:
1. 终端会显示验证码
2. 按 Enter 打开浏览器
3. 在浏览器中输入验证码并授权
4. 授权成功后返回终端

### 验证登录成功

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

应该显示登录成功信息。

---

## ⚡ 步骤2: 一键设置仓库基础设施

```powershell
cd D:\APaper\MyClaudeCode\CFD\cfd_class
python scripts/setup_repo.py
```

脚本会自动完成:
- ✅ main分支保护规则 (需2人审核+CI)
- ✅ develop分支保护规则 (需1人审核)
- ✅ 17个标签体系
- ✅ Sprint 1 Milestone
- ✅ Projects看板

---

## 📋 步骤3: 批量创建20个任务Issues

```powershell
python scripts/create_issues.py
```

将自动创建:
- A1-A4: 基础设施 (@PM)
- B1-B10: 核心引擎 (@BE)
- C1-C4: 前端UI (@FE)
- D1-D3: 测试框架 (@QA)
- E1-E3: 文档 (@TW)

---

## 🎉 步骤4: 验证并通知团队

访问以下链接确认设置成功:
- Issues: https://github.com/kaklos-cyber/cfd_class/issues
- Projects: https://github.com/kaklos-cyber/cfd_class/projects
- Labels: https://github.com/kaklos-cyber/cfd_class/labels

然后推送文档并通知团队开始工作!

---

## 📞 需要帮助?

如果遇到问题, 请检查:
1. GitHub CLI 是否已认证 (`gh auth status`)
2. Python 版本是否 ≥ 3.9
3. 是否有仓库写权限

详细问题排查请查看 TEAM_WORKFLOW.md 的 FAQ 章节。