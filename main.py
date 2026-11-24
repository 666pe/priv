#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6p priv - Ferramenta de Otimização do Windows
Senha de acesso: clientpriv
Compilável com: pyinstaller --onefile --windowed --icon=icon.ico main.py
"""

import sys
import os
import ctypes
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Adiciona o diretório do script ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from login import LoginWindow
from optimizer import SystemOptimizer
from gui import MainWindow


def is_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """Reexecuta o script como administrador."""
    if is_admin():
        return True

    # Reexecuta com elevação
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        return False  # Processo atual deve sair
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível elevar privilégios:\n{e}")
        return False


def main():
    # Verifica privilégios de administrador
    if not is_admin():
        if not run_as_admin():
            sys.exit(0)
        return  # O processo elevado continuará

    # Inicia a aplicação
    root = tk.Tk()
    root.withdraw()  # Esconde janela principal até login

    # Tela de login
    login = LoginWindow(root, password="clientpriv", on_success=lambda: start_app(root))
    root.mainloop()


def start_app(root):
    """Inicia a janela principal após login bem-sucedido."""
    root.deiconify()
    root.title("6p priv - Otimizador do Sistema")
    root.geometry("900x650")
    root.minsize(800, 600)

    # Centraliza na tela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (900 // 2)
    y = (root.winfo_screenheight() // 2) - (650 // 2)
    root.geometry(f"900x650+{x}+{y}")

    # Tema e estilo
    style = ttk.Style()
    style.theme_use('clam')

    # Cores personalizadas
    style.configure('TFrame', background='#1e1e2e')
    style.configure('TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 10))
    style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#89b4fa')
    style.configure('TButton', font=('Segoe UI', 10), padding=8)
    style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
    style.configure('TNotebook', background='#1e1e2e', borderwidth=0)
    style.configure('TNotebook.Tab', font=('Segoe UI', 10), padding=[20, 10])
    style.map('TNotebook.Tab',
              background=[('selected', '#313244'), ('!selected', '#1e1e2e')],
              foreground=[('selected', '#89b4fa'), ('!selected', '#a6adc8')])
    style.configure('TLabelframe', background='#1e1e2e', borderwidth=1, relief='solid')
    style.configure('TLabelframe.Label', background='#1e1e2e', foreground='#89b4fa', font=('Segoe UI', 10, 'bold'))
    style.configure('TEntry', fieldbackground='#313244', foreground='#cdd6f4')
    style.configure('TCheckbutton', background='#1e1e2e', foreground='#cdd6f4')
    style.configure('Horizontal.TProgressbar', troughcolor='#313244', background='#89b4fa')

    root.configure(bg='#1e1e2e')

    # Inicializa otimizador e janela principal
    optimizer = SystemOptimizer()
    app = MainWindow(root, optimizer)

    # Protocolo de fechamento
    root.protocol("WM_DELETE_WINDOW", app.on_close)


if __name__ == "__main__":
    main()