# CFD-Class 代码推送指南

## 当前状态

✅ Git 已安装 (2.43.0.windows.1)
✅ GitHub CLI 已安装 (2.43.1)
✅ 代码已提交 (Commit: 7a91b8d)
✅ 分支已创建 (feature/015-streamlit-main-app)

## 推送步骤

### 1. 登录 GitHub

在终端中运行：

```bash
gh auth login
```

选择：
- **GitHub.com**
- **HTTPS** 协议
- 使用 **网页浏览器** 登录（推荐）

或者使用 Token 登录：

```bash
# 如果你有 GitHub Personal Access Token
echo "YOUR_TOKEN" | gh auth login --with-token
```

### 2. 验证登录

```bash
gh auth status
```

### 3. 推送代码

```bash
# 确保在正确的分支
git branch

# 推送分支到 GitHub
git push -u origin feature/015-streamlit-main-app
```

### 4. 创建 Pull Request

```bash
# 使用 GitHub CLI 创建 PR
gh pr create \
  --title "feat(ui): create Streamlit main application entry point (#15)" \
  --body "This PR implements the main Streamlit application entry point as described in Issue #15.

## 变更内容
- Add main app.py with multi-page structure
- Add Simulation page with parameter configuration
- Add Comparison page for scheme analysis
- Add Theory page for educational content
- Implement reusable UI components
- Add business logic engines
- Add Git tools installation script
- Configure CI/CD pipeline

## 测试计划
- [ ] 单元测试：UI组件测试
- [ ] 集成测试：页面交互测试
- [ ] 手动测试：Streamlit应用运行测试

## 相关Issue
Closes #15" \
  --base develop \
  --head feature/015-streamlit-main-app
```

或者使用网页界面创建 PR：

```bash
# 在浏览器中打开 PR 创建页面
gh pr create --web
```

### 5. 验证 PR

```bash
# 查看 PR 列表
gh pr list

# 查看 PR 详情
gh pr view 15
```

## 文件清单

已提交的 18 个文件：

```
✅ .github/workflows/ci.yml
✅ scripts/install-git-tools-simple.ps1
✅ scripts/install-git-tools.ps1
✅ src/frontend/__init__.py
✅ src/frontend/app.py
✅ src/frontend/components/__init__.py
✅ src/frontend/components/navigation.py
✅ src/frontend/components/parameter_panel.py
✅ src/frontend/components/plot_display.py
✅ src/frontend/components/scheme_selector.py
✅ src/frontend/engines/__init__.py
✅ src/frontend/engines/comparison_engine.py
✅ src/frontend/engines/report_engine.py
✅ src/frontend/engines/simulation_engine.py
✅ src/frontend/pages/1_Simulation.py
✅ src/frontend/pages/2_Comparison.py
✅ src/frontend/pages/3_Theory.py
✅ src/frontend/pages/__init__.py
```

## 提交信息

```
feat(ui): create Streamlit main application entry point

- Add main app.py with multi-page structure
- Add Simulation page with parameter configuration
- Add Comparison page for scheme analysis
- Add Theory page for educational content
- Implement reusable UI components
- Add business logic engines
- Add Git tools installation script
- Configure CI/CD pipeline

Closes #15
```

## 常见问题

### Q: 推送时提示 "Permission denied"
A: 确保已登录 GitHub 并有仓库写入权限

### Q: 推送时提示 "rejected"
A: 先拉取最新代码：
```bash
git pull origin develop
```

### Q: 如何查看提交历史
A: 
```bash
git log --oneline
```

### Q: 如何撤销提交
A:
```bash
# 撤销最后一次提交，保留更改
git reset --soft HEAD~1

# 撤销最后一次提交，丢弃更改
git reset --hard HEAD~1
```

## 下一步

1. 登录 GitHub (`gh auth login`)
2. 推送代码 (`git push -u origin feature/015-streamlit-main-app`)
3. 创建 PR (`gh pr create`)
4. 等待代码审查
5. 合并 PR

---

**生成时间**: 2026-05-09
**作者**: CFD-Team FE
