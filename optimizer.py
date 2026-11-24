#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Otimização do Sistema - 6p priv
Contém todas as funções de otimização: CPU, RAM, Registro, Limpeza, etc.
"""

import os
import sys
import subprocess
import winreg
import ctypes
import psutil
import threading
import time
from pathlib import Path
from typing import List, Tuple, Callable, Optional


class SystemOptimizer:
    """Classe principal para otimizações do sistema."""

    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        self.log_callback = log_callback or (lambda msg: None)
        self.is_running = False
        self.current_task = ""

    def log(self, message: str):
        """Envia mensagem para o callback de log."""
        self.log_callback(message)

    # ==================== CPU / GPU / RAM BOOST ====================

    def set_high_performance_power_plan(self) -> bool:
        """Ativa o plano de energia de Alto Desempenho."""
        try:
            # Lista planos disponíveis
            result = subprocess.run(
                ['powercfg', '/list'],
                capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )

            # GUID do plano Alto Desempenho (padrão do Windows)
            high_perf_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"

            # Tenta ativar
            subprocess.run(
                ['powercfg', '/setactive', high_perf_guid],
                capture_output=True, check=True
            )
            self.log("✓ Plano de energia 'Alto Desempenho' ativado")
            return True
        except subprocess.CalledProcessError:
            self.log("✗ Falha ao ativar plano Alto Desempenho (pode não existir)")
            return False
        except Exception as e:
            self.log(f"✗ Erro ao configurar plano de energia: {e}")
            return False

    def set_process_priority(self, priority: str = "HIGH") -> bool:
        """Define prioridade do processo atual."""
        try:
            priorities = {
                "REALTIME": psutil.REALTIME_PRIORITY_CLASS,
                "HIGH": psutil.HIGH_PRIORITY_CLASS,
                "ABOVE_NORMAL": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
                "NORMAL": psutil.NORMAL_PRIORITY_CLASS,
                "BELOW_NORMAL": psutil.BELOW_NORMAL_PRIORITY_CLASS,
                "IDLE": psutil.IDLE_PRIORITY_CLASS,
            }

            proc = psutil.Process()
            proc.nice(priorities.get(priority.upper(), psutil.HIGH_PRIORITY_CLASS))
            self.log(f"✓ Prioridade do processo definida para {priority}")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao definir prioridade: {e}")
            return False

    def optimize_cpu_affinity(self) -> bool:
        """Otimiza afinidade de CPU para processos de jogos/apps pesados."""
        try:
            # Pega número de CPUs lógicas
            cpu_count = psutil.cpu_count(logical=True)
            if cpu_count <= 1:
                self.log("ℹ Sistema com 1 CPU lógica - afinidade não aplicável")
                return True

            # Define máscara para usar todos os cores exceto o primeiro (reservado para sistema)
            mask = (1 << cpu_count) - 2  # Todos menos CPU 0

            proc = psutil.Process()
            proc.cpu_affinity([i for i in range(1, cpu_count)])
            self.log(f"✓ Afinidade de CPU otimizada (cores 1-{cpu_count-1})")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao otimizar afinidade CPU: {e}")
            return False

    def disable_cpu_parking(self) -> bool:
        """Desativa CPU Parking (cores estacionados) via registro."""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\0cc5b647-c1df-4637-891a-dec355318583"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "ValueMax", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "ValueMin", 0, winreg.REG_DWORD, 0)
            self.log("✓ CPU Parking desativado (requer reinicialização)")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao desativar CPU Parking: {e}")
            return False

    def optimize_gpu_scheduling(self) -> bool:
        """Ativa agendamento de GPU com aceleração de hardware (Windows 10 2004+)."""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2)
            self.log("✓ Agendamento de GPU por hardware ativado (requer reinicialização)")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao configurar GPU Scheduling: {e}")
            return False

    def set_gpu_priority_high(self) -> bool:
        """Define prioridade alta para processos GPU."""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "GPUPriority", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "GPUQuantum", 0, winreg.REG_DWORD, 1)
            self.log("✓ Prioridade GPU configurada para alta")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao configurar prioridade GPU: {e}")
            return False

    def optimize_memory_management(self) -> bool:
        """Otimiza gerenciamento de memória (Large System Cache, etc.)."""
        try:
            # LargeSystemCache - melhora cache de arquivo para servidores/apps pesados
            key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "LargeSystemCache", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "DisablePagingExecutive", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ClearPageFileAtShutdown", 0, winreg.REG_DWORD, 0)

            self.log("✓ Gerenciamento de memória otimizado (requer reinicialização)")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao otimizar memória: {e}")
            return False

    def clean_standby_memory(self) -> bool:
        """Limpa memória em standby (cache) usando EmptyWorkingSet."""
        try:
            # Usa API do Windows para limpar working set de todos os processos
            kernel32 = ctypes.windll.kernel32
            psapi = ctypes.windll.psapi

            # Enumera processos
            max_procs = 1024
            pids = (ctypes.c_ulong * max_procs)()
            cb_needed = ctypes.c_ulong()

            if psapi.EnumProcesses(ctypes.byref(pids), ctypes.sizeof(pids), ctypes.byref(cb_needed)):
                count = cb_needed.value // ctypes.sizeof(ctypes.c_ulong)
                cleaned = 0

                for i in range(count):
                    pid = pids[i]
                    if pid == 0 or pid == 4:  # System Idle / System
                        continue
                    h_process = kernel32.OpenProcess(0x1F0FFF, False, pid)  # PROCESS_ALL_ACCESS
                    if h_process:
                        if psapi.EmptyWorkingSet(h_process):
                            cleaned += 1
                        kernel32.CloseHandle(h_process)

                self.log(f"✓ Working set limpo para {cleaned} processos")
                return True
        except Exception as e:
            self.log(f"✗ Erro ao limpar memória standby: {e}")
            return False

    def run_cpu_ram_boost(self, progress_callback=None) -> bool:
        """Executa otimizações completas de CPU/RAM/GPU."""
        self.is_running = True
        tasks = [
            ("Plano de energia Alto Desempenho", self.set_high_performance_power_plan),
            ("Prioridade do processo", lambda: self.set_process_priority("HIGH")),
            ("Afinidade de CPU", self.optimize_cpu_affinity),
            ("Desativar CPU Parking", self.disable_cpu_parking),
            ("Agendamento GPU Hardware", self.optimize_gpu_scheduling),
            ("Prioridade GPU", self.set_gpu_priority_high),
            ("Gerenciamento de Memória", self.optimize_memory_management),
            ("Limpar Memória Standby", self.clean_standby_memory),
        ]

        success_count = 0
        for i, (name, func) in enumerate(tasks):
            if not self.is_running:
                break
            if progress_callback:
                progress_callback(i / len(tasks) * 100, f"Aplicando: {name}...")
            if func():
                success_count += 1

        if progress_callback:
            progress_callback(100, f"Concluído: {success_count}/{len(tasks)} otimizações aplicadas")

        self.is_running = False
        return success_count == len(tasks)

    # ==================== REGISTRY OPTIMIZATIONS ====================

    REGISTRY_TWEAKS = {
        "Desativar Telemetria": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", winreg.REG_DWORD, 0),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", winreg.REG_DWORD, 0),
        ],
        "Desativar Hibernação": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "HibernateEnabled", winreg.REG_DWORD, 0),
        ],
        "Desativar Prefetch/Superfetch (SSD)": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnablePrefetcher", winreg.REG_DWORD, 0),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnableSuperfetch", winreg.REG_DWORD, 0),
        ],
        "Acelerar Menu Iniciar": [
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "MenuShowDelay", winreg.REG_SZ, "0"),
        ],
        "Desativar Animações": [
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics", "MinAnimate", winreg.REG_SZ, "0"),
        ],
        "Desativar Efeitos Visuais (Performance)": [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", winreg.REG_DWORD, 2),
        ],
        "Aumentar Prioridade I/O": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "IoPageLockLimit", winreg.REG_DWORD, 0x4000000),
        ],
        "Desativar Índice de Pesquisa": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\WSearch", "Start", winreg.REG_DWORD, 4),
        ],
        "Desativar SysMain (Superfetch)": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\SysMain", "Start", winreg.REG_DWORD, 4),
        ],
        "Otimizar TCP/IP (Latência)": [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency", winreg.REG_DWORD, 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TCPNoDelay", winreg.REG_DWORD, 1),
        ],
    }

    def apply_registry_tweaks(self, selected: List[str], progress_callback=None) -> Tuple[int, int]:
        """Aplica tweaks de registro selecionados."""
        total = len(selected)
        success = 0

        for i, tweak_name in enumerate(selected):
            if not self.is_running:
                break

            if progress_callback:
                progress_callback(i / total * 100, f"Aplicando: {tweak_name}...")

            tweaks = self.REGISTRY_TWEAKS.get(tweak_name, [])
            tweak_success = True

            for hkey, path, name, reg_type, value in tweaks:
                try:
                    with winreg.CreateKey(hkey, path) as key:
                        winreg.SetValueEx(key, name, 0, reg_type, value)
                    self.log(f"  ✓ {tweak_name}: {name} = {value}")
                except PermissionError:
                    self.log(f"  ✗ {tweak_name}: Sem permissão para {path}")
                    tweak_success = False
                except Exception as e:
                    self.log(f"  ✗ {tweak_name}: Erro em {name} - {e}")
                    tweak_success = False

            if tweak_success:
                success += 1

        if progress_callback:
            progress_callback(100, f"Registro: {success}/{total} grupos aplicados")

        return success, total

    # ==================== CLEANUP TOOLS ====================

    CLEANUP_PATHS = {
        "Temp do Usuário": r"%TEMP%",
        "Temp do Windows": r"C:\Windows\Temp",
        "Prefetch": r"C:\Windows\Prefetch",
        "Cache do Windows Update": r"C:\Windows\SoftwareDistribution\Download",
        "Relatórios de Erro": r"C:\ProgramData\Microsoft\Windows\WER",
        "Logs de Instalação": r"C:\Windows\Logs",
        "Cache de Miniaturas": r"%LOCALAPPDATA%\Microsoft\Windows\Explorer",
        "Cache do Navegador (Edge)": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache",
        "Cache do Navegador (Chrome)": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache",
        "Lixeira": "recycle_bin",
    }

    def clean_path(self, path: str, progress_callback=None) -> Tuple[int, int]:
        """Limpa arquivos em um caminho. Retorna (arquivos_removidos, espaço_liberado_mb)."""
        expanded = os.path.expandvars(path)
        if not os.path.exists(expanded):
            return 0, 0

        files_removed = 0
        bytes_freed = 0

        try:
            for root, dirs, files in os.walk(expanded, topdown=False):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        os.remove(filepath)
                        files_removed += 1
                        bytes_freed += size
                    except (PermissionError, OSError):
                        pass  # Arquivo em uso ou sem permissão

                # Tenta remover pastas vazias
                for dir_name in dirs:
                    dirpath = os.path.join(root, dir_name)
                    try:
                        os.rmdir(dirpath)
                    except (PermissionError, OSError):
                        pass

        except Exception as e:
            self.log(f"  Erro ao limpar {path}: {e}")

        return files_removed, bytes_freed // (1024 * 1024)

    def empty_recycle_bin(self) -> bool:
        """Esvazia a lixeira."""
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.log("✓ Lixeira esvaziada")
            return True
        except ImportError:
            # Fallback via SHEmptyRecycleBin
            try:
                ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001 | 0x00000010)
                self.log("✓ Lixeira esvaziada (API Windows)")
                return True
            except Exception as e:
                self.log(f"✗ Erro ao esvaziar lixeira: {e}")
                return False
        except Exception as e:
            self.log(f"✗ Erro ao esvaziar lixeira: {e}")
            return False

    def run_cleanup(self, selected: List[str], progress_callback=None) -> Tuple[int, int]:
        """Executa limpeza nos caminhos selecionados."""
        self.is_running = True
        total = len(selected)
        total_files = 0
        total_mb = 0

        for i, name in enumerate(selected):
            if not self.is_running:
                break

            if progress_callback:
                progress_callback(i / total * 100, f"Limpando: {name}...")

            path = self.CLEANUP_PATHS.get(name)

            if name == "Lixeira":
                if self.empty_recycle_bin():
                    total_files += 1
            elif path:
                files, mb = self.clean_path(path, progress_callback)
                if files > 0 or mb > 0:
                    self.log(f"  ✓ {name}: {files} arquivos, {mb} MB liberados")
                total_files += files
                total_mb += mb

        if progress_callback:
            progress_callback(100, f"Limpeza concluída: {total_files} arquivos, {total_mb} MB liberados")

        self.is_running = False
        return total_files, total_mb

    # ==================== SHORTCUTS / TOOLS ====================

    def open_windows_security(self) -> bool:
        """Abre o Windows Security (antivírus nativo)."""
        try:
            subprocess.Popen(['start', 'windowsdefender:'], shell=True)
            self.log("✓ Windows Security aberto")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao abrir Windows Security: {e}")
            return False

    def disable_tablet_mode(self) -> bool:
        """Desativa modo tablet."""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\ImmersiveShell"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "TabletMode", 0, winreg.REG_DWORD, 0)
            self.log("✓ Modo tablet desativado")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao desativar modo tablet: {e}")
            return False

    def open_disk_cleanup(self) -> bool:
        """Abre limpeza de disco nativa."""
        try:
            subprocess.Popen(['cleanmgr'], shell=True)
            self.log("✓ Limpeza de Disco aberta")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao abrir Limpeza de Disco: {e}")
            return False

    def open_storage_sense(self) -> bool:
        """Abre configurações de Sensor de Armazenamento."""
        try:
            subprocess.Popen(['start', 'ms-settings:storagesense'], shell=True)
            self.log("✓ Sensor de Armazenamento aberto")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao abrir Sensor de Armazenamento: {e}")
            return False

    def flush_dns_cache(self) -> bool:
        """Limpa cache DNS."""
        try:
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=True)
            self.log("✓ Cache DNS limpo")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao limpar cache DNS: {e}")
            return False

    def clear_event_logs(self) -> bool:
        """Limpa logs de eventos (Application, System, Security)."""
        try:
            for log in ['Application', 'System', 'Security']:
                subprocess.run(['wevtutil', 'cl', log], capture_output=True)
            self.log("✓ Logs de eventos limpos")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao limpar logs de eventos: {e}")
            return False

    def optimize_drives(self) -> bool:
        """Executa otimização de unidades (desfragmentar/trim)."""
        try:
            subprocess.Popen(['dfrgui'], shell=True)
            self.log("✓ Otimização de Unidades aberta")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao abrir otimização: {e}")
            return False

    def run_sfc_scannow(self) -> bool:
        """Executa verificação de arquivos do sistema."""
        try:
            subprocess.Popen(['sfc', '/scannow'], shell=True)
            self.log("✓ SFC /scannow iniciado (verifique janela do CMD)")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao executar SFC: {e}")
            return False

    def run_dism_restore(self) -> bool:
        """Executa reparo DISM."""
        try:
            subprocess.Popen(['dism', '/online', '/cleanup-image', '/restorehealth'], shell=True)
            self.log("✓ DISM RestoreHealth iniciado (verifique janela do CMD)")
            return True
        except Exception as e:
            self.log(f"✗ Erro ao executar DISM: {e}")
            return False


# ==================== THREAD HELPER ====================

class OptimizationThread(threading.Thread):
    """Thread para executar otimizações sem travar a UI."""

    def __init__(self, target, args=(), kwargs=None, on_progress=None, on_finish=None):
        super().__init__(daemon=True)
        self.target = target
        self.args = args
        self.kwargs = kwargs or {}
        self.on_progress = on_progress
        self.on_finish = on_finish
        self.result = None

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception as e:
            self.result = e
        finally:
            if self.on_finish:
                self.on_finish(self.result)


def run_in_thread(target, args=(), kwargs=None, on_progress=None, on_finish=None):
    """Executa função em thread separada com callbacks."""
    thread = OptimizationThread(target, args, kwargs, on_progress, on_finish)
    thread.start()
    return thread