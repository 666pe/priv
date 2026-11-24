#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela de Login - 6p priv
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time


class LoginWindow:
    """Janela de login com senha."""

    def __init__(self, parent, password, on_success):
        self.parent = parent
        self.password = password
        self.on_success = on_success
        self.attempts = 0
        self.max_attempts = 3
        self.locked = False
        self.lock_until = 0

        self.create_widgets()
        self.center_window()
        self.entry_password.focus_set()

        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.verify_password())

    def create_widgets(self):
        """Cria os widgets da tela de login."""
        # Frame principal
        self.frame = tk.Frame(self.parent, bg='#1e1e2e')
        self.frame.pack(expand=True, fill='both')

        # Container central
        container = tk.Frame(self.frame, bg='#313244', bd=0)
        container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=380)

        # Título
        title_frame = tk.Frame(container, bg='#313244')
        title_frame.pack(pady=(40, 10))

        tk.Label(
            title_frame,
            text="6p priv",
            font=('Segoe UI', 28, 'bold'),
            fg='#89b4fa',
            bg='#313244'
        ).pack()

        tk.Label(
            title_frame,
            text="Otimizador do Sistema",
            font=('Segoe UI', 11),
            fg='#a6adc8',
            bg='#313244'
        ).pack()

        # Separador
        sep = tk.Frame(container, height=2, bg='#45475a')
        sep.pack(fill='x', padx=40, pady=20)

        # Campo de senha
        pwd_frame = tk.Frame(container, bg='#313244')
        pwd_frame.pack(pady=10, padx=40, fill='x')

        tk.Label(
            pwd_frame,
            text="Senha de acesso",
            font=('Segoe UI', 10),
            fg='#cdd6f4',
            bg='#313244'
        ).pack(anchor='w', pady=(0, 5))

        self.entry_password = tk.Entry(
            pwd_frame,
            show='●',
            font=('Segoe UI', 12),
            bg='#1e1e2e',
            fg='#cdd6f4',
            insertbackground='#cdd6f4',
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightbackground='#45475a',
            highlightcolor='#89b4fa'
        )
        self.entry_password.pack(fill='x', ipady=8)

        # Label de status/tentativas
        self.lbl_status = tk.Label(
            container,
            text="",
            font=('Segoe UI', 9),
            fg='#f38ba8',
            bg='#313244'
        )
        self.lbl_status.pack(pady=(5, 15))

        # Botão de entrar
        self.btn_login = tk.Button(
            container,
            text="ENTRAR",
            font=('Segoe UI', 11, 'bold'),
            bg='#89b4fa',
            fg='#1e1e2e',
            activebackground='#74c7ec',
            activeforeground='#1e1e2e',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.verify_password
        )
        self.btn_login.pack(pady=10, padx=40, fill='x', ipady=10)

        # Versão
        tk.Label(
            container,
            text="v1.0.0  •  Requer execução como Administrador",
            font=('Segoe UI', 8),
            fg='#6c7086',
            bg='#313244'
        ).pack(side='bottom', pady=20)

        # Efeito hover no botão
        self.btn_login.bind('<Enter>', lambda e: self.btn_login.config(bg='#74c7ec'))
        self.btn_login.bind('<Leave>', lambda e: self.btn_login.config(bg='#89b4fa'))

    def center_window(self):
        """Centraliza a janela na tela."""
        self.parent.update_idletasks()
        w, h = 400, 380
        x = (self.parent.winfo_screenwidth() // 2) - (w // 2)
        y = (self.parent.winfo_screenheight() // 2) - (h // 2)
        self.parent.geometry(f"{w}x{h}+{x}+{y}")

    def verify_password(self):
        """Verifica a senha digitada."""
        if self.locked:
            remaining = int(self.lock_until - time.time())
            if remaining > 0:
                self.lbl_status.config(text=f"Bloqueado. Tente novamente em {remaining}s")
                return
            else:
                self.locked = False
                self.attempts = 0

        entered = self.entry_password.get().strip()

        if entered == self.password:
            # Sucesso - animação rápida
            self.btn_login.config(text="✓ ACESSO CONCEDIDO", bg='#a6e3a1', state='disabled')
            self.parent.after(500, self.on_success)
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts

            if remaining > 0:
                self.lbl_status.config(text=f"Senha incorreta. Tentativas restantes: {remaining}")
                self.shake_window()
                self.entry_password.delete(0, 'end')
            else:
                self.locked = True
                self.lock_until = time.time() + 30  # 30 segundos de bloqueio
                self.lbl_status.config(text="Muitas tentativas. Bloqueado por 30 segundos.")
                self.btn_login.config(state='disabled')
                self.parent.after(30000, self.unlock)

    def unlock(self):
        """Desbloqueia após timeout."""
        self.locked = False
        self.attempts = 0
        self.btn_login.config(state='normal', text="ENTRAR", bg='#89b4fa')
        self.lbl_status.config(text="")

    def shake_window(self):
        """Animação de shake na janela."""
        original_x = self.parent.winfo_x()
        for i in range(6):
            offset = 10 if i % 2 == 0 else -10
            self.parent.geometry(f"+{original_x + offset}+{self.parent.winfo_y()}")
            self.parent.update()
            time.sleep(0.03)
        self.parent.geometry(f"+{original_x}+{self.parent.winfo_y()}")