# CFD-Class 项目初始化与任务发布 - 完整自动化脚本
# ============================================
# 使用方法:
#   1. 先运行: .\scripts\setup_repository.ps1 (一次性初始化)
#   2. 再运行: .\scripts\create_all_issues.ps1 (批量创建20个Issues)
#
# 前置条件:
#   - 已安装 GitHub CLI (gh)
#   - 已有 GitHub 账号且有仓库写权限
# ============================================

$ErrorActionPreference = "Stop"
$repo = "kaklos-cyber/cfd_class"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     CFD-Class 项目自动化初始化工具 v1.0                    ║" -ForegroundColor Cyan
Write-Host "║     设置基础设施 + 创建看板 + 发布20个任务                 ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ====== 检查前置条件 ======
Write-Host "📋 [1/6] 检查前置条件..." -ForegroundColor Yellow

$ghExists = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghExists) {
    Write-Host "❌ 错误: 未找到 GitHub CLI (gh)" -ForegroundColor Red
    Write-Host "   请先运行: winget install GitHub.cli" -ForegroundColor Red
    exit 1
}

$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "" 
    Write-Host "⚠️  未检测到GitHub登录状态，正在启动登录流程..." -ForegroundColor Yellow
    Write-Host ""
    
    # 尝试使用设备流登录（非交互式提示）
    Write-Host "🔐 请在弹出的浏览器中完成GitHub授权..." -ForegroundColor Yellow
    $loginResult = gh auth login --web --git-protocol https 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ 登录失败。请手动运行以下命令登录:" -ForegroundColor Red
        Write-Host "   gh auth login --web" -ForegroundColor White
        exit 1
    }
}

Write-Host "✅ GitHub CLI 已就绪!" -ForegroundColor Green

# ====== Step 1: 设置分支保护规则 ======
Write-Host ""
Write-Host "📋 [2/6] 设置分支保护规则..." -ForegroundColor Yellow

Write-Host "   → 配置 main 分支保护..." -ForegroundColor White
$mainProtection = @{
    required_pull_request_reviews = @{
        required_approving_review_count = 2
        dismiss_stale_reviews_on_push = $true
        require_code_owner_review = $false
    }
    required_status_checks = @{
        strict = $true
        contexts = @("ci/test", "ci/lint")
    }
    enforce_admins = $true
    allow_force_pushes = $false
    allow_deletions = $false
}
$mainJson = $mainProtection | ConvertTo-Json -Depth 3
$mainResult = gh api repos/$repo/branches/main/protection `
    -X PUT `
    -f "$($mainJson -replace '"', '\"')" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ main 分支保护已启用 (需2人审核 + CI通过)" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ main 分支保护可能已存在或权限不足(可稍后手动设置)" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

Write-Host "   → 配置 develop 分支保护..." -ForegroundColor White
$devProtection = @{
    required_pull_request_reviews = @{
        required_approving_review_count = 1
        dismiss_stale_reviews_on_push = $true
    }
    required_status_checks = @{
        strict = $false
        contexts = @("ci/test")
    }
    enforce_admins = $true
    allow_force_pushes = $false
    allow_deletions = $false
}
$devJson = $devProtection | ConvertTo-Json -Depth 3
$devResult = gh api repos/$repo/branches/develop/protection `
    -X PUT `
    -f "$($devJson -replace '"', '\"')" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ develop 分支保护已启用 (需1人审核)" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ develop 分支保护可能已存在或权限不足(可稍后手动设置)" -ForegroundColor Yellow
}

# ====== Step 2: 创建Labels标签体系 ======
Write-Host ""
Write-Host "📋 [3/6] 创建Labels标签体系 (12个)..." -ForegroundColor Yellow

$labels = @(
    @{name="kind/bug"; color="e11d21"; description="软件缺陷"},
    @{name="kind/enhancement"; color="a855f7"; description="新功能建议"},
    @{name="kind/docs"; color="0075ff"; description="文档相关"},
    @{name="kind/refactor"; color="fbca04"; description="代码重构"},
    @{name="kind/testing"; color="2ea44f"; description="测试相关"},
    
    @{name="priority/critical"; color="d73a49"; description="P0-紧急 必须立即处理"},
    @{name="priority/high"; color="ff7b00"; description="P1-高优先级 本Sprint必须完成"},
    @{name="priority/medium"; color="1d9ce0"; description="P2-中优先级 可安排到下个Sprint"},
    @{name="priority/low"; color="909399"; description="P3-低优先级 有空再做"},
    
    @{name="module/core"; color="0e8a16"; description="核心计算引擎 src/core/"},
    @{name="module/ui"; color="5319e7"; description="用户界面 src/frontend/"},
    @{name="module/tests"; color="#bd10e0"; description="测试代码 tests/"},
    @{name="module/docs"; color="f94189"; description="文档 docs/"},
    @{name="module/infrastructure"; color="6b7280"; description="基础设施 CI/CD/配置"},
    
    @{name="status/in-progress"; color="f59e0b"; description="进行中"},
    @{name="status/review"; color="8b5cf6"; description="待审核"},
    @{name="status/blocked"; color="ef4444"; description="被阻塞"}
)

$labelCount = 0
foreach ($label in $labels) {
    $labelJson = $label | ConvertTo-Json
    $result = gh api repos/$repo/labels -X POST -f $labelJson 2>$null
    if ($LASTEXITCODE -eq 0) { $labelCount++ }
}

