#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build para compilar 6p priv em .exe
Uso: python build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def main():
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    build_dir = project_dir / "build"

    # Limpa builds anteriores
    for d in [dist_dir, build_dir]:
        if d.exists():
            print(f"Limpando {d}...")
            shutil.rmtree(d, ignore_errors=True)

    # Verifica se pyinstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--windowed",                   # Sem console (GUI)
        "--name=6p_priv",              # Nome do executável
        "--icon=icon.ico",             # Ícone (se existir)
        "--add-data=README.md;.",      # Inclui README
        "--clean",                      # Limpa cache
        "--noconfirm",                  # Sobrescreve sem perguntar
        "main.py"
    ]

    # Remove --icon se não existir
    icon_path = project_dir / "icon.ico"
    if not icon_path.exists():
        cmd = [c for c in cmd if not c.startswith("--icon")]
        print("⚠ Ícone não encontrado (icon.ico), compilando sem ícone personalizado")

    print("=" * 60)
    print("Compilando 6p priv...")
    print("=" * 60)

    try:
        result = subprocess.run(cmd, cwd=project_dir, check=True)
        print("\n" + "=" * 60)
        print("✓ Build concluído com sucesso!")
        print(f"Executável em: {dist_dir / '6p_priv.exe'}")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Erro na compilação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()