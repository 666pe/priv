@echo off
chcp 65001 >nul
title Compilando 6p priv...

echo ========================================
echo  6p priv - Build para .exe
echo ========================================
echo.

python --version 2>nul || (
    echo ERRO: Python nao encontrado no PATH
    echo Instale Python 3.8+ de python.org
    pause
    exit /b 1
)

echo Verificando dependencias...
pip show pyinstaller >nul 2>&1 || (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Compilando...
echo.

python build.py

echo.
if exist "dist\6p_priv.exe" (
    echo ========================================
    echo  SUCESSO! Executavel criado em:
    echo  dist\6p_priv.exe
    echo ========================================
) else (
    echo ========================================
    echo  ERRO: Executavel nao foi gerado
    echo  Verifique mensagens acima
    echo ========================================
)

pause