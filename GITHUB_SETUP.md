# GitHub 认证和推送指南

## 当前状态

❌ GitHub 未登录
❌ 代码未推送
✅ 本地代码已提交

## 解决方案

### 方法一：使用 GitHub CLI 登录（推荐）

1. **运行登录命令**:
```bash
gh auth login
```

2. **选择选项**:
   - ? What account do you want to log into? **GitHub.com**
   - ? What is your preferred protocol for Git operations? **HTTPS**
   - ? Authenticate Git with your GitHub credentials? **Yes**
   - ? How would you like to authenticate GitHub CLI? **Login with a web browser**

3. **复制验证码**，在浏览器中打开提示的 URL，粘贴验证码

4. **授权 CFD-Class 仓库访问**

5. **验证登录**:
```bash
gh auth status
```

6. **推送代码**:
```bash
git push -u origin feature/015-streamlit-main-app
```

7. **创建 PR**:
```bash
gh pr create --title "feat(ui): create Streamlit main application entry point (#15)" --body "This PR implements the main Streamlit application entry point as described in Issue #15."
```

### 方法二：使用 Personal Access Token

1. **生成 Token**:
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 选择权限: `repo`, `workflow`, `read:org`
   - 生成并复制 Token

2. **使用 Token 登录**:
```bash
echo "YOUR_TOKEN" | gh auth login --with-token
```

3. **推送代码**:
```bash
git push -u origin feature/015-streamlit-main-app
```

### 方法三：使用 Git 凭据管理器

1. **配置 Git 凭据**:
```bash
git config --global credential.helper manager
```

2. **推送时会提示输入用户名和密码**:
   - 用户名: 你的 GitHub 用户名
   - 密码: 使用 Personal Access Token

3. **推送代码**:
```bash
git push -u origin feature/015-streamlit-main-app
```

## 验证推送

```bash
# 查看远程分支
git branch -r

# 查看提交历史
git log --oneline

# 查看 PR 列表
gh pr list
```

## 常见问题

### Q: 提示 "Permission denied"
A: 确保你有仓库的写入权限，或者 Fork 仓库后推送

### Q: 提示 "403 Forbidden"
A: 需要登录 GitHub 或检查 Token 权限

### Q: 如何检查当前用户
A:
```bash
gh api user --jq '.login'
```

## 下一步

1. 选择上述方法之一登录 GitHub
2. 推送代码到远程仓库
3. 创建 Pull Request
4. 等待代码审查

---

**生成时间**: 2026-05-09
**作者**: CFD-Team FE
