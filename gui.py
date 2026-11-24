#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica Principal - 6p priv
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from optimizer import SystemOptimizer, run_in_thread


class MainWindow:
    """Janela principal da aplicação."""

    def __init__(self, root, optimizer: SystemOptimizer):
        self.root = root
        self.optimizer = optimizer
        self.optimizer.log_callback = self.log_message

        # Variáveis de controle
        self.cpu_ram_running = False
        self.registry_running = False
        self.cleanup_running = False

        # Checkbox vars para Registry
        self.registry_vars = {}
        # Checkbox vars para Cleanup
        self.cleanup_vars = {}

        self.create_widgets()
        self.start_system_monitor()

    def create_widgets(self):
        """Cria toda a interface."""
        # Header
        self.create_header()

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Abas
        self.tab_cpu_ram = ttk.Frame(self.notebook)
        self.tab_registry = ttk.Frame(self.notebook)
        self.tab_cleanup = ttk.Frame(self.notebook)
        self.tab_tools = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cpu_ram, text="  🚀  CPU / RAM / GPU  ")
        self.notebook.add(self.tab_registry, text="  📝  Registro  ")
        self.notebook.add(self.tab_cleanup, text="  🗑️  Limpeza  ")
        self.notebook.add(self.tab_tools, text="  🔧  Ferramentas  ")
        self.notebook.add(self.tab_logs, text="  📋  Logs  ")

        self.create_cpu_ram_tab()
        self.create_registry_tab()
        self.create_cleanup_tab()
        self.create_tools_tab()
        self.create_logs_tab()

        # Status bar
        self.create_status_bar()

    def create_header(self):
        """Cria cabeçalho com título e info do sistema."""
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=10)

        # Título
        ttk.Label(
            header,
            text="6p priv",
            style='Header.TLabel'
        ).pack(side='left')

        ttk.Label(
            header,
            text="Otimizador do Sistema Windows",
            font=('Segoe UI', 10),
            foreground='#a6adc8'
        ).pack(side='left', padx=(10, 0))

        # Info do sistema (direita)
        self.sys_info_frame = ttk.Frame(header)
        self.sys_info_frame.pack(side='right')

        self.lbl_cpu = ttk.Label(self.sys_info_frame, text="CPU: --%")
        self.lbl_cpu.pack(side='right', padx=10)

        self.lbl_ram = ttk.Label(self.sys_info_frame, text="RAM: --%")
        self.lbl_ram.pack(side='right', padx=10)

    def create_cpu_ram_tab(self):
        """Cria aba de CPU/RAM/GPU Boost."""
        # Container com scroll
        canvas = tk.Canvas(self.tab_cpu_ram, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_cpu_ram, orient='vertical', command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # === Seção: Plano de Energia ===
        self.create_section(scrollable, "Plano de Energia", [
            ("Ativar 'Alto Desempenho'", self.btn_high_perf, "Define o plano de energia para máximo desempenho"),
        ])

        # === Seção: CPU ===
        self.create_section(scrollable, "Otimizações de CPU", [
            ("Prioridade Alta (Processo Atual)", self.btn_cpu_priority, "Define prioridade HIGH para este processo"),
            ("Afinidade de CPU (Todos exceto Core 0)", self.btn_cpu_affinity, "Reserva Core 0 para o sistema"),
            ("Desativar CPU Parking", self.btn_cpu_parking, "Impede que cores sejam estacionados (requer reinício)"),
        ])

        # === Seção: GPU ===
        self.create_section(scrollable, "Otimizações de GPU", [
            ("Agendamento GPU por Hardware", self.btn_gpu_scheduling, "Windows 10 2004+ (requer reinício)"),
            ("Prioridade GPU Alta", self.btn_gpu_priority, "Prioridade alta para processos gráficos"),
        ])

        # === Seção: Memória ===
        self.create_section(scrollable, "Gerenciamento de Memória", [
            ("Otimizar LargeSystemCache & Paging", self.btn_memory_mgmt, "Melhora cache de arquivos (requer reinício)"),
            ("Limpar Memória Standby (Working Set)", self.btn_clean_standby, "Libera memória em cache não utilizada"),
        ])

        # === Botão TUDO ===
        ttk.Separator(scrollable, orient='horizontal').pack(fill='x', pady=20)

        btn_all = ttk.Button(
            scrollable,
            text="⚡ APLICAR TODAS OTIMIZAÇÕES CPU/RAM/GPU",
            style='Accent.TButton',
            command=self.run_all_cpu_ram
        )
        btn_all.pack(fill='x', pady=10, ipady=12)

        # Progress bar para CPU/RAM
        self.cpu_ram_progress = ttk.Progressbar(scrollable, mode='determinate')
        self.cpu_ram_progress.pack(fill='x', pady=(5, 0))
        self.lbl_cpu_ram_status = ttk.Label(scrollable, text="Pronto", foreground='#a6e3a1')
        self.lbl_cpu_ram_status.pack(anchor='w', pady=(5, 0))

    def create_registry_tab(self):
        """Cria aba de otimizações de Registro."""
        canvas = tk.Canvas(self.tab_registry, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_registry, orient='vertical', command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Checkboxes para cada tweak
        tweaks = list(self.optimizer.REGISTRY_TWEAKS.keys())

        # Select all / deselect all
        btn_frame = ttk.Frame(scrollable)
        btn_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(btn_frame, text="☑ Selecionar Todos", command=lambda: self.toggle_all_registry(True)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="☐ Desselecionar Todos", command=lambda: self.toggle_all_registry(False)).pack(side='left', padx=5)

        for tweak in tweaks:
            var = tk.BooleanVar(value=True)
            self.registry_vars[tweak] = var

            cb = ttk.Checkbutton(scrollable, text=tweak, variable=var)
            cb.pack(anchor='w', pady=3, padx=10)

        # Botão aplicar
        ttk.Separator(scrollable, orient='horizontal').pack(fill='x', pady=15)

        btn_apply = ttk.Button(
            scrollable,
            text="📝 APLICAR OTIMIZAÇÕES DE REGISTRO SELECIONADAS",
            style='Accent.TButton',
            command=self.run_registry_tweaks
        )
        btn_apply.pack(fill='x', pady=10, ipady=12)

        # Progress
        self.registry_progress = ttk.Progressbar(scrollable, mode='determinate')
        self.registry_progress.pack(fill='x', pady=(5, 0))
        self.lbl_registry_status = ttk.Label(scrollable, text="Pronto", foreground='#a6e3a1')
        self.lbl_registry_status.pack(anchor='w', pady=(5, 0))

        # Aviso
        ttk.Label(
            scrollable,
            text="⚠ Algumas alterações requerem reinicialização do Windows.",
            font=('Segoe UI', 9),
            foreground='#f38ba8'
        ).pack(anchor='w', pady=(15, 0))

    def create_cleanup_tab(self):
        """Cria aba de limpeza."""
        canvas = tk.Canvas(self.tab_cleanup, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_cleanup, orient='vertical', command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Checkboxes
        paths = list(self.optimizer.CLEANUP_PATHS.keys())

        btn_frame = ttk.Frame(scrollable)
        btn_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(btn_frame, text="☑ Selecionar Todos", command=lambda: self.toggle_all_cleanup(True)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="☐ Desselecionar Todos", command=lambda: self.toggle_all_cleanup(False)).pack(side='left', padx=5)

        for name in paths:
            var = tk.BooleanVar(value=True)
            self.cleanup_vars[name] = var

            # Tooltip com caminho
            path = self.optimizer.CLEANUP_PATHS[name]
            display = f"{name}  ({path})" if path != "recycle_bin" else name

            cb = ttk.Checkbutton(scrollable, text=display, variable=var)
            cb.pack(anchor='w', pady=3, padx=10)

        # Botão aplicar
        ttk.Separator(scrollable, orient='horizontal').pack(fill='x', pady=15)

        btn_clean = ttk.Button(
            scrollable,
            text="🗑️ EXECUTAR LIMPEZA SELECIONADA",
            style='Accent.TButton',
            command=self.run_cleanup
        )
        btn_clean.pack(fill='x', pady=10, ipady=12)

        # Progress
        self.cleanup_progress = ttk.Progressbar(scrollable, mode='determinate')
        self.cleanup_progress.pack(fill='x', pady=(5, 0))
        self.lbl_cleanup_status = ttk.Label(scrollable, text="Pronto", foreground='#a6e3a1')
        self.lbl_cleanup_status.pack(anchor='w', pady=(5, 0))

    def create_tools_tab(self):
        """Cria aba de ferramentas/atalhos."""
        canvas = tk.Canvas(self.tab_tools, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_tools, orient='vertical', command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Ferramentas organizadas em categorias
        tools = [
            ("Sistema & Segurança", [
                ("🛡️ Abrir Windows Security", self.optimizer.open_windows_security, "Antivírus e proteção nativa do Windows"),
                ("🔧 Verificar Arquivos do Sistema (SFC)", self.optimizer.run_sfc_scannow, "Repara arquivos de sistema corrompidos"),
                ("🔧 Reparar Imagem do Windows (DISM)", self.optimizer.run_dism_restore, "Repara o armazenamento de componentes"),
            ]),
            ("Desempenho & Armazenamento", [
                ("💾 Limpeza de Disco (cleanmgr)", self.optimizer.open_disk_cleanup, "Ferramenta nativa de limpeza"),
                ("📊 Sensor de Armazenamento", self.optimizer.open_storage_sense, "Configura limpeza automática"),
                ("🔧 Otimizar Unidades (Desfragmentar/Trim)", self.optimizer.optimize_drives, "Otimiza HDDs e SSDs"),
            ]),
            ("Rede & Cache", [
                ("🌐 Limpar Cache DNS", self.optimizer.flush_dns_cache, "Resolve problemas de resolução de nomes"),
                ("📋 Limpar Logs de Eventos", self.optimizer.clear_event_logs, "Libera espaço e melhora performance"),
            ]),
            ("Interface", [
                ("📱 Desativar Modo Tablet", self.optimizer.disable_tablet_mode, "Força modo desktop"),
            ]),
        ]

        for category, items in tools:
            # Label da categoria
            lbl = ttk.Label(scrollable, text=category, style='Header.TLabel')
            lbl.pack(anchor='w', pady=(15, 5), padx=10)

            for name, func, desc in items:
                self.create_tool_button(scrollable, name, func, desc)

    def create_logs_tab(self):
        """Cria aba de logs."""
        # Toolbar
        toolbar = ttk.Frame(self.tab_logs)
        toolbar.pack(fill='x', padx=10, pady=10)

        ttk.Button(toolbar, text="🗑️ Limpar Logs", command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(toolbar, text="💾 Salvar Logs", command=self.save_logs).pack(side='left', padx=5)

        # Área de log
        self.log_text = scrolledtext.ScrolledText(
            self.tab_logs,
            bg='#1e1e2e',
            fg='#cdd6f4',
            insertbackground='#cdd6f4',
            font=('Consolas', 9),
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground='#45475a'
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Configura tags de cor
        self.log_text.tag_config('success', foreground='#a6e3a1')
        self.log_text.tag_config('error', foreground='#f38ba8')
        self.log_text.tag_config('info', foreground='#89b4fa')
        self.log_text.tag_config('warning', foreground='#fab387')
        self.log_text.tag_config('timestamp', foreground='#6c7086')

        # Log inicial
        self.log_message("=== 6p priv Iniciado ===")
        self.log_message("Sistema pronto para otimização", 'info')

    def create_section(self, parent, title, buttons):
        """Cria uma seção com título e botões."""
        # Título
        lbl = ttk.Label(parent, text=title, style='Header.TLabel')
        lbl.pack(anchor='w', pady=(15, 5), padx=10)

        for name, cmd, desc in buttons:
            self.create_action_button(parent, name, cmd, desc)

    def create_action_button(self, parent, text, command, description):
        """Cria botão de ação com descrição."""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=3, padx=10)

        btn = ttk.Button(frame, text=text, command=command, width=40)
        btn.pack(side='left')

        lbl = ttk.Label(frame, text=description, foreground='#6c7086', font=('Segoe UI', 9))
        lbl.pack(side='left', padx=10)

    def create_tool_button(self, parent, text, command, description):
        """Cria botão de ferramenta."""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=3, padx=10)

        btn = ttk.Button(frame, text=text, command=lambda: self.run_tool(command, text))
        btn.pack(side='left')

        lbl = ttk.Label(frame, text=description, foreground='#6c7086', font=('Segoe UI', 9))
        lbl.pack(side='left', padx=10)

    def create_status_bar(self):
        """Cria barra de status inferior."""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill='x', side='bottom', padx=10, pady=5)

        self.lbl_status = ttk.Label(self.status_bar, text="Pronto", foreground='#a6e3a1')
        self.lbl_status.pack(side='left')

        ttk.Label(self.status_bar, text="|  6p priv v1.0.0  |  Execute como Administrador  ", foreground='#6c7086').pack(side='right')

    # ==================== CALLBACKS - CPU/RAM ====================

    def btn_high_perf(self):
        self.run_single_optimizer(self.optimizer.set_high_performance_power_plan, "Plano Alto Desempenho")

    def btn_cpu_priority(self):
        self.run_single_optimizer(lambda: self.optimizer.set_process_priority("HIGH"), "Prioridade CPU")

    def btn_cpu_affinity(self):
        self.run_single_optimizer(self.optimizer.optimize_cpu_affinity, "Afinidade CPU")

    def btn_cpu_parking(self):
        self.run_single_optimizer(self.optimizer.disable_cpu_parking, "CPU Parking")

    def btn_gpu_scheduling(self):
        self.run_single_optimizer(self.optimizer.optimize_gpu_scheduling, "GPU Scheduling")

    def btn_gpu_priority(self):
        self.run_single_optimizer(self.optimizer.set_gpu_priority_high, "Prioridade GPU")

    def btn_memory_mgmt(self):
        self.run_single_optimizer(self.optimizer.optimize_memory_management, "Gerenciamento Memória")

    def btn_clean_standby(self):
        self.run_single_optimizer(self.optimizer.clean_standby_memory, "Limpar Standby")

    def run_single_optimizer(self, func, name):
        """Executa uma otimização simples com feedback."""
        def on_finish(result):
            if result is True:
                self.log_message(f"✓ {name} aplicado com sucesso", 'success')
                self.lbl_cpu_ram_status.config(text=f"✓ {name} concluído", foreground='#a6e3a1')
            elif result is False:
                self.log_message(f"✗ {name} falhou", 'error')
                self.lbl_cpu_ram_status.config(text=f"✗ {name} falhou", foreground='#f38ba8')
            else:
                self.log_message(f"⚠ {name}: erro inesperado", 'warning')

        self.lbl_cpu_ram_status.config(text=f"⟳ Aplicando {name}...", foreground='#fab387')
        self.log_message(f"⟳ Iniciando: {name}", 'info')
        run_in_thread(func, on_finish=on_finish)

    def run_all_cpu_ram(self):
        """Executa todas otimizações CPU/RAM."""
        if self.cpu_ram_running:
            return

        self.cpu_ram_running = True
        self.cpu_ram_progress['value'] = 0
        self.lbl_cpu_ram_status.config(text="⟳ Iniciando otimização completa...", foreground='#fab387')

        def on_progress(pct, msg):
            self.root.after(0, lambda: self.cpu_ram_progress.configure(value=pct))
            self.root.after(0, lambda: self.lbl_cpu_ram_status.config(text=msg, foreground='#fab387'))

        def on_finish(result):
            self.cpu_ram_running = False
            if result is True:
                self.lbl_cpu_ram_status.config(text="✓ Todas otimizações aplicadas com sucesso!", foreground='#a6e3a1')
                self.log_message("✓ Otimização completa CPU/RAM/GPU finalizada", 'success')
            else:
                self.lbl_cpu_ram_status.config(text="⚠ Concluído com algumas falhas", foreground='#f38ba8')
                self.log_message("⚠ Otimização completa finalizada com avisos", 'warning')

        run_in_thread(self.optimizer.run_cpu_ram_boost, kwargs={'progress_callback': on_progress}, on_finish=on_finish)

    # ==================== CALLBACKS - REGISTRY ====================

    def toggle_all_registry(self, state: bool):
        for var in self.registry_vars.values():
            var.set(state)

    def run_registry_tweaks(self):
        if self.registry_running:
            return

        selected = [name for name, var in self.registry_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Aviso", "Nenhuma otimização selecionada.")
            return

        if not messagebox.askyesno("Confirmar", f"Aplicar {len(selected)} otimizações de registro?\nAlgumas requerem reinicialização."):
            return

        self.registry_running = True
        self.registry_progress['value'] = 0
        self.lbl_registry_status.config(text="⟳ Aplicando tweaks de registro...", foreground='#fab387')

        def on_progress(pct, msg):
            self.root.after(0, lambda: self.registry_progress.configure(value=pct))
            self.root.after(0, lambda: self.lbl_registry_status.config(text=msg, foreground='#fab387'))

        def on_finish(result):
            self.registry_running = False
            if isinstance(result, tuple):
                success, total = result
                self.lbl_registry_status.config(text=f"✓ {success}/{total} grupos aplicados", foreground='#a6e3a1' if success == total else '#f38ba8')
                self.log_message(f"Registro: {success}/{total} grupos de tweaks aplicados", 'success' if success == total else 'warning')
            else:
                self.lbl_registry_status.config(text="✗ Erro ao aplicar", foreground='#f38ba8')
                self.log_message("✗ Falha ao aplicar tweaks de registro", 'error')

        run_in_thread(self.optimizer.apply_registry_tweaks, args=(selected,), kwargs={'progress_callback': on_progress}, on_finish=on_finish)

    # ==================== CALLBACKS - CLEANUP ====================

    def toggle_all_cleanup(self, state: bool):
        for var in self.cleanup_vars.values():
            var.set(state)

    def run_cleanup(self):
        if self.cleanup_running:
            return

        selected = [name for name, var in self.cleanup_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Aviso", "Nenhum local selecionado para limpeza.")
            return

        self.cleanup_running = True
        self.cleanup_progress['value'] = 0
        self.lbl_cleanup_status.config(text="⟳ Iniciando limpeza...", foreground='#fab387')

        def on_progress(pct, msg):
            self.root.after(0, lambda: self.cleanup_progress.configure(value=pct))
            self.root.after(0, lambda: self.lbl_cleanup_status.config(text=msg, foreground='#fab387'))

        def on_finish(result):
            self.cleanup_running = False
            if isinstance(result, tuple):
                files, mb = result
                self.lbl_cleanup_status.config(text=f"✓ {files} arquivos, {mb} MB liberados", foreground='#a6e3a1')
                self.log_message(f"Limpeza concluída: {files} arquivos removidos, {mb} MB liberados", 'success')
            else:
                self.lbl_cleanup_status.config(text="✗ Erro na limpeza", foreground='#f38ba8')
                self.log_message("✗ Falha durante limpeza", 'error')

        run_in_thread(self.optimizer.run_cleanup, args=(selected,), kwargs={'progress_callback': on_progress}, on_finish=on_finish)

    # ==================== CALLBACKS - TOOLS ====================

    def run_tool(self, func, name):
        """Executa ferramenta simples."""
        self.log_message(f"⟳ Executando: {name}", 'info')

        def on_finish(result):
            if result is True:
                self.log_message(f"✓ {name} executado", 'success')
            else:
                self.log_message(f"✗ {name} falhou", 'error')

        run_in_thread(func, on_finish=on_finish)

    # ==================== LOGS ====================

    def log_message(self, message: str, level: str = 'info'):
        """Adiciona mensagem ao log com timestamp e cor."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.root.after(0, lambda: self._append_log(timestamp, message, level))

    def _append_log(self, timestamp, message, level):
        """Append thread-safe ao log."""
        self.log_text.configure(state='normal')
        self.log_text.insert('end', f"[{timestamp}] ", 'timestamp')
        self.log_text.insert('end', f"{message}\n", level)
        self.log_text.configure(state='disabled')
        self.log_text.see('end')

    def clear_logs(self):
        """Limpa área de logs."""
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.configure(state='disabled')
        self.log_message("Logs limpos", 'info')

    def save_logs(self):
        """Salva logs em arquivo."""
        try:
            from tkinter import filedialog
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
                title="Salvar logs"
            )
            if path:
                content = self.log_text.get('1.0', 'end')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_message(f"Logs salvos em: {path}", 'success')
        except Exception as e:
            self.log_message(f"Erro ao salvar logs: {e}", 'error')

    # ==================== SYSTEM MONITOR ====================

    def start_system_monitor(self):
        """Inicia monitor de CPU/RAM na header."""
        def update():
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0.1)
                ram = psutil.virtual_memory().percent

                self.lbl_cpu.config(text=f"CPU: {cpu:.0f}%")
                self.lbl_ram.config(text=f"RAM: {ram:.0f}%")

                # Altera cor se alto uso
                cpu_color = '#f38ba8' if cpu > 80 else '#fab387' if cpu > 50 else '#a6e3a1'
                ram_color = '#f38ba8' if ram > 85 else '#fab387' if ram > 65 else '#a6e3a1'

                self.lbl_cpu.config(foreground=cpu_color)
                self.lbl_ram.config(foreground=ram_color)
            except Exception:
                pass

            self.root.after(2000, update)

        update()

    def on_close(self):
        """Fecha a aplicação."""
        if any([self.cpu_ram_running, self.registry_running, self.cleanup_running]):
            if not messagebox.askyesno("Sair", "Otimizações em andamento. Deseja sair mesmo assim?"):
                return
        self.root.destroy()