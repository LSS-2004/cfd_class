# CFD-Class Git 工具安装脚本
# 用于在 Windows 环境中安装 Git 和 GitHub CLI

param(
    [switch]$Force,
    [switch]$SkipGit,
    [switch]$SkipGh,
    [string]$DownloadPath = "$env:TEMP\cfd-class-install"
)

$ErrorActionPreference = "Stop"

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ️  $Message" "Cyan"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" "Red"
}

# 检查管理员权限
function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# 下载文件函数
function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath
    )
    
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($Url, $OutputPath)
        return $true
    }
    catch {
        Write-Error "下载失败: $Url"
        Write-Error $_.Exception.Message
        return $false
    }
}

# 安装 Git
function Install-Git {
    Write-Info "开始安装 Git..."
    
    # 检查是否已安装
    $gitPath = Get-Command git -ErrorAction SilentlyContinue
    if ($gitPath -and -not $Force) {
        Write-Success "Git 已安装: $($gitPath.Source)"
        $version = git --version
        Write-Info "版本: $version"
        return $true
    }
    
    # 创建下载目录
    if (-not (Test-Path $DownloadPath)) {
        New-Item -ItemType Directory -Path $DownloadPath -Force | Out-Null
    }
    
    # Git 下载地址
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$DownloadPath\Git-2.43.0-64-bit.exe"
    
    Write-Info "下载 Git 安装程序..."
    if (-not (Download-File -Url $gitUrl -OutputPath $gitInstaller)) {
        # 使用备用下载地址
        $gitUrl = "https://git-scm.com/download/win"
        Write-Warning "尝试从备用地址下载..."
        Write-Info "请手动访问 $gitUrl 下载并安装 Git"
        return $false
    }
    
    Write-Info "安装 Git..."
    $arguments = "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=""icons,ext\reg\shellhere,assoc,assoc_sh"""
    
    try {
        $process = Start-Process -FilePath $gitInstaller -ArgumentList $arguments -Wait -PassThru
        if ($process.ExitCode -eq 0) {
            Write-Success "Git 安装成功"
            
            # 刷新环境变量
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
            
            # 验证安装
            $version = git --version
            Write-Info "Git 版本: $version"
            return $true
        }
        else {
            Write-Error "Git 安装失败，退出码: $($process.ExitCode)"
            return $false
        }
    }
    catch {
        Write-Error "Git 安装过程出错"
        Write-Error $_.Exception.Message
        return $false
    }
}

# 安装 GitHub CLI
function Install-GitHubCLI {
    Write-Info "开始安装 GitHub CLI (gh)..."
    
    # 检查是否已安装
    $ghPath = Get-Command gh -ErrorAction SilentlyContinue
    if ($ghPath -and -not $Force) {
        Write-Success "GitHub CLI 已安装: $($ghPath.Source)"
        $version = gh --version
        Write-Info "版本: $version"
        return $true
    }
    
    # 创建下载目录
    if (-not (Test-Path $DownloadPath)) {
        New-Item -ItemType Directory -Path $DownloadPath -Force | Out-Null
    }
    
    # GitHub CLI 下载地址
    $ghUrl = "https://github.com/cli/cli/releases/download/v2.43.1/gh_2.43.1_windows_amd64.msi"
    $ghInstaller = "$DownloadPath\gh_2.43.1_windows_amd64.msi"
    
    Write-Info "下载 GitHub CLI 安装程序..."
    if (-not (Download-File -Url $ghUrl -OutputPath $ghInstaller)) {
        Write-Warning "自动下载失败"
        Write-Info "请手动访问 https://github.com/cli/cli/releases 下载并安装 GitHub CLI"
        return $false
    }
    
    Write-Info "安装 GitHub CLI..."
    $arguments = "/i `"$ghInstaller`" /qn /norestart"
    
    try {
        $process = Start-Process -FilePath "msiexec.exe" -ArgumentList $arguments -Wait -PassThru
        if ($process.ExitCode -eq 0) {
            Write-Success "GitHub CLI 安装成功"
            
            # 刷新环境变量
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
            
            # 验证安装
            $version = gh --version
            Write-Info "GitHub CLI 版本: $version"
            return $true
        }
        else {
            Write-Error "GitHub CLI 安装失败，退出码: $($process.ExitCode)"
            return $false
        }
    }
    catch {
        Write-Error "GitHub CLI 安装过程出错"
        Write-Error $_.Exception.Message
        return $false
    }
}

# 配置 Git
function Configure-Git {
    Write-Info "配置 Git..."
    
    # 检查 Git 是否可用
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Error "Git 未安装或不在 PATH 中"
        return $false
    }
    
    # 设置默认配置
    git config --global init.defaultBranch main
    git config --global core.autocrlf true
    git config --global core.safecrlf false
    
    Write-Success "Git 配置完成"
    return $true
}

# 配置 GitHub CLI
function Configure-GitHubCLI {
    Write-Info "配置 GitHub CLI..."
    
    # 检查 gh 是否可用
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Error "GitHub CLI 未安装或不在 PATH 中"
        return $false
    }
    
    # 检查是否已登录
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "GitHub CLI 已登录"
        Write-Info $authStatus
    }
    else {
        Write-Warning "GitHub CLI 未登录"
        Write-Info "请运行 'gh auth login' 进行登录"
    }
    
    return $true
}

# 主函数
function Main {
    Write-ColorOutput "=====================================" "Blue"
    Write-ColorOutput "  CFD-Class Git 工具安装脚本" "Blue"
    Write-ColorOutput "=====================================" "Blue"
    Write-ColorOutput "" 
    
    # 检查管理员权限
    if (-not (Test-Admin)) {
        Write-Warning "脚本未以管理员权限运行"
        Write-Info "某些安装可能需要管理员权限"
        Write-Info "建议右键 PowerShell 选择'以管理员身份运行'"
        Write-ColorOutput ""
    }
    
    # 安装 Git
    $gitSuccess = $true
    if (-not $SkipGit) {
        $gitSuccess = Install-Git
    }
    else {
        Write-Info "跳过 Git 安装"
    }
    
    Write-ColorOutput ""
    
    # 安装 GitHub CLI
    $ghSuccess = $true
    if (-not $SkipGh) {
        $ghSuccess = Install-GitHubCLI
    }
    else {
        Write-Info "跳过 GitHub CLI 安装"
    }
    
    Write-ColorOutput ""
    
    # 配置
    if ($gitSuccess) {
        Configure-Git
    }
    
    if ($ghSuccess) {
        Configure-GitHubCLI
    }
    
    Write-ColorOutput ""
    Write-ColorOutput "=====================================" "Blue"
    Write-ColorOutput "  安装完成！" "Blue"
    Write-ColorOutput "=====================================" "Blue"
    Write-ColorOutput ""
    
    if ($gitSuccess) {
        Write-Success "Git 安装成功"
    }
    else {
        Write-Error "Git 安装失败，请手动安装"
    }
    
    if ($ghSuccess) {
        Write-Success "GitHub CLI 安装成功"
    }
    else {
        Write-Error "GitHub CLI 安装失败，请手动安装"
    }
    
    Write-ColorOutput ""
    Write-Info "下一步操作:"
    Write-Info "1. 重启终端或 PowerShell"
    Write-Info "2. 运行 'git --version' 验证 Git"
    Write-Info "3. 运行 'gh --version' 验证 GitHub CLI"
    Write-Info "4. 运行 'gh auth login' 登录 GitHub"
    Write-ColorOutput ""
}

# 执行主函数
Main
