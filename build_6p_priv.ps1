<#
.SYNOPSIS
    Build automatizado do 6p priv - Compila .exe standalone
.DESCRIPTION
    Instala Python (via winget), dependencias, compila com PyInstaller
    e copia o executavel para a area de trabalho.
.NOTES
    Execute como ADMINISTRADOR (PowerShell > Executar como Administrador)
#>

param(
    [switch]$NoDesktopCopy  # Nao copiar para Desktop
)

$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
$DistDir = Join-Path $ProjectDir "dist"
$ExeName = "6p_priv.exe"
$DesktopPath = [Environment]::GetFolderPath("Desktop")

Write-Host "================================================================"
Write-Host "           6p priv - Build Automatizado v1.0                  "
Write-Host "================================================================"
Write-Host ""

# Verifica Admin
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "AVISO: ESTE SCRIPT PRECISA RODAR COMO ADMINISTRADOR" -ForegroundColor Red
    Write-Host "   Clique com botao direito no PowerShell > 'Executar como Administrador'" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

function Write-Step { param($msg) Write-Host "`n>> $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "   $msg" -ForegroundColor Gray }
function Write-Warn { param($msg) Write-Host "   !! $msg" -ForegroundColor Yellow }
function Write-Done { param($msg) Write-Host "   OK $msg" -ForegroundColor Cyan }

# 1. Verifica/instala Python
Write-Step "Verificando Python..."
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyVer = python --version 2>&1
    Write-Done "Python encontrado: $pyVer"
} else {
    Write-Info "Python nao encontrado. Instalando via winget..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
        refreshenv 2>$null
        if (Get-Command python -ErrorAction SilentlyContinue) {
            Write-Done "Python instalado: $(python --version)"
        } else {
            Write-Host "ERRO: Falha ao instalar Python. Instale manualmente de python.org" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "ERRO: winget nao disponivel. Instale Python 3.8+ de python.org" -ForegroundColor Red
        exit 1
    }
}

# 2. Atualiza pip
Write-Step "Atualizando pip..."
python -m pip install --upgrade pip --quiet
Write-Done "pip atualizado"

# 3. Instala dependencias
Write-Step "Instalando dependencias (psutil, winshell, pyinstaller)..."
python -m pip install psutil winshell pyinstaller --quiet
Write-Done "Dependencias instaladas"

# 4. Limpa builds anteriores
Write-Step "Limpando builds anteriores..."
if (Test-Path $DistDir) { Remove-Item $DistDir -Recurse -Force }
if (Test-Path (Join-Path $ProjectDir "build")) { Remove-Item (Join-Path $ProjectDir "build") -Recurse -Force }
Write-Done "Limpeza concluida"

# 5. Compila
Write-Step "Compilando com PyInstaller (pode demorar 30-60s)..."
cd $ProjectDir
$cmd = @(
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name=6p_priv",
    "--clean",
    "--noconfirm",
    "main.py"
)

# Adiciona icone se existir
$iconPath = Join-Path $ProjectDir "icon.ico"
if (Test-Path $iconPath) { $cmd += "--icon=$iconPath" }

try {
    & $cmd
    Write-Done "Compilacao concluida!"
} catch {
    Write-Host "ERRO na compilacao: $_" -ForegroundColor Red
    exit 1
}

# 6. Verifica resultado
$exePath = Join-Path $DistDir $ExeName
if (Test-Path $exePath) {
    $sizeMB = [math]::Round((Get-Item $exePath).Length / 1MB, 1)
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "  BUILD CONCLUIDO COM SUCESSO!                                " -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "  Executavel: $exePath" -ForegroundColor Green
    Write-Host "  Tamanho: ${sizeMB} MB" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green

    # Copia para Desktop
    if (-not $NoDesktopCopy) {
        $dest = Join-Path $DesktopPath $ExeName
        Copy-Item $exePath $dest -Force
        Write-Done "Copiado para: $dest"
    }

    # Teste rapido
    Write-Host "`nQuer testar o executavel agora? (s/N)" -NoNewline
    $resp = Read-Host
    if ($resp -match '^[sS]') {
        Write-Info "Iniciando 6p_priv.exe (precisa de Admin)..."
        Start-Process $exePath -Verb RunAs
    }
} else {
    Write-Host "ERRO: Executavel nao gerado em $exePath" -ForegroundColor Red
    exit 1
}

Write-Host "`nPressione Enter para sair..."
Read-Host | Out-Null