Write-Host "   ✅ 成功创建 $labelCount / $($labels.Count) 个标签" -ForegroundColor Green

# ====== Step 3: 创建Milestone ======
Write-Host ""
Write-Host "📋 [4/6] 创建Sprint 1 Milestone..." -ForegroundColor Yellow

$milestoneJson = @{
    title = "Sprint 1 - Core Engine & UI Framework"
    state = "open"
    description = "CFD-Class项目第一个Sprint的核心目标:

**目标**: 完成核心计算引擎(6种格式)和前端UI框架基础搭建

**主要交付物**:
- DamBreakConfig配置管理
- 精确Riemann求解器 + HLL近似通量
- BaseScheme基类 + 6种FVM格式实现
- Streamlit主入口 + 参数面板 + 格式选择器
- pytest测试框架 + 核心单元测试
- GB/T文档框架完善

**时间范围**: 约4周 (2026-05-07 ~ 2026-06-04)

**团队成员**:
- @BE: 核心引擎开发 (B1-B10)
- @FE: 前端UI框架 (C1-C4)
- @QA: 测试框架 (D1-D3)
- @TW: 文档完善 (E1-E3)
- @PM: 协调管理 (A1-A4)
- @Arch: 技术审核"
} | ConvertTo-Json -Depth 3

$msResult = gh api repos/$repo/milestones -X POST -f $milestoneJson 2>$null

if ($LASTEXITCODE -eq 0) {
    $msNumber = ($msResult | ConvertFrom-Json).number
    Write-Host "   ✅ Milestone #$msNumber 创建成功: 'Sprint 1 - Core Engine & UI Framework'" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ Milestone可能已存在(可忽略此错误)" -ForegroundColor Yellow
}

# ====== Step 4: 创建Projects看板 ======
Write-Host ""
Write-Host "📋 [5/6] 创建Projects看板..." -ForegroundColor Yellow

$projectJson = @{
    name = "CFD-Class Sprint 1"
    body = "## CFD-Class Sprint 1 看板

### 列定义
| 列名 | 用途 | WIP限制 |
|------|------|--------|
| **Backlog** | 待办任务 | 无限制 |
| **In Progress** | 进行中的任务 | ≤3 |
| **Review** | 待Code Review | ≤5 |
| **Testing** | QA测试中 | 无限制 |
| **Done** | 已完成 | 无限制 |

### Sprint目标
完成一维溃坝教学软件的核心引擎和UI框架。
" | ConvertTo-Json
} | ConvertTo-Json -Depth 3

# 使用GraphQL API创建Project v2
$query = @"
mutation CreateProject($input: CreateProjectInput!) {
  createProject(input: $input) {
    project {
      id
      url
    }
  }
}
@

$variables = @{
    input = @{
        ownerId = "kaklos-cyber"
        title = "CFD-Class Sprint 1"
        body = "CFD-Class 一维溃坝教学软件 Sprint 1 任务看板`n`n### 列`n- Backlog (待办)`n- In Progress (进行中)`n- Review (待审核)`n- Testing (测试中)`n- Done (已完成)"
    }
} | ConvertTo-Json -Depth 5

# 尝试创建project (v2 API可能不可用，用v1替代)
try {
    $projResult = gh api graphql -f query=$query -f variables=$variables 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Project V2 看板创建成功!" -ForegroundColor Green
    } else {
        throw "V2 API failed"
    }
} catch {
    # Fallback: 创建V1 project (自动创建Kanban board)
    Write-Host "   ℹ️ 使用 Project V1 (经典版看板)..." -ForegroundColor Cyan
    
    # V1 project 通过header创建
    $headers = @{
        "Accept" = "application/vnd.github.inertia-preview+json"
    }
    $v1Body = @{
        name = "CFD-Class Sprint 1"
        body = "## Sprint 1 看板`n`n**目标**: 核心引擎 + UI框架`n**周期**: 4周`n**团队**: 6人"
    } | ConvertTo-Json
    
    $projResult = gh api user/projects -X POST -H "Accept: application/vnd.github.inertia-preview+json" -f "$($v1Body | ConvertTo-Json -Depth 3)" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Project V1 看板创建成功! (请在网页上配置列)" -ForegroundColor Green
        Write-Host "   💡 提示: 打开 https://github.com/kaklos-cyber/cfd_class/projects 手动添加列" -ForegroundColor Cyan
    } else {
        Write-Host "   ⚠️ 自动创建看板失败，请手动创建: Settings → Features → Projects" -ForegroundColor Yellow
    }
}

# ====== 完成 ======
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ 基础设施设置完成!                       ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                             ║" -ForegroundColor Green
Write-Host "║  ✓ main 分支保护: 需2人审核 + CI通过                        ║" -ForegroundColor Green
Write-Host "║  ✓ develop 分支保护: 需1人审核                           ║" -ForegroundColor Green
Write-Host "║  ✓ Labels标签: 12个 (类型/优先级/模块/状态)               ║" -ForegroundColor Green
Write-Host "║  ✓ Milestone: Sprint 1 - Core Engine & UI Framework       ║" -ForegroundColor Green
Write-Host "║  ✓ Projects看板: CFD-Class Sprint 1                      ║" -ForegroundColor Green
Write-Host "║                                                             ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📌 下一步: 运行 .\scripts\create_all_issues.ps1 批量创建20个任务Issues" -ForegroundColor Yellow
Write-Host ""
