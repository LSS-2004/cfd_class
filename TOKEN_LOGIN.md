# 使用 Personal Access Token 登录 GitHub

## 方法一：生成 Token 并登录

### 步骤 1：生成 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 输入 Token 名称：`CFD-Class-Development`
4. 选择过期时间：**30 days** 或 **No expiration**
5. 勾选以下权限：
   - ✅ `repo` (完整仓库访问)
   - ✅ `workflow` (GitHub Actions)
   - ✅ `read:org` (读取组织信息)

6. 点击 **"Generate token"**
7. **立即复制 Token**（页面关闭后无法再次查看）

### 步骤 2：使用 Token 登录

在终端中运行：

```bash
echo "YOUR_TOKEN_HERE" | gh auth login --with-token
```

将 `YOUR_TOKEN_HERE` 替换为你复制的 Token。

### 步骤 3：验证登录

```bash
gh auth status
```

## 方法二：直接在 Git 中使用 Token

### 步骤 1：配置 Git 凭据

```bash
git config --global credential.helper manager
```

### 步骤 2：推送代码

```bash
git push -u origin feature/015-streamlit-main-app
```

当提示输入用户名和密码时：
- **用户名**: 你的 GitHub 用户名 (`LSS-2004`)
- **密码**: 使用 Personal Access Token（不是 GitHub 密码）

## 验证推送成功

```bash
# 查看远程分支
git branch -r

# 查看提交历史
git log --oneline

# 查看 PR 列表
gh pr list
```

## 创建 Pull Request

```bash
gh pr create \
  --title "feat(ui): create Streamlit main application entry point (#15)" \
  --body "This PR implements the main Streamlit application entry point as described in Issue #15." \
  --base develop
```

## 常见问题

### Q: Token 过期了怎么办？
A: 重新生成 Token 并登录：
```bash
gh auth logout
echo "NEW_TOKEN" | gh auth login --with-token
```

### Q: 如何查看当前 Token？
A:
```bash
gh auth token
```

### Q: 如何撤销 Token？
A: 访问 https://github.com/settings/tokens 删除对应的 Token

---

**生成时间**: 2026-05-09
**作者**: CFD-Team FE
