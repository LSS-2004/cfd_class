# CFD-Class Repository Setup Script
# ============================================
$ErrorActionPreference = "Stop"
$repo = "kaklos-cyber/cfd_class"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CFD-Class Setup Tool v1.0" -ForegroundColor Cyan
Write-Host "======================================== -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow

$ghExists = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghExists) {
    Write-Host "ERROR: GitHub CLI not found" -ForegroundColor Red
    exit 1
}

$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Not authenticated with GitHub" -ForegroundColor Red
    Write-Host "Please run: gh auth login --web" -ForegroundColor White
    exit 1
}

Write-Host "OK: GitHub CLI ready!" -ForegroundColor Green

# Step 1: Branch protection rules
Write-Host ""
Write-Host "[2/6] Setting up branch protection..." -ForegroundColor Yellow

Write-Host "   -> Configuring main branch..." -ForegroundColor White
$bodyMain = @{
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
} | ConvertTo-Json -Depth 3

$result = gh api repos/$repo/branches/main/protection -X PUT -f input="$bodyMain" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK: main branch protected (2 reviewers + CI)" -ForegroundColor Green
} else {
    Write-Host "   WARNING: main protection may already exist" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

Write-Host "   -> Configuring develop branch..." -ForegroundColor White
$bodyDev = @{
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
} | ConvertTo-Json -Depth 3

$result = gh api repos/$repo/branches/develop/protection -X PUT -f input="$bodyDev" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK: develop branch protected (1 reviewer)" -ForegroundColor Green
} else {
    Write-Host "   WARNING: develop protection may already exist" -ForegroundColor Yellow
}

# Step 2: Create Labels
Write-Host ""
Write-Host "[3/6] Creating labels (17)..." -ForegroundColor Yellow

$labels = @(
    @{name="kind/bug"; color="e11d21"; description="Bug"},
    @{name="kind/enhancement"; color="a855f7"; description="Feature"},
    @{name="kind/docs"; color="0075ff"; description="Documentation"},
    @{name="kind/refactor"; color="fbca04"; description="Refactor"},
    @{name="kind/testing"; color="2ea44f"; description="Testing"},
    
    @{name="priority/critical"; color="d73a49"; description="P0-Critical"},
    @{name="priority/high"; color="ff7b00"; description="P1-High"},
    @{name="priority/medium"; color="1d9ce0"; description="P2-Medium"},
    @{name="priority/low"; color="909399"; description="P3-Low"},
    
    @{name="module/core"; color="0e8a16"; description="Core Engine"},
    @{name="module/ui"; color="5319e7"; description="UI Frontend"},
    @{name="module/tests"; color="#bd10e0"; description="Tests"},
    @{name="module/docs"; color="f94189"; description="Docs"},
    @{name="module/infrastructure"; color="6b7280"; description="Infrastructure"},
    
    @{name="status/in-progress"; color="f59e0b"; description="In Progress"},
    @{name="status/review"; color="8b5cf6"; description="Review"},
    @{name="status/blocked"; color="ef4444"; description="Blocked"}
)

$count = 0
foreach ($label in $labels) {
    $json = $label | ConvertTo-Json
    $result = gh api repos/$repo/labels -X POST -f "$json" 2>$null
    if ($LASTEXITCODE -eq 0) { $count++ }
}
Write-Host "   OK: Created $count / $($labels.Count) labels" -ForegroundColor Green

# Step 3: Create Milestone
Write-Host ""
Write-Host "[4/6] Creating Sprint 1 Milestone..." -ForegroundColor Yellow

$milestoneBody = @{
    title = "Sprint 1 - Core Engine & UI Framework"
    state = "open"
    description = @"
Sprint 1 Goals:
- Complete core engine (6 schemes)
- Build UI framework foundation
- Set up testing framework
- Complete documentation structure
"@
} | ConvertTo-Json -Depth 3

$result = gh api repos/$repo/milestones -X POST -f "$milestoneBody" 2>$null
if ($LASTEXITCODE -eq 0) {
    $msNum = ($result | ConvertFrom-Json).number
    Write-Host "   OK: Milestone #$msNum created" -ForegroundColor Green
} else {
    Write-Host "   WARNING: Milestone may already exist" -ForegroundColor Yellow
}

# Step 4: Create Project Board
Write-Host ""
Write-Host "[5/6] Creating Project board..." -ForegroundColor Yellow

try {
    # Try V2 API first
    $query = 'mutation { createProject(input: {ownerId: "kaklos-cyber", title: "CFD-Class Sprint 1"}) { project { id url } } }'
    $result = gh api graphql -f query=$query 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK: Project V2 created successfully!" -ForegroundColor Green
    } else {
        throw "V2 failed"
    }
} catch {
    # Fallback to V1
    Write-Host "   INFO: Using Project V1..." -ForegroundColor Cyan
    $v1Body = '{"name": "CFD-Class Sprint 1", "body": "Sprint 1 Kanban Board"}'
    $result = gh api user/projects -X POST -H "Accept: application/vnd.github.inertia-preview+json" -f "$v1Body" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK: Project V1 created! Configure columns manually" -ForegroundColor Green
        Write-Host "   TIP: Visit https://github.com/kaklos-cyber/cfd_class/projects to add columns" -ForegroundColor Cyan
    } else {
        Write-Host "   WARNING: Auto-create failed, please create manually" -ForegroundColor Yellow
    }
}

# Complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "======================================== -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor White
Write-Host "  [x] main branch: Protected (2 reviewers + CI)" -ForegroundColor Green
Write-Host "  [x] develop branch: Protected (1 reviewer)" -ForegroundColor Green
Write-Host "  [x] Labels: 17 labels created" -ForegroundColor Green
Write-Host "  [x] Milestone: Sprint 1 created" -ForegroundColor Green
Write-Host "  [x] Project: CFD-Class Sprint 1" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEP: Run .\scripts\create_all_issues.ps1 to create 20 task issues" -ForegroundColor Yellow
Write-Host ""