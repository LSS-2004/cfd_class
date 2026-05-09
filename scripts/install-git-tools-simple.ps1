# CFD-Class Git 工具安装脚本 (简化版)
# 用于在 Windows 环境中安装 Git 和 GitHub CLI

Write-Host "=====================================" -ForegroundColor Blue
Write-Host "  CFD-Class Git 工具安装脚本" -ForegroundColor Blue
Write-Host "=====================================" -ForegroundColor Blue
Write-Host ""

# 检查管理员权限
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  脚本未以管理员权限运行" -ForegroundColor Yellow
    Write-Host "ℹ️  某些安装可能需要管理员权限" -ForegroundColor Cyan
    Write-Host "ℹ️  建议右键 PowerShell 选择'以管理员身份运行'" -ForegroundColor Cyan
    Write-Host ""
}

# 创建下载目录
$DownloadPath = "$env:TEMP\cfd-class-install"
if (-not (Test-Path $DownloadPath)) {
    New-Item -ItemType Directory -Path $DownloadPath -Force | Out-Null
}

# 安装 Git
Write-Host "ℹ️  检查 Git 安装状态..." -ForegroundColor Cyan
$gitPath = Get-Command git -ErrorAction SilentlyContinue

if ($gitPath) {
    Write-Host "✅ Git 已安装: $($gitPath.Source)" -ForegroundColor Green
    $version = git --version
    Write-Host "ℹ️  版本: $version" -ForegroundColor Cyan
} else {
    Write-Host "ℹ️  开始安装 Git..." -ForegroundColor Cyan
    
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$DownloadPath\Git-2.43.0-64-bit.exe"
    
    Write-Host "ℹ️  下载 Git 安装程序..." -ForegroundColor Cyan
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($gitUrl, $gitInstaller)
        
        Write-Host "ℹ️  安装 Git..." -ForegroundColor Cyan
        $arguments = "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS"
        $process = Start-Process -FilePath $gitInstaller -ArgumentList $arguments -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✅ Git 安装成功" -ForegroundColor Green
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        } else {
            Write-Host "❌ Git 安装失败，退出码: $($process.ExitCode)" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Git 安装失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "ℹ️  请手动访问 https://git-scm.com/download/win 下载并安装 Git" -ForegroundColor Cyan
    }
}

Write-Host ""

# 安装 GitHub CLI
Write-Host "ℹ️  检查 GitHub CLI 安装状态..." -ForegroundColor Cyan
$ghPath = Get-Command gh -ErrorAction SilentlyContinue

if ($ghPath) {
    Write-Host "✅ GitHub CLI 已安装: $($ghPath.Source)" -ForegroundColor Green
    $version = gh --version
    Write-Host "ℹ️  版本: $version" -ForegroundColor Cyan
} else {
    Write-Host "ℹ️  开始安装 GitHub CLI..." -ForegroundColor Cyan
    
    $ghUrl = "https://github.com/cli/cli/releases/download/v2.43.1/gh_2.43.1_windows_amd64.msi"
    $ghInstaller = "$DownloadPath\gh_2.43.1_windows_amd64.msi"
    
    Write-Host "ℹ️  下载 GitHub CLI 安装程序..." -ForegroundColor Cyan
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($ghUrl, $ghInstaller)
        
        Write-Host "ℹ️  安装 GitHub CLI..." -ForegroundColor Cyan
        $arguments = "/i `"$ghInstaller`" /qn /norestart"
        $process = Start-Process -FilePath "msiexec.exe" -ArgumentList $arguments -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✅ GitHub CLI 安装成功" -ForegroundColor Green
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        } else {
            Write-Host "❌ GitHub CLI 安装失败，退出码: $($process.ExitCode)" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ GitHub CLI 安装失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "ℹ️  请手动访问 https://github.com/cli/cli/releases 下载并安装 GitHub CLI" -ForegroundColor Cyan
    }
}

Write-Host ""

# 配置 Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "ℹ️  配置 Git..." -ForegroundColor Cyan
    git config --global init.defaultBranch main
    git config --global core.autocrlf true
    git config --global core.safecrlf false
    Write-Host "✅ Git 配置完成" -ForegroundColor Green
}

# 配置 GitHub CLI
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "ℹ️  配置 GitHub CLI..." -ForegroundColor Cyan
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ GitHub CLI 已登录" -ForegroundColor Green
    } else {
        Write-Host "⚠️  GitHub CLI 未登录" -ForegroundColor Yellow
        Write-Host "ℹ️  请运行 'gh auth login' 进行登录" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Blue
Write-Host "  安装完成！" -ForegroundColor Blue
Write-Host "=====================================" -ForegroundColor Blue
Write-Host ""
Write-Host "ℹ️  下一步操作:" -ForegroundColor Cyan
Write-Host "ℹ️  1. 重启终端或 PowerShell" -ForegroundColor Cyan
Write-Host "ℹ️  2. 运行 'git --version' 验证 Git" -ForegroundColor Cyan
Write-Host "ℹ️  3. 运行 'gh --version' 验证 GitHub CLI" -ForegroundColor Cyan
Write-Host "ℹ️  4. 运行 'gh auth login' 登录 GitHub" -ForegroundColor Cyan
Write-Host ""
