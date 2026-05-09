# Fork 仓库并推送代码

## 问题
你没有 `kaklos-cyber/cfd_class` 仓库的直接写入权限。

## 解决方案：Fork 仓库

### 步骤 1：Fork 仓库

1. 访问 https://github.com/kaklos-cyber/cfd_class
2. 点击右上角的 **"Fork"** 按钮
3. 选择你的账户 (`LSS-2004`)
4. 等待 Fork 完成

### 步骤 2：更新远程仓库地址

Fork 完成后，在终端中运行：

```bash
# 查看当前远程仓库
git remote -v

# 更新远程仓库为你的 Fork
git remote set-url origin https://github.com/LSS-2004/cfd_class.git

# 验证更新
git remote -v
```

### 步骤 3：推送代码

```bash
git push -u origin feature/015-streamlit-main-app
```

### 步骤 4：创建 Pull Request

1. 访问你的 Fork 仓库：`https://github.com/LSS-2004/cfd_class`
2. 点击 **"Pull requests"** 标签
3. 点击 **"New pull request"** 按钮
4. 点击 **"compare across forks"** 链接
5. 设置：
   - **base repository**: `kaklos-cyber/cfd_class`
   - **base**: `develop`
   - **head repository**: `LSS-2004/cfd_class`
   - **compare**: `feature/015-streamlit-main-app`
6. 填写 PR 标题和描述
7. 点击 **"Create pull request"**

## PR 标题和描述模板

**标题**:
```
feat(ui): create Streamlit main application entry point (#15)
```

**描述**:
```markdown
This PR implements the main Streamlit application entry point as described in Issue #15.

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
Closes #15
```

## 验证推送成功

```bash
# 查看远程分支
git branch -r

# 查看提交历史
git log --oneline
```

## 后续步骤

1. 等待代码审查
2. 根据反馈修改代码
3. 审查通过后，由 @PM 或 @Arch 合并 PR

---

**生成时间**: 2026-05-09
**作者**: CFD-Team FE
